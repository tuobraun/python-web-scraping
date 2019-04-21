""" import requests
import lxml.html

url = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p=1&i=1&mode=list&f[mv]=bnf3-3gdlm-boxh-c8er-ddz9&f[mx]=2f6-2ff-2fi'
r = requests.get(url)
with open('test.html', 'wb') as output_file:
    output_file.write(r.text.encode('UTF-8'))
 """
import requests
import lxml.html
page = 1
url = 'https://www.citilink.ru/catalog/computers_and_notebooks/parts/videocards/'
filters = '&sorting=price_asc&f=9368_29nVidiad1d1GeForced1GTXd11050TI,9368_29nVidiad1d1GeForced1GTXd11060,9368_29nVidiad1d1GeForced1GTXd11070,9368_29nVidiad1d1GeForced1GTXd11070Ti,9368_29nVidiad1d1GeForced1GTXd11080,304_294d1gb,304_296d1gb,304_298d1gb'
combined_url = requests.get(url+str(page)+filters)
doc = lxml.html.fromstring(combined_url.content)
prod_list = doc.xpath('//div[@class="product_category_list"]')[0]
link = prod_list.xpath('.//a[@class="link_gtm-js link_pageevents-js ddl_product_link"]/@href')
title = prod_list.xpath('.//a[@class="link_gtm-js link_pageevents-js ddl_product_link"]/@title')

price = prod_list.xpath('.//span[@class="subcategory-product-item__price subcategory-product-item__price_special"]/ins[@class="subcategory-product-item__price-num"]/text()')
#price = price.replace("\s+", "")

print ("Модель\t\t\t\t\t\t\t\tЦена")
for t, p in zip(title, price):
    print (t + '\t' + p)

l = len(title)
print(">>>Items per page: " + str(l))