"""
Copyright 2021 Carnegie Mellon University. All Rights Reserved.
Released under a MIT (SEI)-style license. See LICENSE.md in the project root for license information.
"""
import requests
import threading
import time


THREADS = 200
REQ_PER_THREAD = 100


def request_thread(token):
    headers = {'Authorization': f'Bearer {token}'}
    for i in range(REQ_PER_THREAD):
        r = requests.post('http://localhost:5000/api/Welder%20Test%20View', headers=headers)
        if r.status_code != 200:
            print(f'Got code {r.status_code}')


def main():
    token_data = {
        'grant_type': 'password',
        'username': '',
        'password': '',
        'scope': 's3',
    }

    token_response = requests.post(
        'http://localhost:10000/connect/token',
        data=token_data,
        auth=('welder', 'a')
    )
    if not token_response.status_code == 200:
        raise Exception('Got a bad token response.')
    else:
        print(token_response.json())

    token = token_response.json()['access_token']

    start = time.time()
    pool = []
    for i in range(THREADS):
        t = threading.Thread(target=request_thread, args=(token,))
        t.start()
        pool.append(t)

    for t in pool:
        t.join()

    print(f'With {THREADS} threads and {REQ_PER_THREAD} requests per thread, took {time.time() - start}')


if __name__ == '__main__':
    main()

