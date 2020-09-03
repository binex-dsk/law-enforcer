from types import ModuleType
from commands import __dict__ as commands
import random, discord

from groups import __dict__ as groups
from constants.auth import ids, prefix

names = ['help']
no_docs = True
reqargs = ['args', 'client', 'c']

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    # initialize an helpEmbed
    helpEmb = discord.Embed()
    # get 2 random ids from the owners
    id1 = f'<@{ids[random.randint(0, 1)]}>'
    id2 = f'<@{ids[random.randint(0, 1)]}>'

    cmd = None
    if len(args) > 0:
        cmd = discord.utils.find(lambda cm: args[0] in cm.names,
        list(filter(lambda x: isinstance(x, ModuleType), list(commands.values()))))

    if not len(args) > 0:
        helpEmb.set_author(name='Invite me here!', url=discord.utils.oauth_url(client.user.id,
        permissions=discord.Permissions(permissions=268561591)), icon_url=client.user.avatar_url)

        helpEmb.title = 'All commands'

        helpEmb.description = 'This is a list of all groups and their commands.'

        [helpEmb.add_field(name=group.name, value=f'{group.description}\n`{"`, `".join(group.commands)}`', inline=False) for group in [x for x in groups.values()if isinstance(x, ModuleType)]]

        helpEmb.set_footer(text='Law Enforcer v1.4.0', icon_url=client.user.avatar_url)

    elif cmd:
        if hasattr(cmd, 'no_docs'):
            return await c.send('The command you entered exists but lacks documentation. '\
            'If you believe this is in error, contact the owner.')
        if hasattr(cmd, 'examples'):
            examples = [x.replace('id1', id1).replace('id2', id2) for x in cmd.examples]
        nl = '\n'
        escpref = f'\\{prefix}'
        helpEmb.title = cmd.name
        helpEmb.description = cmd.desc
        if hasattr(cmd, 'cargs'):
            helpEmb.add_field(name='Usage', value=f'\\{prefix}{cmd.name} ' + ' '.join(f'({x["name"]})' if not x['optional'] else f'[{x["name"]} || {x["default"]}]' for x in cmd.cargs), inline=False)
        else:
            helpEmb.add_field(name='Usage', value=f'\\{prefix}{cmd.name}', inline=False)
        if examples:
            helpEmb.add_field(name='Examples',
            value='\n'.join(f'{escpref}{cmd.name} {x}' for x in cmd.examples), inline=False)
        if hasattr(cmd, 'names') and len(cmd.names) > 1:
            helpEmb.add_field(name='Aliases',
            value=f'\\{prefix}{f"{nl}{escpref}".join(cmd.names[1:])}', inline=False)
        if hasattr(cmd, 'notes'):
            helpEmb.add_field(name='Extra Notes', value=cmd.notes)
        if hasattr(cmd, 'reqperms'):
            helpEmb.add_field(name='Required Permissions', value='\n'.join(q.upper().replace(' ', '_') for q in cmd.reqperms))
    # no valid command? go here
    else:
        helpEmb.title = 'Invalid command!'

        helpEmb.description = f'The command you entered, {args[0]}, is invalid.'

        helpEmb.set_footer(text=f'Use {prefix}help for a list of commands.',
        icon_url=client.user.avatar_url)

    await c.send(embed=helpEmb)
