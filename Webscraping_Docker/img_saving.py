import urllib.request

url = "http://uta.pw/shodou/img/28/214.png"
savename = "test2.png"


#Download
mem = urllib.request.urlopen(url).read()

with open(savename, mode="wb") as f:   #wrtie binary는 이미지 형태로 저장하겠다는 것, 반대 개념은 text. 
    f.write(mem)
    print("Saved!")














#urllib.request.urlretrieve(url, savename)   # 어떤 url에 있는 것을 어디에 저장할 것인가
