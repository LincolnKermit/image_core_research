from bs4 import BeautifulSoup
from flask import Flask, render_template
import requests

app = Flask(__name__)
img_url = []


location = input("Enter the location of the image: ")


# Headers and cookies
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}
cookies = {
    "AEC": "Ae3NU9MiziGWk6fjIRXbOH3MGyNaME4XK4OuUEB3FkQigtcaWu_-P5Xiew",
    "NID": "512=FjqxFKCHZX_DX5eZAOVeui6C5VWMEXQyFBq1EFkyjHwVvAa9HkCpnsPwwXHHhhjkKp9BzG0wjShiDMIa8BjOGoQNqxRt1JXpTe5CG1WSpIMXkrP91lgUJw68t8hLwbN77AMkVl5dB96lntcbCUJeFgkaLbKdgDL8TwV6tkIruqZUqRRM",
    "SOCS": "CAISNQgQEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjQwMzA1LjA1X3AwGgJmciACGgYIgMLTrwY"
}

def yandex_search(location: str):
    location = location
    yandex_format = "https://yandex.ru/images/search?rpt=imageview&url=" + location
    soup = BeautifulSoup(requests.get(yandex_format, headers=headers).text, 'html.parser')
    images = [img.attrs['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    for url in images:
        if url in img_url:
            print("Duplicate found from Yandex")
            pass
        else:
            print("New image found from Yandex")
            img_url.append(url)
    return img_url

def google_search(location: str):
    location = location
    google_format = "https://lens.google.com/uploadbyurl?url=" + location
    soup = BeautifulSoup(requests.get(google_format, headers=headers, cookies=cookies, allow_redirects=True).text, 'html.parser')
    for url in soup:
        if url.startwith("https://lens.google.com/search?ep="):
            redirect_url = url
            print(url)
    soup = BeautifulSoup(requests.get(redirect_url, headers=headers, cookies=cookies).text, 'html.parser')
        
    images = [img.attrs['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    
    for url in images:
        if url in img_url:
            print("Duplicate found from Google")
            pass
        else:
            print("New image found from Google")
            img_url.append(url)
    return img_url


image_urls = yandex_search(location)
image_urls += google_search(location)

# Open web browser
@app.route('/')
def index():
    return render_template('index.html', image_urls=image_urls, i=len(image_urls))


if __name__ == '__main__':
    print("\n")
    print("Searching for images...")
    print("\n")
    print("Running on localhost - port 5000")
    app.run(debug=False, port=5000)
















'''
<img src="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTCOqYnH96y4Ay_kBKYiU2hjB_p_QwX8qwXz7UPJuDqqEbQRqpY" class="wETe9b jFVN1" aria-hidden="true" data-iml="1235">

'''