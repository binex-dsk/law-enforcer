from constants import checks
from tables import server_config
import constants.db as db

name = 'clear'
names = ['clear', 'purge']
long = 'Clear a certain amount of messages.'
syntax = '(amount || 20)'
ex1 = '40'
ex2 = ' '
notes = 'The limit for this is very high (10000), but higher values (>2000) will be slower.'
reqperms = '`manage messages`\n`read message history`'
no_docs = False
arglength = 1

async def run(env):
    args, g, c, m = [env[k] for k in ('args', 'g', 'c', 'm')]

    conf = db.fetch(server_config, {'guild': g.id}).fetchone()
    try:
        await checks.perms(['manage_messages', 'read_message_history'], g, c, m)
    except:
        return

    if len(args) < 1:
        amt = 20
    else:
        amt = int(args[0])
    if amt > 10000 or amt < 2:
        return await c.send('Please use a valid amount between 2 and 10000.')
    try:
        # deletes the messages. it's +1 to handle the original message
        # discord.py purge actually can support over 100, unlike d.js and the api
        # it uses separate calls for >100 values
        
        if conf.clear_delete_pinned:
            await c.purge(limit=amt+1)
        else:
            pins = await c.pins()
            await c.purge(limit=amt+1, check=lambda x:x not in pins)
        message = await c.send(f'Successfully cleared {amt} messages.')

        # delete the sent message after 3 secs
        await message.delete(delay=3)
    except Exception as er:
        await c.send(f'Error while clearing messages: {er}')
        