#load urllib, beautifulsoup, and pandas
import urllib.request as req
import bs4
import pandas as pd

#crawl html of gossiping board 
def getData(url):
    #headers include cookie and user-agent
    request=req.Request(url, headers={
        'cookie':'over18=1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    })
    with req.urlopen(request) as response:
        data=response.read().decode('utf-8')

    #analysing html and picking up '推文數'、'標題'、'網址'
    root=bs4.BeautifulSoup(data, 'html.parser')
    titles=root.find_all('div', class_='r-ent') #searching 'div' which in 'class=r-ent'
    data = []
    for title in titles:
        if title.a != None:#printing out title if 'a' exists
            eachtitle = title.a.string
            eachurl = 'https://www.ptt.cc/'+title.a['href']
            if title.span != None: #Under the condition of first 'if', printing out the string of 'span'
                push = title.span.string
            else:
                push = '0'#printing out as '0' if there is no span 
        c = [push, eachtitle, eachurl]        
        data.append(c)   
    dataframe(data)
    
    u = root.select("div.btn-group.btn-group-paging a") 
    print ("---------本頁的URL為", url, '---------')
    url = "https://www.ptt.cc"+ u[1]["href"] 
            
    # crawl next link 
    nextlink=root.find('a',string='‹ 上頁') # searching 'a' when string=' 上頁'
    return nextlink['href']


def make_clickable(val):
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)

def dataframe (data):
    pd.set_option('display.max_colwidth', 250)
    df = pd.DataFrame(data, columns = ['推文數','標題','網址'])
    display(df.style.format({'網址':make_clickable}))
    

#input url and number of pages
siteaddress=str(input('請輸入Ptt討論版網址：'))
pagenumber=int(input('請輸入要抓取的頁數：'))

pageurl=siteaddress
count=0
while count<pagenumber:
    pageurl='https://www.ptt.cc' + getData(pageurl)
    count+=1
