import requests
import lxml.html as html
import os
import datetime

HOME_URL= 'https://www.paginasiete.bo/noticias/buscar/?buscar=feminicidio&p=1'
URL_PAGINA_SIETE='https://www.paginasiete.bo'
XPATH_LINK_TO_ARTICLE = '//h5[@class="titulo"]/a/@href'
XPATH_TITLE = '//h1[@class="titular"]/text()'
XPATH_SUMMARY = '//strong[@class="bajada"]/text()'
XPATH_BODY = '//div[@class="cuerpo-nota"]/p[not(@class)]/text()'


def parser_notices(link,today):
    try:
        link=URL_PAGINA_SIETE+link
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content#.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                summary =  parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n\n')

        else:
            raise ValueError(f'Error:{response.status_code}')    
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home= response.content#.decode('latin-1')
            parsed = html.fromstring(home)
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)
            today=datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices:
                parser_notices(link,today)

        else:
            raise ValueError(f'Error:{response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == "__main__":
    run()