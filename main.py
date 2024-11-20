from openai import OpenAI
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

        args_ = [str(a) for a in args]
        kwargs_ = [f"{k}={v}" for (k, v) in kwargs.items()]
        all_args = args_ + kwargs_
        args_str = ",".join(all_args)
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
        if os.path.exists(self.article_html) and os.path.exists(self.szablon_html):
            with open(self.article_html, 'r', encoding='utf-8') as artykul_file:
                artykul_content = artykul_file.read()

            with open(self.szablon_html, 'r', encoding='utf-8') as szablon_file:
                szablon_content = szablon_file.read()

            output_content = szablon_content.split('<body>')[0] + '\n<body>\n'+ artykul_content + '\n</body>\n' + szablon_content.split('</body>')[1]

            with open(self.podglad_html, 'w', encoding='utf-8') as output_file:
                output_file.write(output_content)
        else:
            print(f"You need '{self.article_html}' and '{self.szablon_html}' to create a preview!")

    def read_article(self):
        if not os.path.exists(self.article_name):
            self.get_article()
            
        with open(self.article_name, "r",  encoding="utf-8") as file:
            content = file.read()
        
        return content

    def get_article(self):
        r = requests.get(self.article_url, allow_redirects=True)
        
        with open(self.article_name, 'wb') as file:
            file.write(r.content)

    def save_as_html(self, content, file_name):
        if content.startswith("```html") and content.endswith("```"):
            content = content[8:-3]
        with open(file_name, "wb") as file:
            file.write(bytes(content, 'utf-8'))

    @timed
    def convert_to_html(self):
        client = OpenAI()
        content = self.read_article()
        print("Asking ChatGPT - ", end='')
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a tool to process user inputs as fresh tasks without using prior context."},
                {"role": "user",
                "type": "text", 
                "content":  'Convert the article to HTML. Suggest where it is worth placing images by inserting <img src="image_placeholder.jpg" alt="">.' + \
                            ' In the alt attribute, include a detailed prompt for generating the image. Add a caption to each image in polish. Place every image in new line.' + \
                            f' Its content is to be placed in the <body> section, and return only this section, without <body>, </body> signatures: {content}'},
            ]
        )

        self.save_as_html(completion.choices[0].message.content, self.article_html)


    @timed
    def generate_template(self):
        client = OpenAI()
        print("Asking ChatGPT - ", end = '')
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a tool to process user inputs as fresh tasks without using prior context."},
                {"role": "user",
                "type": "text", 
                "content":  'Create an HTML template to nicely present an article within the <body>. In this template, <body> section must be empty! Please, dont add your comments'},
            ]
        )

        self.save_as_html(completion.choices[0].message.content, self.szablon_html)

if __name__ == '__main__':
    chat = AskChat()
    chat.generate_template()
    chat.convert_to_html()
    chat.create_preview()