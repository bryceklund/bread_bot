import requests
from requests_oauthlib import OAuth1
import os
import base64
from dotenv import load_dotenv
load_dotenv()

def read_image(url):
    response = requests.get(url, stream=True)
    filename = url.split('/')[-1]
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
            f.close()
        file = open(filename, 'rb')
        data = base64.b64encode(file.read())
        os.remove(filename)
    return data

def upload_image(image, oauth):
    endpoint = 'https://upload.twitter.com/1.1/media/upload.json'
    image_bytes = read_image(image)
    post_data = {
        'media_data': image_bytes,
        'media_category': 'tweet_image'
    }
    media_id = requests.post(url=endpoint, data=post_data, auth=oauth)
    return media_id.json()['media_id']


def send_tweet(content):
    client_key = os.getenv("CLIENT_KEY")
    client_secret = os.getenv("CLIENT_SECRET")
    resource_owner_key = os.getenv("OWNER_KEY")
    resource_owner_secret = os.getenv("OWNER_SECRET")

    oauth = OAuth1(client_key,
                    client_secret=client_secret,
                    resource_owner_key=resource_owner_key,
                    resource_owner_secret=resource_owner_secret,
                    signature_type='body')
    if content['image']:
        media_id = upload_image(content['image'], oauth)
    else:
        media_id = ''
    tweet = content['text']
    post_data = {
        'status': tweet,
        'media_ids': media_id
    }

    endpoint = f'https://api.twitter.com/1.1/statuses/update.json'

    response = requests.post(url=endpoint, data=post_data, auth=oauth)

    if not response.ok:
        print(response.json())
    return response.json()