import discord
from constants import checks, db

name = 'setmuted'
long = 'Set the muted role for the server.'
syntax = '(role ID)'
ex1 = '705538476698763324'
ex2 = '644334910810619924'
notes = 'The usage of the `mute` and `unmute` commands will not be available until this is used.'
reqperms = '`manage server`\n`manage roles`'
no_docs = False

async def run(env):
    args = env['args']
    g = env['g']
    c = env['c']
    m = env['m']
    conn = env['conn']
    roles = env['muted_roles']

    try:
        await checks.perms(['manage_guild', 'manage_roles'], g, c, m)
    except:
        return

    try:
        id = int(args[0])
    except:
        return await c.send('Please provide a valid role ID.')

    role = discord.utils.get(g.roles, id=id)

    if not role:
        return await c.send('This role is not present in the server.')

    fetched = db.fetch(roles, {'guild': g.id}, conn)
    row = None
    try:
        row = fetched.fetchone()
    except:
        pass

    if row:
        if row.id == id:
            return await c.send('This role is already the muted role.')

        try:
            db.update(roles, {'guild': g.id}, {'id': args[0]}, conn)
            return await c.send(f'Successfully set muted role to {role.mention}.')
        except Exception as e:
            print(e)
            await c.send(f'Error while setting muted role:\n{e}')
    else:
        try:
            db.insert(roles, {'id': args[0], 'guild': g.id}, conn)

            return await c.send(f'Successfully set muted role to {role.mention}.')
        except Exception as e:
            print(e)
            return await c.send(f'Error while setting muted role:\n{e}')
