from discord.ext import commands
import aiohttp
import discord
import os
from dotenv import load_dotenv
from predicate import predicate_channel, predicate_furry_channel, predicate_vk_channel

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
vk_token = os.getenv('VK_TOKEN')
vk_api_vesion = os.getenv('API_VERSION')
vk_domain = os.getenv('DOMAIN')
vk_count = os.getenv('COUNT')

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True

client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')


has_channel = commands.check(predicate_channel)
has_furry_channel = commands.check(predicate_furry_channel)
has_vk_channel = commands.check(predicate_vk_channel)

@client.event
async def on_ready():
    print("Ready")


async def on_member_join(member):
    """Функция для выдачи роли новым пользователям"""
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
    """Команда для вывода команд бота"""
    title_error_two = 'список команд'
    desc_error_two = '!clear [msg_count] = удаление сообщений (для админов)\n!cat = вывод картинки кота\n!dog = вывод картинки собаки\n!avatar = вывод аватарки пользователя' \
                     '\n!gaysex = специально для Блетза\n!anime = вывод аниме NSFW'
    embed_var_two = discord.Embed(title=title_error_two,
                                  description=desc_error_two,
                                  color=0xFF0000)
    await ctx.reply(embed=embed_var_two)


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    """Функция удаления сообщений"""
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=discord.Embed(
        description=f':white_check_mark: удалено {amount} сообщений(я)'))


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
async def anime(ctx, member: discord.Member = None):
    """Фунция вывода anime NSFW"""
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://api.waifu.pics/nsfw/waifu')
        json = await request.json(content_type=None)

    embed = discord.Embed(title="Анимешная блядина",
                          color=discord.Color.purple())
    embed.set_image(url=json["url"])
    await ctx.send(embed=embed)


@client.command()
@has_channel
async def avatar(ctx, member: discord.Member = None):
    """Команда для вывода аватарки"""
    if member == None:  # если не упоминать участника тогда выводит аватар автора сообщения
        member = ctx.author
    embed = discord.Embed(title=member).set_image(url=member.avatar.url)
    await ctx.send(embed=embed)


@client.command()
@has_channel
async def gaysex(ctx, member: discord.Member = None):
    """Команда для шлепования"""
    if member == None:  # если не упоминать участника тогда выводит аватар автора сообщения
        member = ctx.author
    dest_one = 'пользователь ' + str(member) + ' был отшлепан'
    embed = discord.Embed(title=dest_one)
    await ctx.send(embed=embed)


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
        embed = discord.Embed(title="Пост без заголовка", color=discord.Color.purple())
        embed.set_image(url=json['response']['items'][0]['attachments'][0]['photo']['sizes'][6]['url'])
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=json['response']['items'][0]['text'], color=discord.Color.purple())
        embed.set_image(url=json['response']['items'][0]['attachments'][0]['photo']['sizes'][6]['url'])
        await ctx.send(embed=embed)


client.run(token)

