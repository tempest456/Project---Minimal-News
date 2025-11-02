import requests
from bs4 import BeautifulSoup


def scrape_article(url):
    """ Returns the article content of the url provided """     
    response = requests.get(url, headers={'User-agent': 'app'})
    soup = BeautifulSoup(response.content, 'lxml')

    article = soup.find('div', class_='postDetail mainPost')

    paragraphs = article.find_all('p')
    paragraphs.pop()

    article_content = ''
    for paragraph in paragraphs:
        article_content += paragraph.text
        article_content += "\n"

    return article_content
