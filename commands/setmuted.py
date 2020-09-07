from constants import db, checks
from tables import muted_roles as roles

name = 'setmuted'
names = ['setmuted', 'mutedrole']
desc = 'Set the muted role for the server.'
examples = ['705538476698763324', '644334910810619924']
notes = 'The usage of the `mute` and `unmute` commands will not be available until this is used.'
reqperms = ['manage guild', 'manage roles']
reqargs = ['args', 'g', 'c']
cargs = [
    {
        'name': 'role ID',
        'aname': 'role',
        'optional': False,
        'excarg': 'g',
        'check': lambda a, g: checks.cid(a, g.get_role),
        'errmsg': 'Please provide a valid role ID in this server.'
    }
]

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    fetched = db.fetch(roles, {'guild': g.id})

    if fetched:
        row = fetched.fetchone()
        if row.id == role.id:
            return await c.send('This role is already the muted role.')

        try:
            db.update(roles, {'guild': g.id}, {'id': args[0]})
            return await c.send(f'Successfully set muted role to {role.mention}.')
        except Exception as e:
            print(e)
            await c.send(f'Error while setting muted role:\n{e}')
    else:
        try:
            db.insert(roles, {'id': args[0], 'guild': g.id})

            return await c.send(f'Successfully set muted role to {role.mention}.')
        except Exception as e:
            print(e)
            return await c.send(f'Error while setting muted role:\n{e}')
