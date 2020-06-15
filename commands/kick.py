from constants import checks

name = 'kick'
long = 'Kick a user from the server.'
syntax = '(user) (reason || none)'
ex1 = 'id1 don\'t do that again'
ex2 = 'id2'
notes = 'The user is DMed upon being kicked. Additionally, '\
'they are given a one-time invite to rejoin with.'\
'\nIn later versions, there will be options to disable this.'
reqperms = '`kick members`\n`create instant invite`'
no_docs = False

async def run(env):
    args = env['args']
    msg = env['msg']
    g = env['g']
    c = env['c']
    m = env['m']

    try:
        await checks.perms(['kick_members', 'create_instant_invite'], g, c, m)
    except:
        return

    if not msg.mentions:
        return await c.send('Please provide a member to kick.')

    member = msg.mentions[0]

    try:
        await checks.roles(m, member, g, c)
    except:
        return

    reason = ' '.join(args[1:len(args)]) or 'None'
    inv = await c.create_invite(reason=f'Temporary invite for {member}', max_uses=1)

    try:
        try:
            await member.send(f'{member}, you have been **kicked** '\
            f'from {g} by {m}.\nReason: {reason}\n'\
            f'I have created a one-time invite for you to join back with: {inv}')
        except:
            pass
        await member.kick(reason=reason)
        await c.send(f'{m}, I have **kicked** {member}.\nReason: {reason}')
    except Exception as e:
        await c.send(f'Error while kicking user: {e}')
