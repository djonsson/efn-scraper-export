__author__ = 'danieljonsson'

import requests
from bs4 import BeautifulSoup

def findVideos():
    base = 'http://www.efn.se/'
    api = base + 'api/playerconf?post_id='

    for num in range(15000, 18920):
        response = requests.get(api + str(num))

        try:
            jsonObject = response.json()

            video_file = jsonObject['streams']['ipad']
            slug = jsonObject['slug']
            image = jsonObject['image']

            print api + str(num)

            html = requests.get(base + slug)
            soup = BeautifulSoup(html.content, 'html.parser')

            video_name = soup.find(attrs={'class': 'module-video__title'}).string
            text_inner = soup.find('div', {'class': 'toggle-text__text-inner'})

            description_text = text_inner.findAll('p')
            description = ''
            for i in description_text:
                description += i.text + '\n'

            video_meta_list = soup.find(attrs={'class': 'module-video__meta-list'})
            for i in video_meta_list.findAll('time'):
                if i.has_attr('datetime'):
                    datetime = i['datetime']

            print video_file
            print base + image
            print slug
            print video_name
            print datetime
            print description


        except KeyError:
            print "Miss on: " + str(num)
        except ValueError:
            print "No content on: " + str(num)

findVideos()