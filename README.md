# Two Bots Dialogue

This is a simple python script in which two LLM models (llama3-8b-8192 from Groq API, and gemini-1.5-flash from Google Generative AI API) discuss a subject chosen by user input. The diaogue is recorded in a conversation log file until the user stops the program. See the example conversation log.

## Getting Started

### Prerequisites
Ensure you have Python installed on your system. You can check by running:
```bash
python --version
```
or
```bash
python3 --version
```
You will need to get a free API key from both Groq API and Google Generative AI API. You can get the former [here](https://console.groq.com/keys) and the latter [here](https://aistudio.google.com/app/apikey)

### Installation
1. Clone the Repository:
```bash
git clone https://github.com/SpyderRex/TwoBotsDialogue.git
cd TwoBotsDialogue
```

2. Install the Requirements:
Install the necessary dependencies using pip:
```bash
pip install -r requirements.txt
```

3. Rename the .env.template file to .env and add your two API keys to the file in the appropriate place.

## Usage
To run the program, simply execute the following command in your terminal:
```bash
python bot_dialogue.py
```
or
```bash
python3 bot_dialogue.py
```

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact
Spyder Rex - rex.multimedia.llc@gmail.com

Project Link: https://github.com/SpyderRex/TwoBotsDialogue

## Donating
If you wish to donate financially to this project, you can do so [here](https://www.paypal.com/donate/?hosted_button_id=N8HR4SN2J6FPG)
