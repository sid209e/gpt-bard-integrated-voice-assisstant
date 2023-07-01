# gpt-bard-integrated-voice-assisstant


This project implements a voice assistant powered by GPT-3 and Bard. The voice assistant can understand voice commands, process natural language queries, and provide appropriate responses using GPT-3 language model and the Bard chatbot.

## Prerequisites

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sid209e/gpt-bard-voice-assistant.git
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Description

The voice assistant is designed to interact with users through speech recognition and synthesis. It utilizes the following technologies:

- **Speech Recognition**: The `speech_recognition` library is used to capture audio input from the user and convert it into text.
- **Amazon Polly**: The Amazon Polly service is utilized for text-to-speech synthesis. It converts the assistant's responses into speech.
- **OpenAI GPT-3**: The OpenAI GPT-3 language model is integrated to generate human-like responses based on user queries and prompts.
- **Bard Chatbot**: The `Bard` chatbot module provides a simplified interface for interacting with the GPT-3 model.

The code initializes the necessary libraries and services, sets up the speech recognition system, and defines functions for handling user prompts, generating responses, and converting text to speech. The voice assistant supports two wake words: "gpt" and "google". Once the assistant is activated, it listens for user queries, sends them to the appropriate language model (GPT-3 or Bard), and plays the generated responses using speech synthesis.

## Usage

1. Modify the code (`gpt_bard_voice_assistant.py`) to remove sensitive credentials and replace them with placeholder values.

2. Run the code:

```bash
python gpt_bard_voice_assistant.py
```

3. Say the wake word ("gpt" or "google") to activate the voice assistant.

4. Speak your query or command to interact with the assistant.

5. The assistant will process your input, generate a response, and play it back as speech.

6. You can use the phrase "OK stop" to terminate the assistant and exit the program.

## Contributing

Contributions are welcome! If you find any issues or have suggestions, please open an issue or submit a pull request.

## License

This project is licensed under the [GNU Public License](LICENSE). You are free to modify and distribute the code under the terms of this license. 




## License

This project is licensed under the [GNU Public License](LICENSE). You are free to modify and distribute the code under the terms of this license. 

