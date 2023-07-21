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


def predicate_channel(ctx):
  """Ограничение для вызова команд в опеределенном канале"""
  channel = client.get_channel(753565123397943358)
  if ctx.channel != channel:
    return False
  else:
    return True


def predicate_furry_channel(ctx):
  """Ограничение для вызова команд в опеределенном канале"""
  bot_channel = client.get_channel(1108066137847119966)
  if ctx.channel != bot_channel:
    return False
  else:
    return True


has_channel = commands.check(predicate_channel)
has_furry_channel = commands.check(predicate_furry_channel)


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
  desc_error_two = '!cat = вывод картинки кота\n!dog = вывод картинки собаки\n!avatar = вывод аватарки пользователя' \
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
  if member == None:  #если не упоминать участника тогда выводит аватар автора сообщения
    member = ctx.author
  embed = discord.Embed(title=member).set_image(url=member.avatar.url)
  await ctx.send(embed=embed)


@client.command()
@has_channel
async def gaysex(ctx, member: discord.Member = None):
  """Команда для шлепования"""
  if member == None:  #если не упоминать участника тогда выводит аватар автора сообщения
    member = ctx.author
  dest_one = 'пользователь ' + str(member) + ' был отшлепан'
  embed = discord.Embed(title=dest_one)
  await ctx.send(embed=embed)


client.run(token)
