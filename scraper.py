import requests
import string
from bs4 import BeautifulSoup
import os

page_no = int(input())
category_input = input()

while page_no >= 1:

    directory = 'Page_' + str(page_no)
    os.mkdir(directory)

    link = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=" + str(page_no)

    page = requests.get(link)
    print(page.status_code)
    soup = BeautifulSoup(page.text, 'html.parser')

    articles = soup.find_all('article')

    for article in articles:

        category = article.find('span', class_="c-meta__type").text

        if category == category_input:

            article_title = article.find('a').text

            article_link = "https://www.nature.com" + article.find('a').get('href')

            article_page = requests.get(article_link)
            soup = BeautifulSoup(article_page.text, 'html.parser')
            content_article = soup.find('article').find('div', class_='c-article-body u-clearfix').text

            article_title_list = article_title.split()

            for index, word in enumerate(article_title_list):
                for punctuation in string.punctuation:
                    if punctuation in word:
                        new_word = word.replace(punctuation, '')
                        article_title_list[index] = new_word

            final_article = directory + "/" + "_".join(article_title_list) + ".txt"

            file = open(final_article, "w", encoding='utf-8')
            file.writelines(content_article)
            file.close()

    page_no -= 1
