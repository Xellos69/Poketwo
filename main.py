import asyncio
import random
import re
import requests
import time
from discord.ext import commands
from termcolor import colored

token = "
ownerid = 822830992426926172

client = commands.Bot(command_prefix='$')
client.remove_command('help')

captcha = True
shiny = 0
legendary = 0
num_pokemon = 0
mythical = 0
pokemon_list = ""

def solve(message):
    hint = [char for i, char in enumerate(message[15:-1]) if char != "\\"]
    hint_string = "".join(hint)
    hint_replaced = hint_string.replace("_", ".")
    solution = re.findall("^" + hint_replaced + "$", pokemon_list, re.MULTILINE)
    return solution

def LoadPokemons():
    global pokemon_list
    print('Loading Pokémon list..')
    try:
        url = 'https://raw.githubusercontent.com/Xellos69/catcher/main/pokemon'
        pokemons = requests.get(url)
        with open('data/pokemon', 'w', encoding='utf8') as PokemonList:
            PokemonList.write(pokemons.text)
            print('Pokémon list updated.')
    except Exception as e:
        print(f'Error updating Pokémon list: {e}')

    with open('data/pokemon', 'r', encoding='utf8') as file:
        pokemon_list = file.read()

@client.event
async def on_ready():
    LoadPokemons()
    print(colored(f'Autocatch is connected as {client.user}', 'black', 'on_white'))

@client.event
async def on_message(message):
    global captcha
    global shiny
    global legendary
    global num_pokemon
    global mythical

    if message.author.id == ownerid and not message.embeds:
        content = message.content.lower().strip()
        if content.count(':') == 1:
            name, percentage = content.split(':')
            name = name.strip()
            percentage = percentage.strip()
            if percentage.endswith('%'):
                await asyncio.sleep(random.randint(1, 3))
                channel = message.channel
                await channel.send(f'<@716390085896962058> c {name}')

    if message.author.id == ownerid and message.content.startswith('$'):
        await client.process_commands(message)

    if message.author.id == 716390085896962058:
        content = message.content

        if 'The pokémon is ' in content:
            if not len(solve(content)):
                print('Pokemon not found.')
            else:
                for i in solve(content):
                    if captcha:
                        await asyncio.sleep(random.randint(1, 3))
                        channel = message.channel
                        name = i.lower()
                        await channel.send(f'<@716390085896962058> c {name}')

        elif 'Congratulations' in content:
            split = content.split(' ')
            pokemon = ' '.join(split[7:]).replace('!', '')
            if 'seem unusual...' in content:
                shiny += 1
                print(f'Shiny Pokémon caught! Pokémon: {pokemon}')
                print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
            else:
                num_pokemon += 1
                print(f'Total Pokémon Caught: {num_pokemon} :{pokemon}')

        elif 'That is the wrong pokémon!' in content and captcha:
            await asyncio.sleep(random.randint(1, 3))
            channel = message.channel
            await channel.send(f'<@716390085896962058> h')

        elif 'human' in content:
            captcha = False
            owner = await client.fetch_user(ownerid)
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

def CheckForUpdates():
    requests_count = 1
    while True:
        for file, url in Files.items():
            print(f'{requests_count} - (GET)[{url}]')
            requests_count += 1
            response = requests.get(url)
            if response.status_code == 200:
                with open(file, 'w') as arch:
                    arch.write(response.text)
                    print(f'{file} Reloaded.')
            else:
                print(f'Failed to update {file}. Status code: {response.status_code}')
        time.sleep(600)

Files = {
    'data/pokemon': 'https://raw.githubusercontent.com/Xellos69/catcher/main/data/pokemon',
}

CheckForUpdates()

client.run(token)
