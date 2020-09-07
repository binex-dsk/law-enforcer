from constants import checks

name = 'kick'
names = ['kick', 'softban']
desc = 'Kick a user from the server.'
examples = ['id1 don\'t do that again', 'id2']
notes = 'The user is DMed upon being kicked. Additionally, '\
'by default, they are given a one-time invite to rejoin with.'
reqperms = ['kick members', 'create instant invite']
reqargs = ['args', 'msg', 'g', 'c', 'm', 'conf']
cargs = [
    {
        'name': 'user mention/id',
        'aname': 'mem',
        'optional': False,
        'excarg': 'g',
        'check': lambda a, g: checks.cid(a, g.get_member),
        'errmsg': 'Please provide a member to kick.'
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
        await checks.roles(m, mem, g, c)
    except:
        return

    inv = await c.create_invite(reason=f'Temporary invite for {mem}', max_uses=1)
    if conf.kick_dm_invite:
        kick_dm_inv_message = conf.kick_dm_inv_message.format(INV=inv)
    else:
        kick_dm_inv_message = None
    to_dm = conf.kick_dm_message.format(MEM=mem, GUILD=g, MOD=m, REASON=reason, INV=kick_dm_inv_message)
    try:
        if conf.kick_dm:
            try:
                await mem.send(to_dm)
            except:
                pass
        await mem.kick(reason=reason)
        await c.send(f'{m}, I have **kicked** {mem}.\nReason: {reason}')
    except Exception as e:
        await c.send(f'Error while kicking user: {e}')
