from bs4 import BeautifulSoup
import requests

path = r"C:\Users\Bingz\Desktop\1_2_homework_required\index.html"
with open(path, 'r') as web_data:
    Soup = BeautifulSoup(web_data.read(), 'lxml') #使用BeautifulSoup解析网页并创建一个soup对象
    pics = Soup.select('body > div > div > div.col-md-9 > div > div > div > img') #获取指定元素列表
    prices = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    titles = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
    ratings = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
    stars = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')
    #print(pics, prices, titles, ratings,stars)

    for pic, price, title, rating, star in zip(pics, prices, titles, ratings, stars): #zip()函数将各个列表打包成一个元组列表
        info = {
            'pic': pic.get('src'), #get函数获取指定标签内容
            'price' : price.get_text(),
            'title' : title.get_text(),
            'rating' : rating.get_text(),
            'star' : len(star.find_all("span", class_='glyphicon glyphicon-star'))
        }
        print(info)

