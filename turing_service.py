#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests

USER_ID = ''
API_KEY = ''
TOKEN = ''

def gen_text_data(text):
  data = {
    'reqType': 0,
    'perception': {
      'inputText': {
        'text': text
      }
    },
    'userInfo': {
      'apiKey': API_KEY,
      'userId': USER_ID
    }
  }

  return json.dumps(data, ensure_ascii=False)

def http_post(data):
  resp = requests.post('http://openapi.tuling123.com/openapi/api/v2', data=data.encode('utf-8').decode('latin1'))

  return { 'status_code': resp.status_code, 'resp_data': json.loads(resp.text, encoding='utf-8') }

