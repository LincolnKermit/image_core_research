import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template


app = Flask(__name__)


location = input("Enter the location of the image: ")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

def image_search(location: str):
    location = location
    yandex_format = "https://yandex.ru/images/search?rpt=imageview&url=" + location
    print(yandex_format)
    soup = BeautifulSoup(requests.get(yandex_format, headers=headers).text, 'html.parser')
    print("soup: ")
    img_url = []
    images = [img.attrs['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    for url in images:
        img_url.append(url)
    return img_url



@app.route('/')
def index():
    print("index 1")
    image_urls = image_search(location)
    print("index 2")
    return render_template('index.html', image_urls=image_urls)


if __name__ == '__main__':
    print("Running...")
    app.run(debug=True, port=5000)
