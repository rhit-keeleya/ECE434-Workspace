#!/usr/bin/env python3

import requests

ngrok_page = "http://localhost:4040/api/tunnels"

def get_tunnel():
    result = requests.get(ngrok_page)
    if(result.status_code==200):
        return result.json()['tunnels'][0]['public_url']
    else:
        print("!failed request!")

if __name__ == '__main__':
    #executed as script
    print(get_tunnel())
