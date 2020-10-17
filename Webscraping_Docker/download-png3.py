import urllib.request
import urllib.parse

api = "https://search.naver.com/search.naver" 
values = {
    "sm":"top_hty",
    "fbm": "1",
    "ie": "utf8",
    "query": "초콜릿"
}
params = urllib.parse.urlencode(values)
url = api + "?" + params

# print(api)
# print(params)
# print(url)

data = urllib.request.urlopen(url).read()
text = data.decode("utf-8") #euc-kr
print(text)
# print(data)

"""
https://smartstore.naver.com/bestch1/products/4756898130?NaPm=ct%3Dkgce94og%7Cci%3Deab921d1947c0c16d2556ed3d7b047fc9ab6a219%7Ctr%3Dsls%7Csn%3D536251%7Chk%3D92126fac7aea2cda8b1d33bbe6562565ceff50f5


방식 : GET, POST, PUT, DELETE
대상 : https://smartstore.naver.com/    => 호스트이름
추가적인 정보
- 경로(path) : /bestch1/products/4756898130
- 데이터(data) 지정 Get방식 한정: ?NaPm=ct%3Dkgce94og%7Cci%3Deab921d1947c0c16d2556ed3d7b047fc9ab6a219%7Ctr%3Dsls%7Csn%3D536251%7Chk%3D92126fac7aea2cda8b1d33bbe6562565ceff50f5



C:\a\a.py


https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%B4%88%EC%BD%9C%EB%A6%BF


방식 : get
대상: https://search.naver.com
추가적인 정보
- 경로: /search.naver
- 데이터 (요청 매개변수): ?sm=top_hty&fbm=0&ie=utf8&query=%EC%B4%88%EC%BD%9C%EB%A6%BF         # ? key equal 값. 

#4개 모두 데이터라고 부를 수 있다.

?sm=top_hty
&fbm=0
&ie=utf8
&query=%EC%B4%88%EC%BD%9C%EB%A6%BF # 인코딩된 문자이다. 역으로 돌릴 때를 디코딩한다고한다.
utf8&query=초콜릿 #한국어를 사용할 수가 없는 것이다.


"""