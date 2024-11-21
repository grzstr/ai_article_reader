# Junior AI Developer Task

## Description

This repository contains the implementation of the recruitment task for the Junior AI Developer position at Oxido. The application is written in Python and is designed to:

1. Connect with the OpenAI API.
2. Read a text file containing an article.
3. Process the article content along with a prompt using OpenAI's API.
4. Save the generated HTML code into a file named `artykul.html`.
5. Generate an HTML template `szablon.html`
6. Combine the generated article with the template
7. Save the final result into a file named `podglad.html`

## Requirements

- Python 3.x (recommended: Python 3.8 or higher)
- OpenAI API key

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:grzstr/ai_article_reader.git
   cd ai_article_reader
   ```

2. **Install Dependencies**
   ```bash
   pip install openai
   ```
3. **Set Up API Key**  
   To use the OpenAI API, you need to configure your API key:
   - Create an account on [OpenAI](https://platform.openai.com/signup)
   - Once signed in, go to [API keys](https://platform.openai.com/account/api-keys) and generate a new key.
   - Set the API key as an environment variable:
   ```bash
   export OPENAI_API_KEY = 'your-api-key'
   ```
   
   Full Documentation is here: 
   [OpenAI Quickstart Documentation](https://platform.openai.com/docs/quickstart)

4. **Run the Application**  
   ```bash
   python main.py
   ```

5. **View the Output**  
   Check the `podglad.html` file in the repository directory

