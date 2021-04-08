import requests
from bs4 import BeautifulSoup
import sched, time
s = sched.scheduler(time.time, time.sleep)

class ScrapingApi:
    def scrap_site(self, url, tag, className):
        # url = 'https://www.prothomalo.com/sports/article/1622290/%E0%A6%B8%E0%A6%BE%E0%A6%95%E0%A6%BF%E0%A6%AC%E0%A7%87%E0%A6%B0-%E0%A6%85%E0%A6%A8%E0%A7%81%E0%A6%AA%E0%A6%B8%E0%A7%8D%E0%A6%A5%E0%A6%BF%E0%A6%A4%E0%A6%BF%E0%A6%A4%E0%A7%87-%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6-%E0%A6%AF%E0%A6%BE-%E0%A6%95%E0%A6%B0%E0%A6%A4%E0%A7%87-%E0%A6%AA%E0%A6%BE%E0%A6%B0%E0%A7%87'
        # url = 'https://www.bbc.com/bengali/news-50272570'
        response = requests.get(url)
        print('response', response)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string
        [s.extract() for s in soup(['script', 'style'])]
        # info = soup.find('article')
        info = soup.find(tag, className)
        text = info.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        body = '\n'.join(chunk for chunk in chunks if chunk)

        print('body', body)
        print('title', title)


        # info_img = soup.find("img", {"id": "xzoom-default"})
        image_url = ''
        info_img = soup.find("div", "xzoom-container")
        images = info_img.findAll('img')
        for i, image in enumerate(images):
            if i == 0:
                print(image['src'])
                image_url = image['src']

        

        return {"title": title, "image_url": image_url, "body": body}


def grab_site_info():
    with open('site_url.txt', 'r') as file:
        data = file.read()
    url = data
    callSite = ScrapingApi()
    response = callSite.scrap_site(url, 'p', 'productDetails-status')
    
    return response



def grab_site_info_schedule(sc):
    with open('site_url.txt', 'r') as file:
        data = file.read()
    url = data
    callSite = ScrapingApi()
    response = callSite.scrap_site(url, 'p', 'productDetails-status')

    s.enter(10, 1, grab_site_info_schedule, (sc,))
    
    return response

def run_schedule(dirPath):
    s.enter(1, 1, grab_site_info_schedule, (s,))
    s.run()


if __name__ == "__main__":
    # grab_site_info()
    s.enter(1, 1, run_schedule, (s,))
    s.run()
