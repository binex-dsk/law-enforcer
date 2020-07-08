import asyncio, discord
from constants import checks, db

name = 'mute'
names = ['mute']
long = 'Mute a user for a certain amount of time'
syntax = '(user) (time) (reason || none)'
ex1 = 'id1 24 stop spamming'
ex2 = 'id2 0.5'
notes = 'The user is DMed when they are muted, as well as automatically unmuted.'
reqperms = '`mute members`\n`kick members`\n`manage roles`'
no_docs = False
arglength = 2

async def unmute(m, t, r, role):
    await asyncio.sleep(t*60*60)
    if not role in m.roles:
        return
    await m.remove_roles(role, reason=r)
    try:
        await m.send(f'You\'ve been automatically unmuted in {m.guild}.')
    except:
        pass

async def run(env):
    args = env['args']
    msg = env['msg']
    g = env['g']
    c = env['c']
    m = env['m']
    conn = env['conn']
    roles = env['muted_roles']

    try:
        await checks.perms(['mute_members', 'kick_members', 'manage_roles'], g, c, m)
    except:
        return

    # checks the muted role
    result = db.fetch(roles, {'guild': g.id}, conn)
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
        await c.send(f'Successfully muted {mem} for {time} hours. Reason: {reason}')
        try:
            await mem.send(f'You\'ve been muted in {g} by {m} for {time} hours.\nReason: {reason}')
        except:
            pass
        # goes to the unmute function, muting them for the specified time
        await unmute(mem, time, 'Mute time expired', muted_role)
    except Exception as e:
        await c.send(f'Error while muting member: {e}')
