from types import ModuleType
from commands import __dict__ as cmds
import discord
from tables import server_config
from constants import db

name = 'config'
names = ['config', 'serverconfig']
desc = 'Configure various commands and settings.'
notes = 'Unlike server setup, this utilizes embeds and message editing/deleting, making it easier to understand and use.'
reqperms = ['administrator']
reqargs = ['client', 'g', 'c', 'm']

def gval(to_upd, opt, row):
    return f"{to_upd.get(row)}" if f"{to_upd.get(row)}" != "None" else f"{opt[row]}"

async def awaitmsg(client, m, contents):
    cfm = await client.wait_for('message', check=lambda x: x.author.id == m.id and x.content.lower() in contents)

    await cfm.delete()

    return cfm


def addfield(embed, name, value):
    return embed.add_field(name=name, value=value, inline=False)


def setbase(embed, title, desc):
    embed.clear_fields()
    embed.title = title
    embed.description = desc


async def int_base(conf_emb, emb, name, sub, msg, min, max, client, to_upd, opt, val, m):
    setbase(conf_emb, f'{name} -- {sub}',
            f'{msg}\nCurrent value: `{opt[val]}`\nPlease type new value. Must be an integer between {min} and {max}.')

    await emb.edit(embed=conf_emb)

    cfm = await client.wait_for('message', check=lambda x: x.author.id == m.id and x.content.isdigit() and min <= int(x.content) <= max)

    await cfm.delete()

    cc = cfm.content.lower()

    to_upd.update({val: int(cc)})


async def tf_base(conf_emb, emb, name, sub, msg, val, opt, client, m, to_upd):
    setbase(conf_emb, f'{name} -- {sub}',
            f'{msg}\nCurrent value: `{opt[val]}`\nPlease type new value. Must be "true" or "false".')

    await emb.edit(embed=conf_emb)

    cfm = await awaitmsg(client, m, ['true', 'false'])

    cc = cfm.content.lower()
    if cc == 'true':
        to_upd.update({val: True})
    else:
        to_upd.update({val: False})

async def subst_base(conf_emb, emb, name, sub, msg, val, subst, opt, client, m, to_upd):
    setbase(conf_emb, f'{name} -- {sub}',
            f'{msg}\nCurrent value: ```{opt[val]}```\nPlease type new value. Substitutions:\n{subst}.')

    await emb.edit(embed=conf_emb)

    cfm = await client.wait_for('message', check=lambda x: x.author.id == m.id)

    await cfm.delete()

    cc = cfm.content

    to_upd.update({val: cc})


async def ban(client, m, emb, conf_emb, opt, to_upd, un=False):
    lst = ['dm', 'message', 'back']
    if un:
        mt = "Unban"
    else:
        mt = "Ban"
        lst.append('deletion')
    mtl = mt.lower()

    setbase(conf_emb, f'{mt} Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    if not un:
        addfield(conf_emb, 'Message Deletion Days (deletion)', gval(to_upd, opt, 'ban_delete_days'))
    addfield(conf_emb, f'DM User upon {mtl}? (dm)', gval(to_upd, opt, f'{mtl}_dm'))
    addfield(conf_emb, 'DM Message, I/A (message)', gval(to_upd, opt, f'{mtl}_dm_message'))

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, lst)

    cc = cfm.content.lower()

    if cc == 'deletion':
        await int_base(conf_emb, emb, 'Ban Command', 'Message Deletion Days', 'How many days of messages will be deleted when a user is banned?', 0, 7, client, to_upd, opt, 'ban_delete_days', m)
    elif cc == 'dm':
        await tf_base(conf_emb, emb, f'{mt} Command', 'DM User', f'Should the user be DMed upon {mtl}?', f'{mtl}_dm', opt, client, m, to_upd)
    elif cc == 'message':
        await subst_base(conf_emb, emb, f'{mt} Command', 'DM Message', f'What message should be sent to the user upon being {mtl}ned?', f'{mtl}_dm_message', '{MEM}: member being {mtl}ned\n{GUILD}: server name\n{MOD}: responsible moderator\n{REASON}: reason for {mtl}'.format(MEM='\{MEM}', mtl=mtl, GUILD='\{GUILD}', MOD='\{MOD}', REASON='\{REASON}'), opt, client, m, to_upd)
    else:
        return await commands(client, m, emb, conf_emb, opt, to_upd)
    await ban(client, m, emb, conf_emb, opt, to_upd, un=un)


async def kick(client, m, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Kick Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'DM User upon kick? (dm)', gval(to_upd, opt, 'kick_dm'))
    addfield(conf_emb, 'DM Message, I/A (message)', gval(to_upd, opt, 'kick_dm_message'))
    addfield(conf_emb, 'DM User an invite, I/A? (inv)', gval(to_upd, opt, 'kick_dm_invite'))
    addfield(conf_emb, 'DM Invite Message, I/A (invitemessage)', gval(to_upd, opt, 'kick_dm_inv_message'))

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['dm', 'message', 'inv', 'invitemessage', 'back'])

    cc = cfm.content.lower()

    if cc == 'dm':
        await tf_base(conf_emb, emb, 'Kick Command', 'DM User', 'Should the user be DMed upon kick?', 'kick_dm', opt, client, m, to_upd)
    elif cc == 'message':
        await subst_base(conf_emb, emb, 'Kick Command', 'DM Message', 'What message should be sent to the user upon being kicked?', 'kick_dm_message', '\{MEM}: member being banned\n\{GUILD}: server name\n\{MOD}: responsible moderator\n\{REASON}: reason for ban\n\{INV}: invite (I/A)', opt, client, m, to_upd)
    elif cc == 'inv':
        await tf_base(conf_emb, emb, 'Kick Command', 'DM Invite', 'Should the user be DMed an Invite upon being kicked?', 'kick_dm_invite', opt, client, m, to_upd)
    elif cc == 'invitemessage':
        await subst_base(conf_emb, emb, 'Kick Command', 'DM Invite Message', 'What message should be sent with the invite to the user being kicked (I/A)?', 'kick_dm_inv_message', '\{INV}: invite', opt, client, m, to_upd)
    else:
        return await commands(client, m, emb, conf_emb, opt, to_upd)
    await kick(client, m, emb, conf_emb, opt, to_upd)


async def mute(client, m, emb, conf_emb, opt, to_upd, un=False):
    subs = '\{MEM}: member being muted\n\{GUILD}: server name\n\{MOD}: responsible moderator\n'
    if un:
        mt = "Unmute"
    else:
        mt = "Mute"
        subs += '\{TIME}: time in hours of mute\n'
    mtl = mt.lower()
    subs += '\{REASON}: reason for mute'

    setbase(conf_emb, f'{mt} Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'DM User upon mute? (dm)', gval(to_upd, opt, f'{mtl}_dm'))
    addfield(conf_emb, 'DM Message, I/A (message)', gval(to_upd, opt, f'{mtl}_dm_message'))

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['dm', 'message', 'back'])

    cc = cfm.content.lower()

    if cc == 'dm':
        await tf_base(conf_emb, emb, f'{mt} Command', 'DM User', 'Should the user be DMed upon {mtl}?', f'{mtl}_dm', opt, client, m, to_upd)
    elif cc == 'message':
        await subst_base(conf_emb, emb, f'{mt} Command', 'DM Message', f'What message should be sent to the user upon being {mtl}d?', f'{mtl}_dm_message', subs, opt, client, m, to_upd)
    else:
        return await commands(client, m, emb, conf_emb, opt, to_upd)
    await mute(client, m, emb, conf_emb, opt, to_upd, un=un)

async def tags(client, m, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Tags Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'Require command to activate? (reqcmd)', gval(to_upd, opt, 'tag_require_command'))
    addfield(conf_emb, 'Search the whole message? (search)', gval(to_upd, opt, 'tag_search_all'))
    addfield(conf_emb, 'Allow all to use addtag? (allow)', gval(to_upd, opt, 'allow_all_addtag'))

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['reqcmd', 'search', 'allow', 'back'])

    cc = cfm.content.lower()

    if cc == 'reqcmd':
        await tf_base(conf_emb, emb, 'Tag Command', 'Require Command Usage', 'Should the `~~tag` command have to be used in order to trigger?', 'tag_require_command', opt, client, m, to_upd)
    elif cc == 'search':
        await tf_base(conf_emb, emb, 'Tag Command', 'Search Whole Message', 'Should the entire message be searched for the tag (I/A)?', 'tag_search_all', opt, client, m, to_upd)
    elif cc == 'allow':
        await tf_base(conf_emb, emb, 'Tag Command', 'Allow All to use Addtag', 'Should ALL members be allowed to use `~~addtag`?', 'allow_all_addtag', opt, client, m, to_upd)
    else:
        return await commands(client, m, emb, conf_emb, opt, to_upd)
    await tags(client, m, emb, conf_emb, opt, to_upd)


async def clear(client, m, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Clear Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'Delete pinned messages? (delpins)', gval(to_upd, opt, 'clear_delete_pinned'))

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['delpins', 'back'])

    cc = cfm.content.lower()

    if cc == 'delpins':
        await tf_base(conf_emb, emb, 'Clear Command', 'Delete Pins', 'Should pinned messages be deleted?', 'clear_delete_pinned', opt, client, m, to_upd)
    else:
        return await commands(client, m, emb, conf_emb, opt, to_upd)
    await clear(client, m, emb, conf_emb, opt, to_upd)


async def main(client, m, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Server Configuration',
            'Welcome to the interactive server configuration module!\nPlease choose the module to enter by typing its name.')
    addfield(conf_emb, 'Commands', 'Individual command configuration.')
    addfield(conf_emb, 'Other', 'General configuration settings.')
    conf_emb.set_footer(text='Type "back" to go back at any time.')
    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['commands', 'other', 'back'])

    cc = cfm.content.lower()

    if cc == 'commands':
        await commands(client, m, emb, conf_emb, opt, to_upd)
    if cc == 'other':
        await others(client, m, emb, conf_emb, opt, to_upd)
    else:
        return await final(emb, conf_emb, opt, to_upd)


async def others(client, m, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Other Configuration',
            'Configure other settings.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'Punish Mute Evasion? (muteev)', gval(to_upd, opt, 'mute_evasion'))
    addfield(conf_emb, 'Mute Evasion Timeout (mutetime)', gval(to_upd, opt, 'mute_evasion_time'))
    addfield(conf_emb, 'Disabled Commands (disabled)', gval(to_upd, opt, 'disabled_cmds') or 'None')

    await emb.edit(embed=conf_emb)

    cfm = await awaitmsg(client, m, ['muteev', 'mutetime', 'disabled', 'back'])

    cc = cfm.content.lower()

    if cc == 'muteev':
        await tf_base(conf_emb, emb, 'Other Configuration', 'Mute Evasion', 'Should mute evasion be punished?', 'mute_evasion', opt, client, m, to_upd)
    elif cc == 'mutetime':
        await int_base(conf_emb, emb, 'Other Configuration', 'Mute Evasion Timeout', 'How many extra hours should be added to mute duration for mute evaders?', 1, 24, client, to_upd, opt, 'mute_evasion_time', m)
    elif cc == 'disabled':
        setbase(conf_emb, 'Disabled Commands',
            f'What commands do you want to disable?\nCurrent value: ```{opt.disabled_cmds or None}```\nPlease type commands to disable in a space-separated format. Use `~~help` in another channel to view available commands.')

        await emb.edit(embed=conf_emb)

        cfm = await client.wait_for('message', check=lambda x: x.author.id == m.id)

        await cfm.delete()

        cc = cfm.content

        cs = cc.split()
        for [s, ss] in enumerate(cs):
            if f'commands.{ss}' not in [x.__name__ for x in list(cmds.values()) if isinstance(x, ModuleType)]:
                del cs[s]

        to_upd.update({'disabled_cmds': ' '.join(cs)})
    else:
        return await main(client, m, emb, conf_emb, opt, to_upd)
    await others(client, m, emb, conf_emb, opt, to_upd)


async def commands(client, m, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Command Configuration',
            'Configure individual command settings.\nCommands:\nBan\nUnban\nKick\nMute\nUnmute\nTags\nClear')

    await emb.edit(embed=conf_emb)

    cfm = await awaitmsg(client, m, ['ban', 'unban', 'kick', 'mute', 'unmute', 'tags', 'clear', 'back'])

    cc = cfm.content.lower()

    if cc == 'ban':
        await ban(client, m, emb, conf_emb, opt, to_upd)
    if cc == 'unban':
        await ban(client, m, emb, conf_emb, opt, to_upd, un=True)
    if cc == 'kick':
        await kick(client, m, emb, conf_emb, opt, to_upd)
    if cc == 'mute':
        await mute(client, m, emb, conf_emb, opt, to_upd)
    if cc == 'unmute':
        await mute(client, m, emb, conf_emb, opt, to_upd, un=True)
    if cc == 'tags':
        await tags(client, m, emb, conf_emb, opt, to_upd)
    if cc == 'clear':
        await clear(client, m, emb, conf_emb, opt, to_upd)
    else:
        return await main(client, m, emb, conf_emb, opt, to_upd)

async def final(emb, conf_emb, opt, to_upd,):
    setbase(conf_emb, 'Final Settings', 'Thank you for using the interactive configuration!\nI am applying your settings. Meanwhile, please `~~contact` my master for bugs, issues, suggestions, etc. on this, as he is unfortunately not able to fully test this. Thank you!')
    conf_emb.set_footer(text='Thanks for using this!')
    await emb.edit(embed=conf_emb)
    
    try:
        db.update(server_config, {'guild': opt.guild}, to_upd)
    except:
        pass

    setbase(conf_emb, 'Finished', 'Settings have been applied. Once again, PLEASE contact the owner with any feedback or issues. Also once again, thank you!')
    return await emb.edit(embed=conf_emb)

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    opt = db.fetch(server_config, {'guild': g.id}).fetchone()
    conf_emb = discord.Embed()

    to_upd = {}

    setbase(conf_emb, 'Server Configuration', 'Welcome to the interactive server configuration module!\nPlease choose the module to enter by typing its name.')
    addfield(conf_emb, 'Commands', 'Individual command configuration.')
    addfield(conf_emb, 'Other', 'General configuration settings.')
    conf_emb.set_footer(text='Type "back" to go back at any time.')
    emb = await c.send(embed=conf_emb)

    await main(client, m, emb, conf_emb, opt, to_upd)
