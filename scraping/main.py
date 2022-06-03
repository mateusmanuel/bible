from termios import VSTART
import requests
import re
from bs4 import BeautifulSoup

def make_testament(testament):
    main_page = requests.get('https://www.vatican.va/archive/bible/nova_vulgata/documents/nova-vulgata_'+testament+'_lt.html')
    main_soup = BeautifulSoup(main_page.text, 'html.parser')

    for li in main_soup.find('ul').find_all('li'):
        a = li.find('a')
        link = a['href']
        title = (a.text).lstrip()

        # if "Psalm" or "Esther" in title:
        #     continue

        make_book(link, title, testament)
        print("\\input{"+testament+"/"+title+".tex}\\flushcolsend")
        

def make_book(link, title, testament):
    page = requests.get('https://www.vatican.va/archive/bible/nova_vulgata/documents/'+link)
    soup = BeautifulSoup(page.text, 'html.parser')

    body = soup.find('tbody').find('tbody').find('td')

    with open('/home/mateus/Programming/bible/'+testament+'/'+title+'.tex', mode='w') as f:
        f.write("\\biblebook{"+title+"}\n")
        for p in body.find_all('p'):
            # p_str = str(p)
            if 'name' in str(p):
                p.b.decompose()
                p_str = p.text
                # cap = p_str.split(' ',2)[2] # rm cap number
                # verses = p_str.split('<br/>')

                f.write("\n\\begin{biblechapter}")

                # for v in verses:
                    # vx = v.replace("<font size=\"3\">","").replace(" </font>","")
                vx = re.sub(r'\d+ ', '\n@ ', p_str)
                vx = re.sub(r'(\d+)a ', '\n@ a ', vx)
                vx = vx.replace("@","\\verse")
                vx = vx.replace("“ ","“")
                vx = vx.replace(" ”","\"")

                f.write(vx+"\n")

                f.write("\\end{biblechapter}\n")
        f.close()


make_testament('vetus-testamentum')    
make_testament('novum-testamentum')



# main_page = requests.get('https://www.vatican.va/archive/bible/nova_vulgata/documents/nova-vulgata_vetus-testamentum_lt.html')
# main_soup = BeautifulSoup(main_page.text, 'html.parser')

# for li in main_soup.find('ul').find_all('li'):
#     a = li.find('a')
#     link = a['href']
#     title = a.text

#     print(title)

#     if "Psalm" in title:
#         continue

#     make_book(link, title, "old_testament")

    
                