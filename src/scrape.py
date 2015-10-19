__author__ = 'danieljonsson'

import requests
from bs4 import BeautifulSoup
import json


def findVideos():
    base = 'http://www.efn.se/'
    api = base + 'api/playerconf?post_id='

    for num in range(350, 5000):
        api_request = api + str(num)
        response = requests.get(api_request)

        try:
            jsonObject = response.json()

            video_file = jsonObject['streams']['ipad']
            slug = jsonObject['slug']
            image = jsonObject['image']

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

            data = {}
            data['apiurl'] = api_request
            data['video'] = video_file
            data['image'] = image
            data['slug'] = slug
            data['video_name'] = video_name
            data['datetime'] = datetime
            data['description'] = description
            jsondata = json.dumps(data)
            print jsondata
            f = open('export.log', 'a')
            f.write(jsondata + '\n')
            f.close()

        except KeyError:
            print "Miss on: " + api_request
        except ValueError:
            print "No content on: " + api_request
        except AttributeError:
            print "Attribute error on: " + api_request

findVideos()