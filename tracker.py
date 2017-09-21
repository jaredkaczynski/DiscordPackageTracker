import discord
import asyncio
import shippo

auth_tokens = {}
servers = {}
client = discord.Client()   
        
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
            tracking_number = message.content.split(' ')[1]
            await client.send_message(message.channel, tracking_number)
            if not servers[message.server]:
                #add new list with tracking number in it
                servers[message.server] = [tracking_number]
            else:
                servers[message.server].append(tracking_number)
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
def run_bot():
    print(auth_tokens)
    print(auth_tokens["discord"])
    client.run(auth_tokens["discord"])
def main():
    get_auth_tokens()
    run_listeners()
    run_bot()
main()
    
