from bs4 import BeautifulSoup
from flask import Flask, render_template
import lib, requests, math, os, time

app = Flask(__name__)
img_url = []
url = "0"
location = input("URL : ")

def loading(x):
    x = int(len(x))
    y = round(100 / x)
    z = round(100 / x)
    starter = '['
    ender = ']'
    string = '█'
    blank = '.'

    while y < 100:
        os.system("clear")
        y = y + z
        space = (100 - y)
        if y > 100:
            print(starter + (string * 100) + ender)
            print("100 %")
            break
        else:
            print(starter + ((string * y) + (blank * space)) + ender)
            print(y, "%")

def yandex_search(location: str):
    location = location
    yandex_format = "https://yandex.ru/images/search?rpt=imageview&url=" + location
    soup = BeautifulSoup(requests.get(yandex_format, headers=lib.headers).text, 'html.parser')
    if requests.status_codes == 200:
        print("Fetching done.")
    else:
        print("Error during Fetching")

    images = [img.attrs['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    for url in images:
        if url in img_url:
            print("Duplicate found from Yandex")
            pass
        else:
            img_url.append(url)
            loading(img_url)
    return img_url

def google_search(location: str):
    location = location
    google_format = "https://lens.google.com/uploadbyurl?url=" + location
    # TODO : allow cookie box = True
    soup = BeautifulSoup(requests.get(google_format, headers=lib.headers, cookies=lib.cookies, allow_redirects=True).text, 'html.parser')
    for url in soup:
        if url.startwith("https://lens.google.com/search?ep="):
            redirect_url = url
            print(url)
    soup = BeautifulSoup(requests.get(redirect_url, headers=lib.headers, cookies=lib.cookies).text, 'html.parser')

    images = [img.attrs['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    # add or endwith .jpg .jpeg .png .webp    
    for url in images:
        if url in img_url:
            print("Duplicate found from Google")
            pass
        else:
            print("New image found from Google")
            img_url.append(url)
            loading(img_url)
    return img_url

# Open web browser
@app.route('/')
def index():
    return render_template('index.html', image_urls=image_urls, i=len(image_urls))

try:
    image_urls = yandex_search(location)
except:
    print(requests.status_codes)

if __name__ == '__main__':
        print("\n")
        print(" * "+str(len(img_url))+" Results \n *  Running on localhost - port 1337 - Debug = False")
        app.run(debug=False, port=1337)
        # port 1337