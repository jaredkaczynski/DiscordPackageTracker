import discord
import asyncio

#Hold the Discord and oauth tokens
with open('token.txt') as f:
        auth_tokens = [x.strip() for x in f.readlines()]

client = discord.Client()

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
        #counter = 0
        #tmp = yield from client.send_message(message.channel, 'Calculating messages...')
        #async for log in client.logs_from(message.channel, limit=100):
            #if log.author == message.author:
                #counter += 1

        #yield from client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!status'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run(auth_tokens[0])

