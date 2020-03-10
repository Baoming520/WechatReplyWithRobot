#!/usr/bin/python
# -*- coding: utf-8 -*-
from turing_service import gen_text_data, http_post

import itchat
import json

# Read config file
with open('./config.json', 'r', encoding='utf-8') as f:
  config = json.load(f)

def get_nicknames(chat_list):
  ret = []
  for elem in chat_list:
    ret.append(elem['nickname'])
  return ret

def update_contacts(itchat):
  # This method SHOULD be executed after login
  friends = [
    {
      'username': f['UserName'], 
      'nickname': f['NickName'], 
      'remarkname': f['RemarkName'],
      'sex': f['Sex'],
      'city': f['City']
    } for f in itchat.get_friends()]
  chatrooms = [
    {
      'encry_chatroom_id': r['EncryChatRoomId'],
      'username': r['UserName'],
      'nickname': r['NickName'],
      'remarkname': r['RemarkName'],
      'members': [ {'nickname': m['NickName'] } for m in itchat.update_chatroom(r['UserName'])['MemberList'] ]
    } for r in itchat.get_chatrooms(update=True)]
  contacts = {
    'friends': friends,
    'chatrooms': chatrooms
  }

  data = json.dumps(contacts, ensure_ascii=False)
  with open(config['contacts_storage_file'], 'w+', encoding='utf-8') as f:
    f.write(data)

def login_callback():
  print('Login')

def logout_callback():
  print('Logout')

@itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
def reply_text(msg):
  # Program does not handle the situation that there are multiple nicknames.
  from_nickname = msg['User']['NickName']
  from_username = msg['User']['UserName']
  from_message = msg['Text']
  print('Send from {}: {}'.format(from_nickname, from_message))
  if from_nickname in get_nicknames(config['chat_with']):
    msg_data = gen_text_data(from_message)
    resp = http_post(msg_data)
    to_message = resp['resp_data']['results'][0]['values']['text']
    print('Send to {}: {}'.format(from_nickname, to_message))
    return to_message

def main(argv=None):
  # Login
  itchat.auto_login(hotReload=True, statusStorageDir=config['status_storage_file'], enableCmdQR=True, loginCallback=login_callback, exitCallback=logout_callback)
  friends = itchat.get_friends()
  chatrooms = itchat.get_chatrooms()
  # itchat.send_msg(msg='Hello', toUserName='filehelper')
  
  if config['update_contacts']:
    update_contacts(itchat)
  
  itchat.run()
  # itchat.logout()
  pass

if __name__ == '__main__':
  main()