from openai import OpenAI
import requests
import os

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
        if content.startswith("```") and content.endswith("```"):
            content = content[3:-3]
        with open("article.html", "wb") as file:
            file.write(bytes(content, 'utf-8'))


    def ask_chat_gpt(self):
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                "type": "text", 
                "content": f"Convert this article to HTML {self.read_article()}"}
            ]
        )

        self.save_as_html(completion.choices[0].message.content)




chat = AskChat()

chat.ask_chat_gpt()