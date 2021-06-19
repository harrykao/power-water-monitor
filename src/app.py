#!/usr/bin/env python3

import json
import os
import requests

r = requests.post(
    'https://api.rainforestcloud.com/rest/auth/accesskey',
    json.dumps({
      "login": os.environ['RAINFOREST_USERNAME'],
      "password": os.environ['RAINFOREST_PASSWORD'],
    }))

print(r.json())
