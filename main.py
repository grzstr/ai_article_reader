from openai import OpenAI
from tqdm import tqdm
import requests
import os



def timed(fn):
    from time import perf_counter
    from functools import wraps

    @wraps(fn)
    def inner(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        elapsed = end - start

        print(f"{fn.__name__} took {elapsed:.6f} to run.")
        return result

    return inner


class AskChat():
    def __init__(self):
        self.article_url = "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"
        
        self.article_name = "article.txt"
        
        self.article_html = 'artykul.html'
        self.szablon_html = 'szablon.html'
        self.podglad_html = 'podglad.html'


    def create_preview(self):
        #Merging the files szablon.html and article.html
        if os.path.exists(self.article_html) and os.path.exists(self.szablon_html):
            with open(self.article_html, 'r', encoding='utf-8') as artykul_file:
                artykul_content = artykul_file.read()

            with open(self.szablon_html, 'r', encoding='utf-8') as szablon_file:
                szablon_content = szablon_file.read()

            output_content = szablon_content.split('<body>')[0] + '\n<body>\n'+ artykul_content + '\n</body>\n' + szablon_content.split('</body>')[1]

            with open(self.podglad_html, 'w', encoding='utf-8') as output_file:
                output_file.write(output_content)
        else:
            raise FileNotFoundError(f"You need '{self.article_html}' and '{self.szablon_html}' to create a preview!")

    def read_article(self):
        #Reading .txt file
        if not os.path.exists(self.article_name):
            self.get_article()
            
        with open(self.article_name, "r",  encoding="utf-8") as file:
            content = file.read()
        
        return content

    def get_article(self):
        #Downloading the article from website
        r = requests.get(self.article_url, allow_redirects=True, timeout=10)

        #Errors if website doesn't respond
        if r.status_code == 404:
            raise FileNotFoundError(f"The file at '{self.article_url}' does not exist (HTTP 404).")
        elif r.status_code != 200:
            raise Exception(f"Failed to download the file. HTTP response code: {r.status_code}")
        else:
            #Size of file
            total_size = int(r.headers.get('Content-Length', 0))
            #Saving article as .txt file
            with open(self.article_name, 'wb') as file:
                if total_size > 0:
                    #Progress Bar
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading: {self.article_name}") as bar:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                                bar.update(len(chunk)) #Updating progress bar

    def save_as_html(self, content, file_name):
        #Saving respond from ChatGPT as HTML file
        if content.startswith("```html") and content.endswith("```"):
            content = content[8:-3]
        with open(file_name, "wb") as file:
            file.write(bytes(content, 'utf-8'))

    @timed
    def convert_to_html(self):
        #Converting txt file to html
        client = OpenAI()
        content = self.read_article()
        print("Asking ChatGPT - ", end='')
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a tool to process user inputs as fresh tasks without using prior context."},
                {"role": "user",
                "type": "text", 
                "content":  'Convert the article to HTML. In text use attributes like <p>, <h1>, <article>, <section>, <footer>, etc.' + \
                            " Suggest where it is worth placing images by inserting <img src='image_placeholder.jpg' alt="">. Don't change this command!" + \
                            ' In the alt attribute, include a detailed prompt for generating the image.' + \
                            ' Add a caption to each image in polish and use appropriate tags. Place every image in new line.' + \
                            f' Its content is to be placed in the <body> section, and return only this section, without <body>, </body> signatures: {content}'},
            ]
        )

        self.save_as_html(completion.choices[0].message.content, self.article_html)


    @timed
    def generate_template(self):
        #Generating template
        client = OpenAI()
        print("Asking ChatGPT - ", end = '')
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a tool to process user inputs as fresh tasks without using prior context."},
                {"role": "user",
                "type": "text", 
                "content":  "Create an HTML template to nicely present an article within the <body>. In this template, <body> section must be empty! Don't place anything in there" + \
                            " Please, don't add your comments. CSS styles must be placed inside the HTML file." + \
                            " Modify the appearance of the text by editing tags such as <p>, <h1>, <article>, <section>, <footer>, etc."},
            ]
        )

        self.save_as_html(completion.choices[0].message.content, self.szablon_html)

if __name__ == '__main__':
    chat = AskChat()
    chat.convert_to_html()
    chat.generate_template()
    chat.create_preview()