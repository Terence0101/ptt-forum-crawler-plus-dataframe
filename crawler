#抓取ptt某討論板的網頁原始碼(HTML)
import urllib.request as req
import bs4
import pandas as pd

def getData(url):
    #建立一個request 物件，所以附加request headers的資訊
    request=req.Request(url, headers={
        'cookie':'over18=1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    })
    with req.urlopen(request) as response:
        data=response.read().decode('utf-8')

    #解析原始碼並取得每篇文章標題、推文數、網址
    root=bs4.BeautifulSoup(data, 'html.parser')
    titles=root.find_all('div', class_='r-ent')#找class="r-ent"的div標籤
    data = []
    for title in titles:
        if title.a != None:#如果標題有a標籤就印出來
            eachtitle = title.a.string
            eachurl = 'https://www.ptt.cc/'+title.a['href']
            if title.span != None:#在標題有a的情況下，如果有span標籤也印出來
                push = title.span.string
            else:
                push = '0'##在標題有a的情況下，如果沒有span標籤補0印出來
        c = [push, eachtitle, eachurl]        
        data.append(c)   
    dataframe(data)
    
    u = root.select("div.btn-group.btn-group-paging a") #a標籤
    print ("---------本頁的URL為", url, '---------')
    url = "https://www.ptt.cc"+ u[1]["href"] #本頁的網址
            
    #抓取下一頁連結
    nextlink=root.find('a',string='‹ 上頁')#找到內文是 上頁的a連結
    return nextlink['href']

#在Jupyter上運行需要補上以下兩行程式碼。在Watson Studio上運行則不用。
#def make_clickable(val):
    #return '<a target="_blank" href="{}">{}</a>'.format(val, val)

def dataframe (data):
    pd.set_option('display.max_colwidth', 250)
    df = pd.DataFrame(data, columns = ['推文數','標題','網址'])
    display(df.style.format({'網址':make_clickable}))

#抓取一個頁面的標題
siteaddress=str(input('請輸入Ptt討論版網址：'))
pagenumber=int(input('請輸入要抓取的頁數：'))

pageurl=siteaddress
count=0
while count<pagenumber:
    pageurl='https://www.ptt.cc' + getData(pageurl)
    count+=1
