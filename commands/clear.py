name = 'clear'
names = ['clear', 'purge']
desc = 'Clear a certain amount of messages.'
examples = ['40']
notes = 'The limit for this is very high (10000), but higher values (>2000) will be slower.'
reqperms = ['manage messages', 'read message history']
reqargs = ['c', 'conf']
cargs = [
    {
        'name': 'amount',
        'optional': False,
        'check': lambda a: a.isdigit() and 2 < int(a) < 10000 and int(a),
        'errmsg': 'Please use a valid amount between 2 and 10000.'
    }
]

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    try:
        # deletes the messages. it's +1 to handle the original message
        # discord.py purge actually can support over 100, unlike d.js and the api
        # it uses separate calls for >100 values

        if conf.clear_delete_pinned:
            await c.purge(limit=int(amount)+1)
        else:
            pins = await c.pins()
            await c.purge(limit=int(amount)+1, check=lambda x: x not in pins)
        message = await c.send(f'Successfully cleared {amount} messages.')

        # delete the sent message after 3 secs
        await message.delete(delay=3)
    except Exception as er:
        await c.send(f'Error while clearing messages: {er}')
        