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
    try:
        media_id = requests.post(url=endpoint, data=post_data, auth=oauth)
        return media_id.json()['media_id']
    except:
        return -1


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

    tweet = content['text']

    if content['image']:
        try:
            media_id = upload_image(content['image'], oauth) 
            post_data = {
                'status': tweet,
                'media_ids': media_id
            }
        except:
            print('failed to grab media_id, returning false')
            return False
    else:
        post_data = {
            'status': tweet
        }

    endpoint = f'https://api.twitter.com/1.1/statuses/update.json'

    print('tweet built. attemping to send...')
    response = requests.post(url=endpoint, data=post_data, auth=oauth)

    if not response.ok:
        print('API call failed: ', response.json())
        return False
    else:
        print('bread twote!')
    return True