import json
import os
import time

import requests
from dotenv import load_dotenv
import random
import string

load_dotenv()

NUMBER_OF_USERS = int(os.getenv('NUMBER_OF_USERS'))
MAX_POST_PER_USER = int(os.getenv('MAX_POST_PER_USER'))
MAX_LIKES_PER_USER = int(os.getenv('MAX_LIKES_PER_USER'))
BASE_URL = os.getenv('BASE_URL')


def create_email():
    return f"{''.join(random.choice(string.ascii_letters) for x in range(8))}@gmail.com"


def create_password():
    temp = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation, 10)
    return "".join(temp)


def get_random_text():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


token_list = []
total_post_list = []


def like_posts(tokens, posts, max_likes_per_user):
    for item in tokens:
        if len(posts) > max_likes_per_user:
            data = random.sample(posts, max_likes_per_user)
        else:
            data = posts
        headers = {'Content-Type': 'application/json',
                   'Authorization': f"Token {item}"}

        requests.post(f"{BASE_URL}/post/bulk_post_like/",
                      data=json.dumps(data), headers=headers)


def create_users_and_posts(number_of_users, number_of_post_per_user):
    for i in range(int(number_of_users)):
        r_user = requests.post(f"{BASE_URL}/register/", data={'email': create_email(), 'password': create_password()})
        token = r_user.json()['auth_token']
        token_list.append(token)
        headers = {'Content-Type': 'application/json',
                   'Authorization': f"Token {token}"}
        r_post = requests.post(f"{BASE_URL}/post/create_post/",
                               data=json.dumps(
                                   [{'title': get_random_text(),
                                     'body': get_random_text()}] * random.randint(1,
                                                                                  number_of_post_per_user)),
                               headers=headers)
        total_post_list.extend([{'post': item['id']} for item in r_post.json()])


time1 = time.time()
create_users_and_posts(NUMBER_OF_USERS, MAX_POST_PER_USER)
like_posts(token_list, total_post_list, MAX_LIKES_PER_USER)
time2 = time.time()

print(f"async function takes {(time2 - time1)} seconds")
