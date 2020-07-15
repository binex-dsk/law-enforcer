import discord
from constants import checks, db
from tables import muted_roles as roles, muted_members as mems

name = 'unmute'
names = ['unmute']
long = 'Unmuted a muted user.'
syntax = '(user) (reason || none)'
ex1 = 'id1 said sorry in dms'
ex2 = 'id2'
notes = 'The user is DMed when unmuted.'
reqperms = '`mute members`\n`kick members`\n`manage roles`'
no_docs = False
arglength = 1

async def run(env):
    args, msg, g, c, m = [env[k] for k in ('args', 'msg', 'g', 'c', 'm')]

    try:
        await checks.perms(['mute_members', 'kick_members', 'manage_roles'], g, c, m)
    except:
        return

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

    reason = ' '.join(args[1:len(args)]) or 'None'
    if not muted_role in mem.roles:
        return await c.send('This member is not muted.')

    await mem.remove_roles(muted_role, reason=reason)
    db.delete(mems, {'id': mem.id, 'guild': g.id})
    await c.send(f'Successfully unmuted {mem}.\nReason: {reason}')
    try:
        await mem.send(f'You\'ve been unmuted in {g} by {m}.\nReason: {reason}')
    except:
        pass
