import discord
import asyncio
import shippo
import json
from flask import Flask, request, Response
import threading
import queue 
from time import sleep

auth_tokens = {}
servers = {}
client = discord.Client()  
#Contains tracking numbers as key with values being data such as discord server/channel
tracking_numbers = {}
app = Flask(__name__)
q = queue.Queue()
        
def run_listeners():
    shippo.api_key = auth_tokens["shippo"]

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):
        if message.content.startswith('!track'):
            content = message.content.split(' ')
            tracking_number = content[1]
            tracking_service = content[2]
            await client.send_message(message.channel, tracking_number)
            #possibly uselesss but storing the tracking numbers associated with a server
            if not servers[message.server]:
                #add new list with tracking number in it
                servers[message.server] = [tracking_number,message.channel]
            else:
                servers[message.server].append(tracking_number)
            if not tracking_numbers[tracking_number]:
                tracking_numbers[tracking_number] = [message.channel, "usps"]
            #counter = 0
            #tmp = yield from client.send_message(message.channel, 'Calculating messages...')
            #async for log in client.logs_from(message.channel, limit=100):
                #if log.author == message.author:
                    #counter += 1

            #yield from client.edit_message(tmp, 'You have {} messages.'.format(counter))
        elif message.content.startswith('!status'):
            tracking_number = message.content.split(' ')[1]
            await client.send_message(message.channel, )
        elif message.content.startswith('!quit'):
            await client.send_message(message.channel, "Shutting Down")
            await client.logout()
            await client.close()
    
def get_auth_tokens():
#Hold the Discord and oauth tokens
    with open('token.txt') as f:
            for line in f:
            #auth_tokens = [x.strip().split(':') for x in f.readlines()]
                (key, val) = line.strip().split(':')
                auth_tokens[key] = val


@app.route('/',methods=['POST'])
def get_webhook():
    if request.method == 'POST':
        content = request.get_json()
        if content is not None:
            print(content)
    return 'OK'
    
def register_webhook(carrier_token,tracking_number):
    webhook_response = shippo.Track.create(
                                        carrier=carrier_token, 
                                        tracking=tracking_number, 
                                    )
def run_discord():
    print("Starting thread 1")
    run_listeners() 
    print(auth_tokens)
    print(auth_tokens["discord"]) 
    client.run(auth_tokens["discord"])
def run_weblistener():
    app.run(host='0.0.0.0', port=80)
def main():
    get_auth_tokens()
    disco_thread = threading.Thread(target=run_weblistener) 
    disco_thread.daemon = True
    disco_thread.start()
    run_discord()
main()
    
