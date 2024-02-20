import asyncio
import random
import string
import json
import re
from discord.ext import commands, tasks

token = ""
ownerid = 822830992426926172

with open('pokemon', 'r', encoding='utf8') as file:
    pokemon_list = file.read()

client = commands.Bot(command_prefix='$')
client.remove_command('help')

captcha = True

def solve(message):
    hint = [char for i, char in enumerate(message[15:-1]) if char != "\\"]
    hint_string = "".join(hint)
    hint_replaced = hint_string.replace("_", ".")
    solution = re.findall("^" + hint_replaced + "$", pokemon_list, re.MULTILINE)
    return solution

@client.event
async def on_ready():

@client.event
async def on_message(message):
    global captcha

    if message.author.id == 854233015475109888 and not message.embeds:
        content = message.content.lower().strip()
        if content.count(':') == 1:
            name, percentage = content.split(':')
            name = name.strip()
            percentage = percentage.strip()
            if percentage.endswith('%'):
                if captcha:
                    await asyncio.sleep(random.randint(1, 3))
                    channel = message.channel
                    await channel.send(f'<@716390085896962058> c {name}')

    if message.author.id == ownerid and message.content.startswith('$'):
        await client.process_commands(message)

    if message.author.id == 716390085896962058:
        content = message.content

        if 'The pokÃ©mon is ' in content:
            if not len(solve(content)):
                print('Pokemon not found.')
            else:
                for i in solve(content):
                    if captcha:
                        await asyncio.sleep(random.randint(1, 3))
                        channel = message.channel
                        name = i.lower()
                        await channel.send(f'<@716390085896962058> c {name}')

        if 'That is the wrong pokÃ©mon!' in content and captcha:
            await asyncio.sleep(random.randint(1, 3))
            channel = message.channel
            await channel.send(f'<@716390085896962058> h')

        elif 'human' in content:
            captcha = False
            owner = client.get_user(ownerid)
            await owner.send(f"<@{ownerid}> Please verify the Poketwo captcha asap!\n https://verify.poketwo.net/captcha/{client.user.id}")

@client.command()
async def start(ctx):
    global captcha
    if ctx.author.id == ownerid:
        captcha = True
        await ctx.send("Successfully started")

@client.command()
async def say(ctx, *, message):
    if ctx.author.id == ownerid:
        mention_user = '<@716390085896962058>'
        await ctx.send(f'{mention_user} {message}')

client.run(token)
