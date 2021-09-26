import requests
import time
import json
import os
clear = lambda: os.system('cls')

webhook = input('Discord Webhook:')
x = input('Group ID:')
oauth_token = input('OAuth Token:')
timeout = input('Scan Timeout:')
autolike = input('Auto Like?(Y=Yes/N=No)')
if autolike.lower() == "y":
    autolike = bool(True)
else:
    autolike = bool(False)
clear()

lastMessageID = 0
i=0

while i <= 10:
    r = requests.get("https://www.yammer.com/api/v1/messages/in_group/"+ str(x) + ".json", headers={
        'cookie': "oauth_token=" + str(oauth_token)
    })
    response = json.loads(r.content)
    print("Checking...")
    if bool(response["messages"]):
        print("Last message ID: " + str(lastMessageID))
        if lastMessageID != int(response["messages"][0]["id"]) and lastMessageID != 0:
            print("New Message! ID: " + str(response["messages"][0]["id"]))
            discordData = {
                "content": "@everyone",
                "embeds": [{
                    "title": "New Yammer Message:",
                    "description": str(response["messages"][0]["content_excerpt"]),
                    "url": str(response["messages"][0]["web_url"]),
                    "color": 5814783
              }]
            }
            requests.post(webhook, json = discordData)
            if autolike:
                data2={
                    'message_id': int(response["messages"][0]["id"]),
                    'access_token': str(oauth_token)
                    
                }
                r2 = requests.post("https://www.yammer.com/api/v1/messages/liked_by/current.json", data=data2, headers={
                    "authorization": "Bearer " + str(oauth_token)
                })
                print("Auto liked!")
                
        lastMessageID = int(response["messages"][0]["id"])
    else:
        print("No Messages yet!")
    time.sleep(int(timeout))
