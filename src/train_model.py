import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from chatbot import chatbot

def generate_training_data(questions):
    training_data = []
    for question in questions:
        response = chatbot(question)
        training_data.append(f"Question: {question}\nAnswer: {response}\n\n")
    
    with open("training_data.txt", "w") as f:
        f.writelines(training_data)

def train_model():
    # Load pre-trained model and tokenizer
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokenizer.pad_token = tokenizer.eos_token

    # Prepare the dataset
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path="training_data.txt",
        block_size=128
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    # Train the model
    trainer.train()

    # Save the fine-tuned model
    model.save_pretrained("./fine_tuned_gpt2")
    tokenizer.save_pretrained("./fine_tuned_gpt2")

if __name__ == "__main__":
    questions = [
        "What is the current wait time at wallace-hamilton hospital?",
        "Which hospital has the shortest wait time?",
        "At which hospitals are patients complaining about billing and insurance issues?",
        "What is the average duration in days for emergency visits?",
        "What are patients saying about the nursing staff at Castaneda-Hardy?",
        "What was the total billing amount charged to each payer for 2023?",
        "What is the average billing amount for medicaid visits?",
        "How many patients has Dr. Ryan Brown treated?",
        "Which physician has the lowest average visit duration in days?",
        "How many visits are open and what is their average duration in days?",
        "Have any patients complained about noise?",
        "How much was billed for patient 789's stay?",
        "Which physician has billed the most to cigna?",
        "Which state had the largest percent increase in medicaid visits from 2022 to 2023?",
    ]

    generate_training_data(questions)
    train_model()