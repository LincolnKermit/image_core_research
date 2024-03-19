import os, time

image_urls = ['link1','link2','link3','link4','link1','link1','link1','link1','link1','link1','link1','link1','link1','link1']

x = int(len(image_urls))
y = round(100/x)
z = round(100/x)
starter = '['
ender = ']'
string = '*'
blank = '.'


while y < 100:
    time.sleep(0.05)
    os.system("clear")
    y = y + z
    space = (100 - y)
    if y > 100:
        print(starter+(string * 100)+ender)
        print("100 %")
        break
    else:
        print(starter+((string * y)+(blank * space))+ender)
        print(y,"%")