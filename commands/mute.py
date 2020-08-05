import datetime, calendar, discord
from constants import checks, db
from tables import muted_roles as roles, muted_members as mems, server_config

name = 'mute'
names = ['mute']
long = 'Mute a user for a certain amount of time.'
syntax = '(user) (time) (reason || none)'
ex1 = 'id1 24 stop spamming'
ex2 = 'id2 0.5'
notes = 'The user is DMed when they are muted, as well as automatically unmuted.'
reqperms = ['mute members', 'kick members', 'manage roles']
reqargs = ['args', 'msg', 'g', 'c', 'm']
no_docs = False
arglength = 2

def get_future(hrs):
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(hrs*60))
    return calendar.timegm(future.timetuple())

async def run(**env):
    for _, a in enumerate(reqargs):
        globals().update({a: env.get(a)})

    conf = db.fetch(server_config, {'guild': g.id}).fetchone()

    # checks the muted role
    result = db.fetch(roles, {'guild': g.id})
    if not result:
        return await c.send('No muted role is set! Please set one with `setmuted`.')

    role = result.fetchone()
    muted_role = discord.utils.get(g.roles, id=role.id)

    if g.me.top_role < muted_role:
        return await c.send('I am at a lower level on the hierarchy than the muted role.')
    if not msg.mentions:
        return await c.send('Please mention a valid member.')

    mem = msg.mentions[0]

    try:
        await checks.roles(m, mem, g, c)
    except:
        return

    # makes sure they aren't already muted
    if muted_role in mem.roles:
        return await c.send('That member is already muted.')

    reason = ' '.join(args[2:len(args)]) or 'None'
    try:
        time = float(args[1])
    except:
        return await c.send('Please provide a valid time.')

    # this checks if it's an integer number of hours, i.e. 5, to stop it from displaying 5.0, etc.
    if float(int(time)) == time:
        time = int(time)
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
