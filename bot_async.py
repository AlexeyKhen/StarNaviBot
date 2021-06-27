import json
import os
import asyncio
import time

import aiohttp
from dotenv import load_dotenv
import random
import string

load_dotenv()

NUMBER_OF_USERS = int(os.getenv('NUMBER_OF_USERS'))
MAX_POST_PER_USER = int(os.getenv('MAX_POST_PER_USER'))
MAX_LIKES_PER_USER = int(os.getenv('MAX_LIKES_PER_USER'))
BASE_URL = os.getenv('BASE_URL')
token_list = []
total_post_list = []


def create_email():
    return f"{''.join(random.choice(string.ascii_letters) for x in range(8))}@gmail.com"


def create_password():
    temp = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation, 10)
    return "".join(temp)


def get_random_text():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


async def creat_user_and_posts(session, number_of_post_per_user):
    response_for_user = await session.post(f"{BASE_URL}/register/",
                                           data={'email': create_email(), 'password': create_password()})
    data = await response_for_user.json()
    token = data['auth_token']
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Token {token}"}

    response_for_posts = await session.post(f"{BASE_URL}/post/create_post/",
                                            data=json.dumps(
                                                [{'title': get_random_text(),
                                                  'body': get_random_text()}] * random.randint(1,
                                                                                               number_of_post_per_user)),
                                            headers=headers)
    new_data = await response_for_posts.json()

    return token, [{'post': item['id']} for item in new_data]


async def main(number_of_users, max_post_per_user, max_likes_per_user):
    async with aiohttp.ClientSession() as session:
        tasks = []
        tasks_like = []
        for i in range(number_of_users):
            tasks.append(creat_user_and_posts(session, max_post_per_user))
        responses = await asyncio.gather(*tasks)
        for token, post_list in responses:
            token_list.append(token)
            total_post_list.extend(post_list)
        for item in token_list:
            if len(total_post_list) > max_likes_per_user:
                data = random.sample(total_post_list, max_likes_per_user)
            else:
                data = total_post_list
            headers = {'Content-Type': 'application/json',
                       'Authorization': f"Token {item}"}
            tasks_like.append(session.post(f"{BASE_URL}/post/bulk_post_like/",
                                           data=json.dumps(data), headers=headers))
        await asyncio.gather(*tasks_like)


time1 = time.time()
asyncio.run(main(NUMBER_OF_USERS, MAX_POST_PER_USER, MAX_LIKES_PER_USER))
time2 = time.time()

print(f"async function takes {(time2 - time1)} seconds")
