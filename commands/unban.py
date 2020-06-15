import random
from constants.auth import ids
from constants import checks

name = 'unban'
long = 'Unban a banned user from the server.'
syntax = '(user ID) (reason || none)'
ex1 = f'{ids[random.randint(0, 1)]} not dumb stupid'
ex2 = ids[random.randint(0, 1)]
notes = 'The user is DMed upon being unbanned (if I can DM them).'
reqperms = '`ban members`'
no_docs = False

async def run(env):
    args = env['args']
    client = env['client']
    g = env['g']
    c = env['c']
    m = env['m']

    try:
        await checks.perms(['ban_members'], g, c, m)
    except:
        return

    if len(args) < 1:
        return await c.send('Please enter a user ID to unban.\n'
        'To get a user ID, enable **Developer Mode** in the **Appearance** tab '\
        'in settings, then right-click the user and select **\'Copy ID.\'**')

    try:
        id = int(args[0])
    except:
        return await c.send('Please provide a valid ID.')

    reason = ' '.join(args[1:len(args)]) or 'None'

    ban = None

    try:
        # fetch the ban for that user
        user = client.get_user(id)
        ban = await g.fetch_ban(user)
    except Exception as e:
        # fetch_ban throws an exception if the user isn't banned
        # so catch it here to notify the user
        await c.send('This user is not banned.')
        return print(f'{e}')

    try:
        await g.unban(ban.user, reason=reason)
        await c.send(f'Successfully unbanned {ban.user}.\nReason: {reason}')
        try:
            await ban.user.send(f'You have been **unbanned** in {g} by {m}.\nReason: {reason}')
        except:
            pass
    except Exception as e:
        await c.send(f'Error while unbanning user.\n{e}')
