from discord.ext import commands
import aiohttp
import discord
import os
from dotenv import load_dotenv
from random import randint

load_dotenv()

dubug = False
title_error = 'Бот на тех.обслуживании'
description_error = 'Бот в текущее время не работает'
error = discord.Embed(title=title_error, description=description_error, color=0xFF0000)

token = os.getenv('DISCORD_TOKEN')
vk_token = os.getenv('VK_TOKEN')
vk_api_vesion = os.getenv('API_VERSION')
vk_domain = os.getenv('DOMAIN')
vk_furry_domain = os.getenv('FURRYI_DOMAIN')
vk_count = os.getenv('COUNT')

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True

client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print("Ready")


def predicate_channel(ctx):
    channel = client.get_channel(753565123397943358)
    if ctx.channel != channel:
        return False
    else:
        return True


def predicate_main_channel(ctx):
    channel = client.get_channel(753533012645511188)
    if ctx.channel != channel:
        return False
    else:
        return True


def predicate_furry_channel(ctx):
    bot_channel = client.get_channel(1108066137847119966)
    if ctx.channel != bot_channel:
        return False
    else:
        return True


def predicate_vk_channel(ctx):
    bot_channel = client.get_channel(1132048003113418822)
    if ctx.channel != bot_channel:
        return False
    else:
        return True


has_channel = commands.check(predicate_channel)
has_furry_channel = commands.check(predicate_furry_channel)
has_vk_channel = commands.check(predicate_vk_channel)
has_main_channel = commands.check(predicate_main_channel)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=753566876327739463)
    await member.add_roles(role)


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
@has_channel
async def help(ctx):
    """Вывод команд бота"""
    if dubug is True:
        error = discord.Embed(title=title_error,
                              description=description_error,
                              color=0xFF0000)
        await ctx.reply(embed=error)
    else:
        title_error_two = 'список команд'
        desc_error_two = '!clear [msg_count] = удаление сообщений (для админов)\n!cat = вывод картинки кота\n!dog = ' \
                         'вывод картинки собаки\n!avatar = вывод аватарки пользователя' \
                         '\n!gaysex = специально для Блетза\n!a = вывод аниме NSFW\n!vk = вывод последнего поста из ' \
                         'паблика "клуб любителей интернета"\n!furry = вывод фурри из паблика вк\n!boy = вывод ' \
                         'Бойкиссера '
        embed_var_two = discord.Embed(title=title_error_two,
                                      description=desc_error_two,
                                      color=0xFF0000)
        await ctx.reply(embed=embed_var_two)


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=discord.Embed(
        description=f':white_check_mark: удалено {amount} сообщений(я)'))


@client.command()
@has_channel
async def dog(ctx):
    """Команда для вывода случайного изображения собаки"""
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.com/animal/dog')
        json = await request.json(content_type=None)
        embed = discord.Embed(title="Собака", color=discord.Color.purple())
        embed.set_image(url=json['image'])
        await ctx.send(embed=embed)


@client.command()
@has_channel
async def cat(ctx):
    """Команда для вывода случайного изображения кота"""
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.com/animal/cat')
        json = await request.json(content_type=None)
        embed = discord.Embed(title="Кот", color=discord.Color.purple())
        embed.set_image(url=json['image'])
        await ctx.send(embed=embed)


@client.command()
@has_furry_channel
async def a(ctx):
    """Фунция вывода anime NSFW"""
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://api.waifu.pics/nsfw/waifu')
        json = await request.json(content_type=None)
        user = ctx.author.id
        print(user)
        if user == 966302633491070976:
            embed = discord.Embed(title="Мршк, тебе низя", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Анимешная блядина",
                                  color=discord.Color.purple())
            embed.set_image(url=json["url"])
            await ctx.send(embed=embed)


@client.command()
@has_channel
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
        embed = discord.Embed(title=member).set_image(url=member.avatar.url)
        await ctx.send(embed=embed)


@client.command()
@has_channel
async def gaysex(ctx, member: discord.Member = None):
    if member == None:
        return
    await ctx.channel.send(f"{ctx.author.mention} отшлепал {member.mention}")


@client.command()
@has_vk_channel
async def vk(ctx):
    """Команда для вывода поста из группы вк"""
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://api.vk.com/method/wall.get', params={
            'access_token': vk_token,
            'v': vk_api_vesion,
            'domain': vk_domain,
            'count': vk_count,
        })
        json = await request.json(content_type=None)

    if json['response']['items'][0]['text'] == "":
        embed = discord.Embed(title="Пост без заголовка", description=json['response']['items'][0]['views']['count'],
                              color=discord.Color.purple())
        embed.set_image(url=json['response']['items'][0]['attachments'][0]['photo']['sizes'][6]['url'])
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=json['response']['items'][0]['text'],
                              description=json['response']['items'][0]['views']['count'], color=discord.Color.purple())
        embed.set_image(url=json['response']['items'][0]['attachments'][0]['photo']['sizes'][6]['url'])
        await ctx.send(embed=embed)


@client.command()
@has_furry_channel
async def furry(ctx):
    async with aiohttp.ClientSession() as session:
        offset = randint(1, 2000)
        request = await session.get('https://api.vk.com/method/wall.get', params={
            'access_token': vk_token,
            'v': vk_api_vesion,
            'domain': vk_furry_domain,
            'offset': offset,
            'count': vk_count
        })
        responce = await request.json(content_type=None)

    if responce['response']['items'][0]['attachments'][0]['photo']['sizes'][9] in \
            responce['response']['items'][0]['attachments'][0]['photo']['sizes']:
        embed = discord.Embed(title="Фулл разрешение", description=responce['response']['items'][0]['text'],
                              color=discord.Color.purple())
        embed.set_image(url=responce['response']['items'][0]['attachments'][0]['photo']['sizes'][9]['url'])
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Мелкое разрешение", description=responce['response']['items'][0]['text'],
                              color=discord.Color.purple())
        embed.set_image(url=responce['response']['items'][0]['attachments'][0]['photo']['sizes'][6]['url'])
        await ctx.send(embed=embed)


@client.command()
async def boy(ctx):
    dest_one = 'Pull up, pull up'
    embed = discord.Embed(title=dest_one, color=discord.Color.purple())
    embed.set_image(
        url='https://media.discordapp.net/attachments/733238386265030679/1063708725271076884/FmXYH1OWAAAPZXi.gif')
    await ctx.send(embed=embed)


client.run(token)
