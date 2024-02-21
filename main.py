import asyncio
import random
import re
from discord.ext import commands, tasks

token = ""
ownerid = 822830992426926172

with open('data/pokemon', 'r', encoding='utf8') as file:
    pokemon_list = file.read()

shiny = 0
legendary = 0
num_pokemon = 0
mythical = 0

with open('data/legendary', 'r' ) as file:
    legendary_list = file.read()

with open('data/mythical', 'r' ) as file:
    mythical_list = file.read()

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
    owner = client.get_user(ownerid)
    await owner.send("I'm Ready Catch")

@client.event
async def on_message(message):
    global captcha
    global shiny
    global legendary
    global num_pokemon
    global mythical

    if message.author.id == 854233015475109888 and not message.embeds:
        content = message.content.lower().strip()
        if content.count(':') == 1:
            name, percentage = map(str.strip, content.split(':'))
            if percentage.endswith('%'):
                if captcha:
                    await asyncio.sleep(random.randint(1, 3.5))
                    await message.channel.send(f'<@716390085896962058> c {name.lower()}')

    if message.author.id == ownerid and message.content.startswith('$'):
        await client.process_commands(message)

    if message.author.id == 716390085896962058:
        content = message.content

        if 'The pokémon is ' in content:
            solved_pokemon = solve(content)
            if not solved_pokemon:
                print('Pokemon not found.')
            else:
                for i in solved_pokemon:
                    if captcha:
                        await asyncio.sleep(random.randint(1, 3))
                        await message.channel.send(f'<@716390085896962058> c {i.lower()}')

        elif 'Congratulations' in content:
            num_pokemon += 1
            split = content.split(' ')
            pokemon = ' '.join(split[7:]).replace('!', '')
            if 'seem unusual...' in content:
                shiny += 1
                print(f'Shiny Pokémon caught! Pokémon: {pokemon}')
                print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
            elif re.findall('^' + pokemon + '$', legendary_list, re.MULTILINE):
                legendary += 1
                print(f'Legendary Pokémon caught! Pokémon: {pokemon}')
                print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
            elif re.findall('^' + pokemon + '$', mythical_list, re.MULTILINE):
                mythical += 1
                print(f'Mythical Pokémon caught! Pokémon: {pokemon}')
                print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
            else:
                print(f'Total Pokémon Caught: {num_pokemon} :{pokemon}')

        elif 'human' in content:
            captcha = False
            owner = client.get_user(ownerid)
            await owner.send(f"<@{ownerid}> Please verify the Poketwo captcha asap!\n https://verify.poketwo.net/captcha/{client.user.id}")

        elif 'That is the wrong pokémon!' in content and captcha:
            await asyncio.sleep(random.randint(1, 3))
            await message.channel.send(f'<@716390085896962058> h')

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
