import requests
from requests_oauthlib import OAuth1
import os
import base64

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
    client_key = '6rhsZNtLGRxhvRWjuRaxf64Es'
    client_secret = 'uGySvEtJGtAb4u8WwLko26f60KqqR4jaAfxP7db1quQIJa2IJt'
    resource_owner_key = '83966663-PFtqUiGvkDwww5lnEGvxfMRUZvazUrz3ucyoMfZ4r'
    resource_owner_secret = '0v31hTygZXckCj1Vf8BsS4DgtArZsEcOZxNg7jmL9zLC5'

    oauth = OAuth1(client_key,
                    client_secret=client_secret,
                    resource_owner_key=resource_owner_key,
                    resource_owner_secret=resource_owner_secret,
                    signature_type='body')
    media_id = upload_image(content['image'], oauth)
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

test_tweet = {
    'text': 'test\ntweet 2',
    'image': "https://upload.wikimedia.org/wikipedia/commons/4/44/Ttongppang%28Poo_Bun%2C_%EB%98%A5%EB%B9%B5%29_%287399937534%29.jpg"
}

send_tweet(test_tweet)