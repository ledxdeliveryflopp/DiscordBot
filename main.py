import io

from discord.ext import commands
import aiohttp
import discord
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True

client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print("Ready")


@client.event
async def on_command_error(ctx, error):
    """Функция вывода ошибки команды"""
    if isinstance(error, commands.CommandNotFound):
        title_error_two = 'Введенная вами команда не существует'
        desc_error_two = 'Используйте **!help**, чтобы просмотреть список всех доступных команд'
        embed_var_two = discord.Embed(title=title_error_two,
                                      description=desc_error_two,
                                      color=0xFF0000)
        await ctx.reply(embed=embed_var_two)


@client.command()
async def help(ctx):
    """Команда для вывода команд бота"""
    title_error_two = 'список команд'
    desc_error_two = '!cat = вывод картинки кота\n!dog = вывод картинки собаки\n!avatar = вывод аватарки пользователя' \
                     '\n!gaysex = специально для Блетза'
    embed_var_two = discord.Embed(title=title_error_two,
                                  description=desc_error_two,
                                  color=0xFF0000)
    await ctx.reply(embed=embed_var_two)


@client.command()
async def dog(ctx):
    """Команда для вывода случайного изображения собаки"""
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.com/animal/dog')
        json = await request.json(content_type=None)

    embed = discord.Embed(title="Собака", color=discord.Color.purple())
    embed.set_image(url=json['image'])
    await ctx.send(embed=embed)


@client.command()
async def cat(ctx):
    """Команда для вывода случайного изображения кота"""
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.com/animal/cat')
        json = await request.json(content_type=None)

    embed = discord.Embed(title="Кот", color=discord.Color.purple())
    embed.set_image(url=json['image'])
    await ctx.send(embed=embed)


@client.command()
async def furry(ctx, member: discord.Member = None):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://e621.net/posts.json?limit=1')
        json = await request.json(content_type=None)

    embed = discord.Embed(title="Кот", color=discord.Color.purple())
    embed.set_image(url=json['url'])
    await ctx.send(embed=embed)


@client.command()
async def avatar(ctx, member: discord.Member = None):
    """Команда для вывода аватарки"""
    if member == None:#если не упоминать участника тогда выводит аватар автора сообщения
        member = ctx.author
    embed = discord.Embed(title=member).set_image(url=member.avatar.url)
    await ctx.send(embed=embed)


@client.command()
async def gaysex(ctx, member: discord.Member = None):
    """Команда для вывода аватарки"""
    if member == None:#если не упоминать участника тогда выводит аватар автора сообщения
        member = ctx.author
    dest_one = 'пользователь ' + str(member) + ' был отшлепан'
    embed = discord.Embed(title=dest_one)
    await ctx.send(embed=embed)


client.run(token)
