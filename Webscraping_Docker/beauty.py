from bs4 import BeautifulSoup   #이렇게 임포트한다.
#일반 cmd창에서 한글이 안나올때는 cmd창에 chcp 949를 입력한다.


#태그 선택자
"ul"
"div"
"li"
# 아이디 선택자
"#<아이디 이름>"
# 클래스 선택자
".<클래스 이름>"
# 클래스 선택자
".<클래스 이름>.<클래스 이름>.<클래스 이름>.<클래스 이름>"
# 후손 선택자 -- 어떤 태그 아래 있는 모든 녀석 children
"#meigen li"
# 자식 선택자 -- 어떤 태그의 바로 아래 있는 하나의 녀석만. child
"ul.items > li"


"#meigen" # id 선택자.
".items"
".art"
".book"
".it"
".book.art.it.items" #class가 여러개인 경우 다 사용하고싶을 때.
"ul.book.art.it.items"

html = """
<html>
    <body>
        <div id="meigen">
        <h1>위키독스 독서</h1>
        <ul class="items art it book">
            <li>유니티 게임 이펙트 입문</li>
            <li>스위프트로 시작하는 아이폰 앱 개발 교과서</li>
            <li>모던 웹사이트 디자인의 정석</li>
        </ul>
    </div>
    </body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

soup.select_one("h1") #하나를 선택함. h1선택하기. 요소이다.
soup.select_one("div > h1")

header= soup.select_one("body > div> h1")
list_items = soup.select("ul.items > li") #여러개를 선택함. 요소의 배열이다.

print(header.string)
# header.attrs["title"]
print(soup.select_one("ul").attrs) #attributes 사용해서 속성 추출하기.


for li in list_items:
    print(li.string)