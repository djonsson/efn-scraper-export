__author__ = 'danieljonsson'

import requests
from bs4 import BeautifulSoup
import json


def find_video_objects():
    base = 'http://www.efn.se/'
    api = base + 'api/playerconf?post_id='

    for num in range(1000, 2000):
        api_request = api + str(num)
        response = requests.get(api_request)

        try:
            json_object = response.json()

            streams = json_object['streams']
            slug = json_object['slug']
            image = json_object['image']
            caption_url = json_object['caption_url']

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

            data = {'caption_url': caption_url, 'api_url': api_request, 'streams': streams, 'image': image,
                    'slug': slug, 'video_name': video_name, 'datetime': datetime, 'description': description}
            json_object = json.dumps(data)

            print json_object
            f = open('export.log', 'a')
            f.write(json_object + '\n')
            f.close()

        except KeyError:
            print "Miss on: " + api_request
        except ValueError:
            print "No content on: " + api_request
        except AttributeError:
            print "Attribute error on: " + api_request

find_video_objects()
