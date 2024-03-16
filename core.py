import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
import webbrowser





app = Flask(__name__)
img_url = []
location = input("Enter the location of the image: ")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

def yandex_search(location: str):
    location = location
    yandex_format = "https://yandex.ru/images/search?rpt=imageview&url=" + location
    soup = BeautifulSoup(requests.get(yandex_format, headers=headers).text, 'html.parser')
    images = [img.attrs['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    for url in images:
        if url in img_url:
            print("Duplicate found")
            pass
        else:
            print("New image found")
            img_url.append(url)
    return img_url

def google_search(location: str):
    location = location
    google_format = "https://lens.google.com/uploadbyurl?url=https://cdn-idf.opendigitaleducation.com/assets/themes/ode-bootstrap-neo/images/widget-3.png" + location
    soup = BeautifulSoup(requests.get(google_format, headers=headers).text, 'html.parser')
    print(soup.prettify())
    images = [img.attrs['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    print(images)
    for url in images:
        if url in img_url:
            print("Duplicate found")
            pass
        else:
            print("New image found")
            img_url.append(url)
    return img_url




image_urls = yandex_search(location)
image_urls += google_search(location)



# Open web browser
@app.route('/')
def index():
    return render_template('index.html', image_urls=image_urls, i=len(image_urls))


if __name__ == '__main__':
    print("Running on localhost - port 5000")
    app.run(debug=False, port=5000)

