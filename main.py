from bs4 import BeautifulSoup
from fake_headers import Headers
import lxml
import requests
import json
import unicodedata

def get_headers():
    return Headers(browser="firefox", os="win").generate()

def get_html(url):
    src = requests.get(url, headers=get_headers()).text
    return src

def get_information():
    link_dict = {}
    count_key = 1
    for i in range(0,10):
        url = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={i}'
        soup = BeautifulSoup(get_html(url), 'lxml')
        pages = soup.find_all('a', class_="serp-item__title")
        for page in pages:
            link = page.get('href')
            link_dict[count_key] = link
            count_key += 1
    with open("all_proffessions_link.json", 'w', encoding='utf-8') as f:
        json.dump(link_dict, f, indent=4, ensure_ascii=False)

def pages_loader(file):
    get_information()
    with open(file, 'r', encoding='utf-8') as f:
        pages = json.load(f)
    result_list = []
    for page in pages.values():
        result = {}
        result['link'] = page
        html_page = get_html(page)
        soup = BeautifulSoup(html_page, 'lxml')
        if soup.find(attrs={'data-qa':'vacancy-salary'}) is not None:
            salary = soup.find(attrs={'data-qa':'vacancy-salary'}).text
        else:
            salary = 'Нет данных'
        result['salary'] = unicodedata.normalize("NFKD",salary)
        company_name = soup.find('span', class_="vacancy-company-name").text
        result['company_name'] = unicodedata.normalize("NFKD",company_name)
        if soup.find(attrs={'data-qa':'vacancy-view-raw-address'}) is not None:
            address = soup.find(attrs={'data-qa':'vacancy-view-raw-address'}).text
        else:
            address = soup.find(attrs={'data-qa':'vacancy-view-location'}).text
        result['address'] = unicodedata.normalize("NFKD",address)
        description = soup.find(attrs={'data-qa':'vacancy-description'}).text
        if "Django" in description and "Flask" in description:
            result_list.append(result)
    return result_list

def result_json_file(result_list):
    with open('result_vacancy.json', 'w', encoding='utf-8') as f:
        json.dump(result_list, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    result_json_file(pages_loader("all_proffessions_link.json"))
    
