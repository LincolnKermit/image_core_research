
# Image Core Researcher

Image Core Researcher is hand-made tool for osint research purpose. (IMINT)

This tools uses Yandex ( Note that the tool doesn't requires or use any API... )

After fetching the matching image, the source of the image is sent to the flask server running on 127.0.0.1 on port 1337.

Please note that the tool is still in developpement and may have bugs or isn't strong enough to find more than 10 pictures




## Demo


Original Image
![App Screenshot](https://images.rtl.fr/~c/770v513/rtl/www/1662832-emmanuel-macron-le-12-mars-2024.jpg)

Processed Image
![App ScreenShot](https://img001.prntscr.com/file/img001/26ydQ6xLQ-mTwGbOmOdbGQ.png)

## Installation

Install my-project with git

```bash
  git clone https://github.com/Lincoln/image_core_research
  cd image_core_research/
  pip3 install flask, bs4
  python3 core.py
```
    
## Run Locally



```bash
  python3 core.py
```


URL :

```bash
  127.0.0.1:1337
```

