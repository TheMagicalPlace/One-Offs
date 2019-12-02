from bs4 import BeautifulSoup as soup
import requests
import json
import asyncio
import time



def SCP_scraper(itemno,tag,minrating=0):
    print(f'{itemno} executed at ' + str(time.time()))
    skip = requests.get(f'http://www.scp-wiki.net/scp-{itemno}')
    scp = soup(skip.text,features="html.parser")
    try:
        rating = int(scp.select('span[class=\'number prw54353\']')[0].string[1:])
    except IndexError:
        print(f'{itemno} comp at ' + str(time.time()))
        print(itemno)
        return
    if rating < minrating:
        print(f'{itemno} comp at' + str(time.time()))
        return
    page_tags = scp.select('div[class="page-tags"] span a')
    page_tags = [tag.string for tag in page_tags]
    if tag in page_tags:
        print(f'{itemno} comp at' + str(time.time()))
        return f'http://www.scp-wiki.net/scp-{itemno}'
    print(f'{itemno} comp at' + str(time.time()))


def save_results(tag,output):
    try:
        with open('tagskips','r') as skiplist:
            lst = json.load(skiplist)
            lst[tag] = output
        with open('tagskips','w') as skiplist:
            json.dump(lst,'tagskips')
    except FileNotFoundError:
        with open('tagskips','w') as skiplist:
            json.dump({f'{tag}':output},'tagskips')

async def search_main(tag,minrating=0):
    output = []
    for i in range(2,150):
        if i < 100:
            if i < 10:
                no = f'00{i}'
            else:
                no = f'0{i}'
        else:
            no = str(i)
        output.append(SCP_scraper(no,tag,minrating))
    #save_results(tag,output)





if __name__ == '__main__':
    t = time.time()
    asyncio.run(search_main(None))
    print(time.time()-t)
