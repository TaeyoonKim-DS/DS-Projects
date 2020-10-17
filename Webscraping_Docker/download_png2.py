import urllib.request

url = "https://api.aoikujira.com/ip/ini"

mem = urllib.request.urlopen(url).read()
print(mem.decode("utf-8"))



#mem = urllib.request.urlopen(url).read()
#print(mem)
#print(mem.decode("euc-kr"))