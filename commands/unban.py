import random
from constants import db
from constants.auth import ids
from tables import server_config

name = 'unban'
names = ['unban', 'unsnipe']
desc = 'Unban a banned user from the server.'
examples = [f'{ids[random.randint(0, 1)]} not dumb stupid', str(ids[random.randint(0, 1)])]
notes = 'The user is DMed upon being unbanned (if I can DM them).'
reqperms = ['ban members']
reqargs = ['args', 'client', 'g', 'c', 'm', 'conf']
cargs = [
    {
        'name': 'user mention/id',
        'aname': 'id',
        'optional': False,
        'excarg': 'client',
        'check': lambda a, c: a.isdigit() and int(a),
        'errmsg': 'Please provide a valid user ID to unban.'
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

    ban = None

    try:
        # fetch the ban for that user
        user = await client.fetch_user(id)
        ban = await g.fetch_ban(user)
    except Exception as e:
        # fetch_ban throws an exception if the user isn't banned
        # so catch it here to notify the user
        await c.send('This user is not banned.')
        return print(f'{e}')

    try:
        await g.unban(ban.user, reason=reason)
        await c.send(f'Successfully unbanned {ban.user}.\nReason: {reason}')
        if conf.unban_dm:
            try:
                await ban.user.send(conf.unban_dm_message.format(MEM=ban.user, GUILD=g, MOD=m, REASON=reason))
            except:
                pass
    except Exception as e:
        await c.send(f'Error while unbanning user.\n{e}')
