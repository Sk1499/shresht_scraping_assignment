import json
from bs4 import BeautifulSoup as bs
from scrapers import ff_scraper , lc_scraper , tj_scraper

URL_list = ['https://foreignfortune.com/','https://www.lechocolat-alainducasse.com/uk/','https://www.traderjoes.com']
# data = []
for i in URL_list:
    if 'foreignfortune' in i:
        output = ff_scraper(i)
        with open('final_output_ff.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
    elif 'lechocolat' in i:
        output = lc_scraper(i)
        with open('final_output_lc.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
    if 'traderjoes' in i:
        output = tj_scraper(i)
        with open('final_output_tj.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
    
    

