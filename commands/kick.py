from constants import checks, db
from tables import server_config

name = 'kick'
names = ['kick', 'softban']
long = 'Kick a user from the server.'
syntax = '(user) (reason || none)'
ex1 = 'id1 don\'t do that again'
ex2 = 'id2'
notes = 'The user is DMed upon being kicked. Additionally, '\
'by default, they are given a one-time invite to rejoin with.'
reqperms = ['kick members', 'create instant invite']
reqargs = ['args', 'msg', 'g', 'c', 'm']
no_docs = False
arglength = 1

async def run(**env):
    for _, a in enumerate(reqargs):
        globals().update({a: env.get(a)})

    conf = db.fetch(server_config, {'guild': g.id}).fetchone()

    if not msg.mentions:
        return await c.send('Please provide a member to kick.')

    member = msg.mentions[0]

    try:
        await checks.roles(m, member, g, c)
    except:
        return

    reason = ' '.join(args[1:len(args)]) or 'None'
    inv = await c.create_invite(reason=f'Temporary invite for {member}', max_uses=1)
    if conf.kick_dm_invite:
        kick_dm_inv_message = conf.kick_dm_inv_message.format(INV=inv)
    else:
        kick_dm_inv_message = None
    to_dm = conf.kick_dm_message.format(MEM=member, GUILD=g, MOD=m, REASON=reason, INV=kick_dm_inv_message)
    try:
        if conf.kick_dm:
            try:
                await member.send(to_dm)
            except:
                pass
        await member.kick(reason=reason)
        await c.send(f'{m}, I have **kicked** {member}.\nReason: {reason}')
    except Exception as e:
        await c.send(f'Error while kicking user: {e}')
