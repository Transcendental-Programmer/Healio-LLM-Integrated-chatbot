
# Hospital System Chatbot

## Description
This project implements a chatbot interface for a hospital system. It uses a LangChain agent designed to answer questions about hospitals, patients, visits, physicians, and insurance payers in a simulated hospital system. The chatbot utilizes retrieval-augmented generation (RAG) over both structured and unstructured synthetically generated data.

## Images
### 1. Home_page
   ![home_page](https://github.com/Transcendental-Programmer/Healio-LLM-Integrated-chatbot/blob/main/static/images/home_page.png)
### 2. Prompt_Example
   ![Prompt_example](https://github.com/Transcendental-Programmer/Healio-LLM-Integrated-chatbot/blob/main/static/images/example_prompt.png)

## Features
- Interactive web-based chat interface
- Answers questions about various aspects of the hospital system
- Utilizes a LangChain agent with RAG for information retrieval and response generation

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Transcendental-Programmer/Healio-LLM-Integrated-chatbot.git
   cd Healio-LLM-Integrated-chatbot
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:8000`

3. Start interacting with the chatbot by typing questions in the input field

### OR use Docker

1. run the requirements.txt

2. Place this Dockerfile in your project's root directory.

3. Build the Docker image:
   ```
   docker build -t hospital-system-chatbot .
   ```

4. Run the container:
   ```
   docker run -p 5000:5000 hospital-system-chatbot
   ```


## Technologies Used
- Python
- Flask
- LangChain
- MongoDB
- HTML/CSS/JavaScript

## Contributing
Contributions to improve the chatbot are welcome. Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit them (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License
[MIT License](https://opensource.org/licenses/MIT)

## Contact
Your Name - priyena.career@gmail.com

Project Link: https://github.com/Transcendental-Programmer/Healio-LLM-Integrated-chatbot/
