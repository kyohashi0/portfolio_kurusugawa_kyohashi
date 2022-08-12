#searchword.py
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

keyword = 'python'
#検索バーのurlに変数keywordを追加する
url = 'https://kino-code.work/?s={}'.format(keyword)
#リンクを呼び出す
r = requests.get(url)
time.sleep(3)

soup = BeautifulSoup(r.text,'html.parser')
page_na = soup.find(class_='pagination')
page_num = page_na.find_all(class_='page-numbers')
#ページ番号を取得する
pages = []
for i in page_num:
    pages.append(i.text)
# リストにurlを格納する
urls = []
# 検索結果が1ページだけのとき
if not pages:
    urls = ['https://kino-code.work/?s={}'.format(keyword)]
# 検索結果が複数ページあるとき
else:

    last_page = int(pages[-2])
    for i in range(1,last_page+1):
        url = 'https://kino-code.work/?s={}'.format(keyword) + '&paged={}'.format(i)
        urls.append(url)
# 取得したデータをリンク、タイトル、説明文に分けて格納する
links = []
titles = []
snippets=[]
for i in range(len(urls)):
    r = requests.get(urls[i])
    time.sleep(3)
    soup=BeautifulSoup(r.text, 'html.parser')
    #find_allの引数に、htmlタグが持つCSSクラスで検索をかける
    get_list_info = soup.find_all('a', class_='entry-card-wrap')
    for n in range(len(get_list_info)):
        #リンクを取得   
        get_list_link = get_list_info[n].attrs['href']
        links.append(get_list_link)
        #タイトルを取得
        get_list_title = get_list_info[n].attrs['title']
        titles.append(get_list_title)
        #説明文を取得
        get_list_snippet = get_list_info[n].find(class_='entry-card-snippet').text
        snippets.append(get_list_snippet)

#リストを辞書型に変換する
result ={
    'title':titles,
    'link': links,
    'snippet': snippets
}
#データフレームを作成する
df = pd.DataFrame(result)
df.to_csv('result.csv', index=False, encoding='utf-8')
