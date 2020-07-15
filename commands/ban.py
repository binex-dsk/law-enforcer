from constants import checks

name = 'ban'
names = ['ban', 'snipe']
long = 'Ban a user from the server.'
syntax = '(user) (reason || none)'
ex1 = 'id1 dumb stupid'
ex2 = 'id2'
notes = 'The user is DMed upon being banned.'
reqperms = '`ban members`'
no_docs = False
arglength = 1

async def run(env):
    args, msg, g, c, m = [env[k] for k in ('args', 'msg', 'g', 'c', 'm')]

    try:
        await checks.perms(['ban_members'], g, c, m)
    except:
        return

    # checks for mentions
    if not msg.mentions:
        return await c.send('Please provide a member to ban.')

    member = msg.mentions[0]

    try:
        await checks.roles(m, member, g, c)
    except:
        return

    reason = ' '.join(args[1:len(args)]) or 'None'

    try:
        # try to tell the member they've been banned
        try:
            await member.send(f'{member}, you have been **banned** '\
            f'from {g} by {m}.\nReason: {reason}')
        # if it doesn't work, ignore it and move on
        except:
            pass
        await member.ban(reason=reason)
        await c.send(f'{m}, I have **banned** {member}.\nReason: {reason}')
    # if any error occurs, catch it and send it
    except Exception as e:
        await c.send(f'Error while banning user: {e}')
