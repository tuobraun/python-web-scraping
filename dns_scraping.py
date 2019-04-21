""" import requests
import lxml.html

url = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p=1&i=1&mode=list&f[mv]=bnf3-3gdlm-boxh-c8er-ddz9&f[mx]=2f6-2ff-2fi'
r = requests.get(url)
with open('test.html', 'wb') as output_file:
    output_file.write(r.text.encode('UTF-8'))
 """
#https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p=1&i=1&mode=list&f[mv]=bnf3-3gdlm-boxh-c8er-ddz9&f[mx]=2f6-2ff-2fi

import requests
import lxml.html
page = 1
url = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p='
filters = '&f[mv]=bnf3-3gdlm-boxh-c8er-ddz9&f[mx]=2f6-2ff-2fi' # GTX 1050Ti - GTX 1080, RAM: 4 - 8 GB
combined_url = requests.get(url+str(page)+filters)
doc = lxml.html.fromstring(combined_url.content)
prod_list = doc.xpath('//div[@class="catalog-items-list view-list"]')[0]
link = prod_list.xpath('.//div[@class="title"]/a/@href')
title = prod_list.xpath('.//h3/text()')
price = prod_list.xpath('.//div[@class="price_g"]/span/text()')

print ("Модель\t\t\t\t\t\t\t\tЦена")
for t, p in zip(title, price):
    print (t + '\t' + p)

l = len(title)
print(">>>Items per page: " + str(l))
