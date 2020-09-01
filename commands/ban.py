from constants import checks, db
from tables import server_config
from discord.utils import escape_mentions

name = 'ban'
names = ['ban', 'snipe']
desc = 'Ban a user from the server.'
examples = ['id1 dumb stupid', '728694582086205550 leaving won\'t save you']
notes = 'The user is DMed upon being banned.'
reqperms = ['ban members']
reqargs = ['client', 'args', 'msg', 'g', 'c', 'm', 'conf']
cargs = [
    {
        'name': 'user mention/id',
        'aname': 'id',
        'optional': False,
        'excarg': 'client',
        'check': lambda a, c: (a.isdigit() or escape_mentions(a) != a) and (mid := int(a.strip('<@&#!>'))) in [x.id for x in c.get_all_members()] and mid,
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

    mem = g.get_member(id)
    user = await client.fetch_user(id)
    if mem:
        try:
            await checks.roles(m, mem, g, c)
        except:
            return

    try:
        if conf.ban_dm:
            try:
                await mem.send(conf.ban_dm_message.format(MEM=user, GUILD=g, MOD=m, REASON=reason))
            # if it doesn't work, ignore it and move on
            except:
                pass
        await g.ban(user, reason=reason, delete_message_days=conf.ban_delete_days)
        await c.send(f'{m}, I have **banned** {user}.\nReason: {reason}')
    # if any error occurs, catch it and send it
    except Exception as e:
        await c.send(f'Error while banning user: {e}')
