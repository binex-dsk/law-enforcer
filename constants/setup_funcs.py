import discord

allowed_perms = ['add_reactions', 'administrator', 'attach_files', 'ban_members',
'change_nickname', 'connect', 'create_instant_invite', 'deafen_members', 'embed_links',
'external_emojis', 'kick_members', 'manage_channels', 'manage_emojis', 'manage_guild',
'manage_messages', 'manage_nicknames', 'manage_permissions', 'manage_roles', 'manage_webhooks',
'mention_everyone', 'move_members', 'mute_members', 'priority_speaker', 'read_message_history',
'read_messages', 'send_messages', 'send_tts_messages', 'speak', 'stream', 'use_external_emojis',
'use_voice_activation', 'view_audit_log', 'view_channel', 'view_guild_insights']

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
        check=lambda s: s.author.id == m.id and s.content.isdigit())

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
        f'Name: {role_name}\nPermissions: {role_perms}\n'\
        f'RGB Color Value: {" ".join(split)}\nHoist: {role_hoist}```'\
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

async def channel(g, c, m, client):
    while True:
        await c.send('If you would like to stop creating channels, please type `stop` now.\n'\
        'Otherwise, let\'s get started!\nFirst, what channel type do you want?\n'\
        'Options are: `category`, `voice`, and `text`.')

        ch = {}

        ms = await client.wait_for('message', check=lambda s: s.author.id == m.id and
        s.content in ['text', 'category', 'voice', 'stop'])

        if ms.content == 'stop':
            await c.send('Stopping interactive channel creation, please wait...')
            break
        ch_type = ms.content

        await c.send('Great. What name should the channel have?')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id)

        ch['name'] = ms.content

        await c.send('Next, what position do you want this channel to be in? '\
        '0 is the top, 1 is the second-to-top, etc.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id and s.content.isdigit())

        ch['position'] = int(ms.content)

        await c.send('Good. Now, we will go through overwrites.\n'\
        'This can be confusing, but don\'t worry, this will guide'\
        ' you through.')

        overwrite = await overwrites(g, c, m, client)
        overwrite = dict(overwrite)

        await c.send('Now that overwrites are set up, we '\
        'will go over some type-specific stuff. Please wait...')

        if ch_type == 'category':
            await c.send('No type-specific settings for categories.')

        if ch_type in ['text', 'voice']:
            await c.send('What category should this be in?\n'\
            'Please type the name. If no category is needed, type `none`')

            ms = await client.wait_for('message',
            check=lambda s: s.author.id == m.id
            and (discord.utils.find(lambda x: x.name == s.content, g.channels)
            or s.content == 'none'))

            if ms.content != 'none':
                ch['category'] = discord.utils.find(lambda x: x.name == ms.content, g.channels)
                await c.send(f'Set channel category to {ch["category"]}.')

        if ch_type == 'text':
            await c.send('What topic do you want?')

            ms = await client.wait_for('message',
            check=lambda s: s.author.id == m.id)

            ch['topic'] = ms.content

            await c.send('Alright. Should this be an NSFW channel?\n'\
            'Like before, type `y` if so and `n` if not.')

            ms = await client.wait_for('message',
            check=lambda s: s.author.id == m.id and s.content in ['y', 'n'])

            if ms.content == 'y':
                ch['nsfw'] = True
            else:
                ch['nsfw'] = False

        nl = '\n'
        await c.send('Alright, now let\'s review your current settings:```'\
        f'type: {ch_type}\n{nl.join(list(map(lambda x: f"{x[0]}: {x[1]}", list(ch.items()))))}'\
        '```Are these settings good? NOTE: If not, you will have to restart the *entire* '\
        'channel setup. It is recommended to manually change these after creation.\n'\
        'Please type `y` if they are okay, and `n` if not.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id and s.content in ['y', 'n'])

        if ms.content == 'y':
            await c.send('Alright. Creating the role now, please wait...')

            if ch_type == 'text':
                gfunc = g.create_text_channel
            elif ch_type == 'voice':
                gfunc = g.create_voice_channel
            else:
                gfunc = g.create_category_channel
                chpos = ch['position']
                del ch['position']
            try:
                newch = await gfunc(overwrites=overwrite, **ch)
                if ch_type == 'category':
                    newch.edit(position=chpos)
                await c.send('Successfully created channel!')
            except Exception as e:
                await c.send('Failed to create channel:\n'\
                f'{e}\nPlease contact the owner with details of this immediately. '\
                'Aborting, please recreate this channel.')
                continue

async def overwrites(g, c, m, client):
    configed_role_ids = []
    overwrites = []
    while True:
        await c.send('First, what role do you want this to be for?\n'\
        'Please ping the role, or `@everyone` for default permissions.\n'\
        'If you don\'t need any more overwrites, please type `stop` now.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id and
        (len(s.role_mentions) > 0 or s.mention_everyone) or s.content == 'stop')

        if ms.content == 'stop':
            await c.send('Stopping permissions overwrite handler, please wait...')
            break

        if len(ms.role_mentions) > 0:
            ment = ms.role_mentions[0]
        else:
            ment = g.default_role
        print(ment.id)
        if ment.id in configed_role_ids:
            await c.send('This role has already been configured!')
            continue

        await c.send('Good. Now, what permissions do you want to *allow*?\n'\
        'To view allowed values, please check '\
        'https://github.com/binex-dsk/law-enforcer/blob/master/perms.txt.\n'\
        'Please provide the permissions in a space-separated manner.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id)

        allow = list(filter(lambda x: x in allowed_perms, ms.content.split()))

        if len(allow) < 1:
            await c.send('No valid permissions were provided.\n'\
            'No permissions will be allowed for this role.')

        await c.send('Now, what permissions do you want to *deny*?\n'\
        'To view allowed values, please check .\n'\
        'Please provide the permissions in a space-separated manner.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id)

        deny = list(filter(lambda x: x in allowed_perms, ms.content.split()))

        if len(deny) < 1:
            await c.send('No valid permissions were provided.\n'\
            'No permissions will be denied for this role.')

        allow_dict = {i : True for i in allow}
        deny_dict = {i : False for i in deny}

        full_perms = dict(allow_dict)
        full_perms.update(deny_dict)


        await c.send('Alright! Here are the permission overwrites.```'\
        f'Allowed: {" ".join(allow)}\nDenied: {" ".join(deny)}```'\
        'If these are good, type `y`, otherwise, type `n`.\n'\
        'NOTE: If these are incorrect, you will have to redo this overwrite.')

        ms = await client.wait_for('message',
        check=lambda s: s.author.id == m.id and s.content in ['y', 'n'])

        if ms.content == 'n':
            continue

        overwrites.append((ment, discord.PermissionOverwrite(**full_perms)))

        configed_role_ids.append(ment.id)

        await c.send('Overwrites added.')

    return overwrites
