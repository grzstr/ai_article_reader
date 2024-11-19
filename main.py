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

    def read_article(self):
        if not os.path.exists(self.article_name):
            self.get_article()
            
        file = open(self.article_name, "r",  encoding="utf-8")
        content = file.read()
        file.close()
        
        return content

    def get_article(self):
        r = requests.get(self.article_url, allow_redirects=True)
        
        with open(self.article_name, 'wb') as file:
            file.write(r.content)

    def save_as_html(self, content):
        if content.startswith("```html") and content.endswith("```"):
            content = content[8:-3]
        with open("article.html", "wb") as file:
            file.write(bytes(content, 'utf-8'))

    @timed
    def ask_chat_gpt(self):
        client = OpenAI()

        print("Asking ChatGPT")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                "type": "text", 
                "content":  'Convert this article to HTML.Suggest where it is worth placing images by inserting <img src="image_placeholder.jpg" alt="">.' + \
                            ' In the alt attribute, include a detailed prompt for generating the image. Place every image in new line.' + \
                            f' Its content is to be placed in the <body> section, and return only this section: {self.read_article()}'}
            ]
        )

        self.save_as_html(completion.choices[0].message.content)




chat = AskChat()

chat.ask_chat_gpt()