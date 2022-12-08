import requests
import codecs
from bs4 import BeautifulSoup as Bs
from random import randint

__all__ = ('hh', "rabota", 'superjob')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def hh(url):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'serp-item'})
                for div in div_lst:
                    header = div.find('h3')
                    title = header.span.a.text
                    href = header.a['href']
                    content = div.find('div', attrs={'class': 'g-user-content'}).text
                    company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text
                    jobs.append({'title': title, 'url': href,
                                 'description': content, 'company': company})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def rabota(url):
    jobs = []
    errors = []
    domain = 'https://kazan.rabota.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'r-serp'})
            if main_div:
                article_lst = main_div.find_all('article', attrs={'data-key': True})
                for article in article_lst:
                    header = article.find('h3')
                    title = header.text
                    href = header.a['href']
                    content = article.find('div', attrs={'class': 'vacancy-preview-card__short-description'}).text
                    company = article.find('span', attrs={'class': 'vacancy-preview-card__company-name'}).text
                    jobs.append({'title': title,
                                 'url': domain + href,
                                 'description': content,
                                 'company': company})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def superjob(url):
    jobs = []
    errors = []
    domain = 'https://kazan.superjob.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            main_div = soup.find('div',  attrs={'class': '_2dEhr _2qHsY _1oWry'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'f-test-search-result-item'})
                for div in div_lst:
                    header = div.find('span', attrs={'class': 'ALb1p _2itH9 _2R-HM _3i61M _2BeAM x_rU7 _1vJ_t DSYVK'})
                    if not header:
                        continue
                    title = header.text
                    href = header.a['href']
                    content = div.find('span', attrs={'class': '_3camv x_rU7 _1vJ_t _2myJ9 _1zaXV'}).text
                    company = div.find('span', attrs={'class': 'f-test-text-vacancy-item-company-name'}).text
                    jobs.append({'title': title, 'url': domain + href,
                                 'description': content, 'company': company})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://kazan.superjob.ru/vacancy/search/?without_agencies=1&keywords=Python'
    jobs, errors = superjob(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs) + '\n')
    h.write(str(errors))
    h.close()
