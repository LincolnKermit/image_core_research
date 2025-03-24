from bs4 import BeautifulSoup
from flask import Flask, render_template
import lib, requests, os
import webbrowser as wb


PORT = 1337
DEBUG_MODE = True
os.system("clear")

app = Flask(__name__)
img_url = []
image_extensions = (".jpg", ".jpeg", ".png", ".webp")
url = ""
location = input("URL : ")

if location == "":
    print("URL is empty")
    exit()
elif location.endswith(image_extensions):
    print("URL is a direct image link.")
else:
    # Check if the URL contains one of the image extensions but does not end with it
    if any(ext in location for ext in image_extensions):
        # Find the position of the image extension
        for ext in image_extensions:
            if ext in location:
                ext_position = location.find(ext)
                break
        # Extract the URL up to the image extension
        modified_location = location[:ext_position + len(ext)]
    else:
        print("URL doesn't seem to point to an image.")
title_yandex = ""

def loading(x: int) -> int:
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

def yandex_search(location: str) -> str:
    global title_yandex
    global description_yandex
    location = location
    yandex_format = "https://yandex.ru/images/search?rpt=imageview&url=" + location
    response = requests.get(yandex_format, headers=lib.headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        title_yandex = soup.find('h2', class_='CbirObjectResponse-Title').text
    except:
        title_yandex = "NO IDENTIFIED TITLE"
    try:
        description_yandex = soup.find('div', class_='CbirObjectResponse-Description').text
    except:
        description_yandex = "NO DESCRIPTION"
    if response.status_code == 200:
        print("Fetching done on Yandex.")
    elif response.status_code == 301:
        print("Redirection detected, probably means you have been rate limited.")
    else:
        print("Error during Fetching on Yandex.")
        exit("Error : "+str(response.status_code))

    images = [img.attrs['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    for url in images:
        if url in img_url:
            print("Duplicate found from Yandex")
            pass
        else:
            img_url.append(url)
            loading(img_url)
    return img_url, response.status_code

def google_search(location: str) -> str:
    location = location
    google_format = "https://lens.google.com/uploadbyurl?url=" + location
    # TODO : allow cookie box = True
    soup = BeautifulSoup(requests.get(google_format, headers=lib.headers, cookies=lib.cookies, allow_redirects=True).text, 'html.parser')
    # lib.cookie is empty. TO FIX
    for url in soup:
        if url.startwith("https://lens.google.com/search?ep="):
            redirect_url = url
            print(url)
        else:
            ("Google URL Redirect Error, Still trying to fetch the image...")
    soup = BeautifulSoup(requests.get(redirect_url, headers=lib.headers, cookies=lib.cookies).text, 'html.parser')
    # lib.cookie is empty. TO FIX
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
    return render_template('index.html', image_urls=img_url, i=len(img_url), title_yandex=title_yandex, description_yandex=description_yandex, location=location)

try:
    image_urls = yandex_search(location)
except Exception as e:
    print("Error during Yandex Search:", e)

title_yandex = title_yandex
description_yandex = description_yandex

if __name__ == '__main__':
    print("\n")
    print(" * "+str(len(img_url))+f" Results \n *  Running on localhost - port {PORT} - Debug = {DEBUG_MODE}")
    wb.open(f"localhost:{PORT}")
    app.run(debug=DEBUG_MODE, port=PORT)
