from constants import checks, auth
import discord, requests
from init import client

def safe_get(id):
    get = requests.get(f'https://discord.com/api/v8/users/{id}', headers={'Authorization': f'Bot {auth.token}'})
    if get.status_code == 200:
        user = discord.User(state=client._connection, data=get.json())
        return user
    return False

name = 'ban'
names = ['ban', 'snipe']
desc = 'Ban a user from the server.'
examples = ['id1 dumb stupid', '728694582086205550 leaving won\'t save you']
notes = 'The user is DMed upon being banned.'
reqperms = ['ban members']
reqargs = ['g', 'c', 'm', 'conf']
cargs = [
    {
        'name': 'user mention/id',
        'aname': 'user',
        'optional': False,
        'check': lambda a: checks.cid(a, safe_get),
        'errmsg': 'Please provide a valid user mention or ID to ban.'
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

    mem = g.get_member(user.id)
    if mem:
        try:
            await checks.roles(m, mem, g, c)
        except:
            return

    try:
        if conf.ban_dm:
            try:
                await user.send(conf.ban_dm_message.format(MEM=user, GUILD=g, MOD=m, REASON=reason))
            # if it doesn't work, ignore it and move on
            except:
                pass
        await g.ban(user, reason=reason, delete_message_days=conf.ban_delete_days)
        await c.send(f'{m}, I have **banned** {user}.\nReason: {reason}')
    # if any error occurs, catch it and send it
    except Exception as e:
        await c.send(f'Error while banning user: {e}')
