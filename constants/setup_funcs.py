import math, discord

# not the best but idc
async def role(g, c, m, client):
    while True:
        await c.send('If you would like to stop creating roles, please type `stop` now.\n'\
        'Otherwise, let\'s get started!\nFirst, what role name do you want?')

        role_name = 'New Role'
        role_perms = 0
        role_hoist = False

        ms = await client.wait_for('message', check=lambda s: s.author.id == m.id)

        if ms.content == 'stop':
            await c.send('Stopping interactive role creation, please wait...')
            break
        role_name = ms.content

        await c.send('Great! Now, what permissions integer do you want?\n'\
        'To get a permission integer, please visit https://discordapi.com/permissions.html.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id and not math.isnan(int(s.content)))

        role_perms = int(ms.content)

        await c.send('Good. Now, please provide an RGB value '\
        'for the role\'s color.\nTo get an RGB value, go to '\
        'https://www.rapidtables.com/web/color/RGB_Color.html.\n'\
        'Provide the values like this: R G B. For example, 204 16 143.')

        ms = await client.wait_for('message', check=lambda s: s.author.id == m.id)

        split = ms.content.split()

        await c.send('Thanks! Finally, would you like this role '\
        'to be separate from others?\nType `y` if so, or `n` if not.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id and s.content in ['y', 'n'])

        if ms.content == 'y':
            role_hoist = True

        await c.send('Alright. Your role has been configured. Please review these settings.\n```'\
        'Name: {role_name}\nPermissions: {role_perms}\n'\
        'RGB Color Value: {' '.join(split)}\nHoist: {role_hoist}```'\
        'If these are correct, type `y`. Otherwise, type `n`. '\
        'NOTE: If they are incorrect, you will have to re-setup the role.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id and s.content in ['y', 'n'])

        if ms.content == 'n':
            await c.send('Restarting role setup...')
            continue
        await c.send('Great! I am now creating the role, please wait...')
        try:
            await g.create_role(name=role_name,
            permissions=discord.Permissions(permissions=role_perms),
            color=discord.Color.from_rgb(int(split[0]),
            int(split[1]), int(split[2])), hoist=role_hoist)
            await c.send('Successfully created the role! Please manually set the role\'s position.')
        except Exception as e:
            await c.send(f'Error while creating role:\n{e}\nAborting role creation.')
            print(e)
            