import discord
from constants import checks, db
from tables import muted_roles as roles, muted_members as mems, server_config

name = 'unmute'
names = ['unmute']
long = 'Unmuted a muted user.'
syntax = '(user) (reason || none)'
ex1 = 'id1 said sorry in dms'
ex2 = 'id2'
notes = 'The user is DMed when unmuted.'
reqperms = ['mute members', 'kick members', 'manage roles']
reqargs = ['args', 'msg', 'g', 'c', 'm']
no_docs = False
arglength = 1

async def run(**env):
    for _, a in enumerate(reqargs):
        globals().update({a: env.get(a)})

    conf = db.fetch(server_config, {'guild': g.id}).fetchone()

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
    try:
        await mem.remove_roles(muted_role, reason=reason)
        db.delete(mems, {'id': mem.id, 'guild': g.id})
        await c.send(f'Successfully unmuted {mem}.\nReason: {reason}')
        if conf.mute_dm:
            try:
                await mem.send(conf.mute_dm_message.format(MEM=mem, GUILD=g, MOD=m, REASON=reason))
            except:
                pass
    except Exception as e:
        await c.send(f'Error while unmuting member: {e}')
