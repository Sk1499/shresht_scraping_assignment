from bs4 import BeautifulSoup as bs
from validation import product
from utils import get_soup
import traceback, json
from requests_html import HTMLSession


def ff_scraper(url):
    try:
        soup = get_soup(url)
        desc = soup.find("meta", {"name": "description"})
        brand_desc = desc['content']
        name = soup.find("meta",{"property": "og:site_name"})
        brand_name = name['content']
        sitenav = soup.find('ul',{'id':'SiteNav'})
        products = []
        for i in sitenav.findAll('li'):
            category = i.find('a')
            cat_soup = get_soup(url + category['href'])
            prod_list = cat_soup('div',{'class':'grid-view-item product-card'})
            for k in prod_list:
                link = k.find('a')
                products.append(link['href'])
            try:
                pagination = cat_soup.find('li',{'class':'pagination__text'}).contents[0].split(' ')[-3]
                for j in range(2 , int(pagination)+1):
                    cat_soup = get_soup(url + category['href'] + '?page=' + str(j))
                    prod_list = cat_soup('div',{'class':'grid-view-item product-card'})
                    for k in prod_list:
                        link = k.find('a')
                        products.append(link['href'])
            except Exception as msg:
                print('No pagination')
        print('total products - ', len(products))
        prod_data = []
        for i in products:
            soup = get_soup(url + i)
            prod_json = soup.find('script',{'id':'ProductJson-product-template'}).contents[0]
            prod_json = json.loads(prod_json)    
            variant_list = []
            for j in prod_json['variants']:
                variant_json = j 
                validation_object = product(variant_json['id'],prod_json['featured_image'],float(str(prod_json['price'])[:-2]),variant_json['title'])
                variant = {
                    "id":variant_json['id'],
                    "variant_title":variant_json['title'],
                    "price":float(str(prod_json['price'])[:-2]),
                    "image":prod_json['featured_image']
                }
                variant_list.append(variant)
            output = {
                "brand":brand_name,
                "description":brand_desc,
                "image":prod_json['featured_image'],
                "models":[{"color":"","variants":variant_list}],
                "price":float(str(prod_json['price'])[:-2]),
                "sale_price":float(str(prod_json['price'])[:-2]),
                "title":prod_json['title'],
                "product_id":prod_json['handle'],
                "url":url + i
            }
            prod_data.append(output)
    except Exception as msg:
        print(str(msg))
        print(traceback.print_exc())
    return prod_data

def lc_scraper(url):
    try:
        soup = get_soup(url)
        brand = soup.find('title')
        brand_name = brand.contents[0]
        desc = soup.find("meta", {"name": "description"})
        brand_desc = desc['content']
        sitenav = soup.find('ul',{'id':'submenu_31'})
        products = []
        for i in sitenav.findAll('li'):
            category = i.find('a')
            cat_soup = get_soup(category['href'])
            prod_list = cat_soup('div',{'class':'productMiniature js-product-miniature'})
            for k in prod_list:
                link = k.find('a')
                products.append(link['href'])
        print('total products - ', len(products))
        prod_data = []
        for i in products:
            print('---------')
            print(i)
            soup = get_soup(i)
            try:
                prod_json = soup.find('script',{'class':'single-product-data-ga4'}).contents[0]
            except:
                print('Not a product page')
                continue
            img = soup.find('li',{'class':'productImages__item keen-slider__slide'})
            image = img.find('a')['href']
            prod_json = json.loads(prod_json)
            validation_object = product(prod_json['item_id'],image,float(prod_json['price']),prod_json['item_name'])
            output = {
                "brand":brand_name,
                "description":brand_desc,
                "image":image,
                "price":float(prod_json['price']),
                "sale_price":float(prod_json['price']),
                "title":prod_json['item_name'],
                "product_id":prod_json['item_id'],
                "url":i
            }
            prod_data.append(output)
    except Exception as msg:
        print(str(msg))
        print(traceback.print_exc())
    return prod_data

def tj_scraper(url):
    try:
        prod_page_url = url + '/home/products/category/products'
        session = HTMLSession()
        r = session.get(prod_page_url)
        r.html.render(sleep=5)
        soup = bs(r.html.raw_html, "html.parser")
        brand_name = "Trader Joe's"
        sitenav = soup.find('ul',{'class':'CategoryFilter_categoryFilter__list__2NBce'})
        products = []
        for i in sitenav:
            category = i.find('a')
            f = session.get(url + category['href'])
            f.html.render(sleep=5)
            cat_soup = bs(f.html.raw_html, "html.parser")
            prod_list = cat_soup.findAll('li',{'class':'ProductList_productList__item__1EIvq'})
            for k in prod_list:
                link = k.find('a')
                products.append(link['href'])
            ul = cat_soup.find('ul',{'class':'Pagination_pagination__list__1JUIg'}) 
            li_list = ul.findAll('li')
            total_pages = li_list[-1]['aria-label']
            total_pages = total_pages.split(',')[0].split(' ')[-1]
            for j in range(2,int(total_pages)):
                try:
                    page_url = url + category['href'] + '?filters=%7B"page"%3A'+ str(j) +'%7D'
                    f = session.get(page_url)
                    f.html.render(sleep=5)
                    cat_soup = bs(f.html.raw_html, "html.parser")
                    prod_list = cat_soup.findAll('li',{'class':'ProductList_productList__item__1EIvq'})
                    for k in prod_list:
                        link = k.find('a')
                        products.append(link['href'])
                except:
                    continue
        print(products)
        print(len(products))
        prod_data = []
        for i in products:
            try:
                prod_page_url = url + i
                print(prod_page_url)
                prod_id = i.split('-')[-1]
                r = session.get(prod_page_url)
                r.html.render(sleep=5)
                soup = bs(r.html.raw_html, "html.parser")
                image = soup.find('picture',{'class':'HeroImage_heroImage__image__1O61B Carousel_heroImage__33Rxb'})
                image = image.find('img')['src']
                image = url + image
                title = soup.find('h1',{'class':'ProductDetails_main__title__14Cnm'}).contents[0]
                price = soup.find('span',{'class':'ProductPrice_productPrice__price__3-50j'}).contents[0].split('$')[-1]
                validation_object = product(prod_id,image,float(price),title)
                output = {
                    "brand":brand_name,
                    "image":image,
                    "price":float(price),
                    "sale_price":float(price),
                    "title":title,
                    "product_id":prod_id,
                    "url":prod_page_url
                }
                print(output)
                print('---------------------')
                prod_data.append(output)
            except:
                continue
    except Exception as msg:
        print(str(msg))
        print(traceback.print_exc())
    return prod_data




