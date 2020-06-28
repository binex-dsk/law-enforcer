import discord
from constants import checks, setup_funcs # noqa

name = 'setup'
names = ['setup']
long = 'Setup your brand-new server.'
syntax = ''
ex1 = False
ex2 = False
notes = 'This server setup is very much in a beta state. '\
'Any issues must be redirected to the owner, using the `contact` command.'
reqperms = '`administrator`'
no_docs = False
arglength = 0

# this isn't the most efficient but it works
async def run(env):
    client = env['client']
    g = env['g']
    c = env['c']
    m = env['m']

    try:
        await checks.perms(['administrator'], g, c, m)
    except:
        return

    await c.send('Welcome to the interactive server setup!\n'\
    'This is a guide to help set your server up like any good server.\n'\
    'To get you started, let\'s go through some basic things.\n'\
    'First off, do you want to change your server\'s name?\n'\
    'Type the new name if so, otherwise type `n`.')

    ms = await client.wait_for('message', check=lambda s: s.author.id == m.id)

    if ms.content == 'n':
        await c.send('Your guild\'s name will not be changed.')
    else:
        try:
            await g.edit(name=ms.content)
            await c.send(f'Successfully set your guild\'s name to {ms.content}.')
        except Exception as e:
            await c.send(f'Error while renaming guild:\n{e}\n'\
            'Aborting name change. Guild name will stay as it was before.')
            print(e)

    await c.send('Next, I will automatically change a few things. Please wait...')

    try:
        await g.edit(default_notifications=1)
        await c.send('Successfully set notifications to mentions only.')
    except Exception as e:
        await c.send(f'Error while setting default notification settings:\n{e}\n'\
        'Keeping default notifications as they are now.')
        print(e)

    try:
        await g.default_role.edit(permissions=discord.Permissions(permissions=104189505))
        await c.send('Successfully set the default role\'s permissions.')
    except Exception as e:
        await c.send(f'Error while setting default role\'s permissions:\n{e}\n'\
        'Keeping default permissions as they are now.')
        print(e)

    await c.send('Next, we will set up some roles.\n'\
    'First, do you want an admin role?\n'\
    'Type `y` if you do, otherwise type `n`.')

    ms = await client.wait_for('message',
    check=lambda s: s.author.id == m.id and s.content in ['y', 'n'])

    if ms.content == 'y':
        await c.send('Alright. Do you want full admin privileges or just full permissions\n'\
        'NOTE: Giving full admin privileges is dangerous! '\
        'Only select this if you trust your admins.\n'\
        'Type `y` if you want full admin privileges, '\
        'or `n` for just permissions.')

        message = await client.wait_for('message',
        check=lambda s: s.author.id == m.id and s.content in ['y', 'n'])

        try:
            txt = 'admin privileges'
            perm_int = 8
            if message.content == 'n':
                txt = 'permissions'
                perm_int = 2146958839

            await g.create_role(name='Admin',
            permissions=discord.Permissions(permissions=perm_int), hoist=True)
            await c.send(f'Successfully created an Admin role with full {txt}.')
        except Exception as e:
            await c.send(f'Error while creating admin role:\n{e}\nAborting role creation..')
            print(e)
    else:
        await c.send('No Admin role will be created.')
    await c.send('Now, we will set up a few roles!')

    await setup_funcs.role(g, c, m, client)

    await c.send('Thank you for using the interactive server setup!\n'\
    'Please contact the owner for feedback, errors, or other similar things.')
