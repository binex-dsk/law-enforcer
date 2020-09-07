import random
from constants.auth import ids, token
import requests, discord
from init import client

def safe_bancheck(g, id):
    get = requests.get(f'https://discord.com/api/v8/guilds/{g}/bans/{id}', headers={'Authorization': f'Bot {token}'})
    if get.status_code == 200:
        user = discord.User(state=client._connection, data=get.json()['user'])
        return user
    return False

name = 'unban'
names = ['unban', 'unsnipe']
desc = 'Unban a banned user from the server.'
examples = [f'{ids[random.randint(0, 1)]} not dumb stupid', str(ids[random.randint(0, 1)])]
notes = 'The user is DMed upon being unbanned (if I can DM them).'
reqperms = ['ban members']
reqargs = ['args', 'client', 'g', 'c', 'm', 'conf']
cargs = [
    {
        'name': 'user id',
        'aname': 'user',
        'optional': False,
        'excarg': 'g',
        'check': lambda a, g: a.isdigit() and safe_bancheck(g, int(a)),
        'errmsg': 'Please provide a valid banned user ID to unban.'
    },
    {
        'name': 'reason',
        'optional': True,
        'default': 'None'
    }
]

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    try:
        await g.unban(user, reason=reason)
        await c.send(f'Successfully unbanned {user}.\nReason: {reason}')
        if conf.unban_dm:
            try:
                await user.send(conf.unban_dm_message.format(MEM=user, GUILD=g, MOD=m, REASON=reason))
            except:
                pass
    except Exception as e:
        await c.send(f'Error while unbanning user.\n{e}')
