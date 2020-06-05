import requests
from bs4 import BeautifulSoup
from secrets import username, password
import sys

class Facebook_scraper():
    login_basic_url = 'https://mbasic.facebook.com/login'
    login_mobile_url = 'https://m.facebook.com/login'
    payload = {
            'email': username,
            'pass': password
        }
    post_ID = ""

    def parse_html(self, request_url):
        with requests.Session() as session:
            post = session.post(self.login_basic_url, data=self.payload)
            parsed_html = session.get(request_url)
        return parsed_html

    def post_content(self):
        REQUEST_URL = f'https://mbasic.facebook.com/story.php?story_fbid={self.post_ID}&id=415518858611168'
        
        soup = BeautifulSoup(self.parse_html(REQUEST_URL).content, "html.parser")
        content = soup.find_all('p')
        post_content = []
        for lines in content:
            post_content.append(lines.text)
        
        post_content = ' '.join(post_content)
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        post_content = post_content.translate(non_bmp_map)
        return post_content

    def date_posted(self):
        REQUEST_URL = f'https://mbasic.facebook.com/story.php?story_fbid={self.post_ID}&id=415518858611168'
        
        soup = BeautifulSoup(self.parse_html(REQUEST_URL).content, "html.parser")
        date_posted = soup.find('abbr')
        return date_posted.text

    def post_likes(self):
        limit = 200
        REQUEST_URL = f'https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit={limit}&total_count=17&ft_ent_identifier={self.post_ID}'

        soup = BeautifulSoup(self.parse_html(REQUEST_URL).content, "html.parser")
        names = soup.find_all('h3')
        people_who_liked = []
        for name in names:
            people_who_liked.append(name.text)
        people_who_liked = [i for i in people_who_liked if i] 
        return people_who_liked

    def post_shares(self):        
        REQUEST_URL = f'https://m.facebook.com/browse/shares?id={self.post_ID}'
        
        with requests.Session() as session:
            post = session.post(self.login_mobile_url, data=self.payload)
            parsed_html = session.get(REQUEST_URL)
        
        soup = BeautifulSoup(parsed_html.content, "html.parser")
        names = soup.find_all('span')
        people_who_shared = []
        for name in names:
            people_who_shared.append(name.text)
        return people_who_shared
    def post_comments(self):
        REQUEST_URL = f'https://mbasic.facebook.com/story.php?story_fbid={self.post_ID}&id=415518858611168'
        
        soup = BeautifulSoup(self.parse_html(REQUEST_URL).content, "html.parser")
        content = soup.find_all('div',class_='ek')
        return content
        
if __name__=='__main__':
    scraper = Facebook_scraper()
    scraper.post_ID = input("Enter the post ID: ")
    #print(scraper.post_content())
    #print(scraper.post_likes())
    print(scraper.post_comments())    
        

