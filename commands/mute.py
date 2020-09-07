import datetime, calendar
from constants import checks, db
from tables import muted_roles as roles, muted_members as mems

def isfloat(stra):
    try:
        return float(stra)
    except:
        return False

name = 'mute'
names = ['mute']
desc = 'Mute a user for a certain amount of time.'
examples = ['id1 24 stop spamming', 'id2 0.5']
notes = 'The user is DMed when they are muted, as well as automatically unmuted.'
reqperms = ['mute members', 'kick members', 'manage roles']
reqargs = ['args', 'msg', 'g', 'c', 'm', 'conf']
cargs = [
    {
        'name': 'user mention/id',
        'aname': 'mem',
        'optional': False,
        'excarg': 'g',
        'check': lambda a, g: checks.cid(a, g.get_member),
        'errmsg': 'Please provide a valid member to mute.'
    },
    {
        'name': 'time',
        'optional': False,
        'check': lambda a: isfloat(a) and float(a),
        'errmsg': 'Please provide a valid mute time.'
    },
    {
        'name': 'reason',
        'optional': True,
        'default': 'None'
    }
]

def get_future(hrs):
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(hrs*60))
    return calendar.timegm(future.timetuple())

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    # checks the muted role
    result = db.fetch(roles, {'guild': g.id})
    if not result:
        return await c.send('No muted role is set! Please set one with `setmuted`.')

    role = result.fetchone()
    muted_role = g.get_role(role.id)

    if g.me.top_role < muted_role:
        return await c.send('I am at a lower level on the hierarchy than the muted role.')

    try:
        await checks.roles(m, mem, g, c)
    except:
        return

    # makes sure they aren't already muted
    if muted_role in mem.roles:
        return await c.send('That member is already muted.')

    try:
        # add the muted role to the member
        await mem.add_roles(muted_role, reason=reason)
        db.insert(mems, {'id': mem.id, 'guild': g.id, 'unmute_after': get_future(time)})
        await c.send(f'Successfully muted {mem} for {time} hours. Reason: {reason}')
        if conf.mute_dm:
            try:
                await mem.send(conf.mute_dm_message.format(MEM=mem, GUILD=g, MOD=m, TIME=time, REASON=reason))
            except:
                pass
    except Exception as e:
        await c.send(f'Error while muting member: {e}')
