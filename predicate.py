from main import client


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


def predicate_vk_channel(ctx):
    """Ограничение для вызова команд в опеределенном канале"""
    bot_channel = client.get_channel(1132048003113418822)
    if ctx.channel != bot_channel:
        return False
    else:
        return True