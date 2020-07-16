from tables import server_config
import constants.db as db
import discord

name = 'config'
names = ['config', 'serverconfig']
long = 'Configure various commands and settings.'
syntax = ''
ex1 = None
ex2 = None
notes = 'Unlike server setup, this utilizes embeds and message editing/deleting, making it easier to understand and use.'
reqperms = '`administrator`'
no_docs = False
arglength = 0


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


async def tf_base(conf_emb, emb, name, sub, msg, val, opt, awaitmsg, client, m, to_upd):
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


async def ban(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Ban Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'Message Deletion Days (deletion)', to_upd.get('ban_delete_days') or opt.ban_delete_days)
    addfield(conf_emb, 'DM User upon ban? (dm)', to_upd.get('ban_dm') or opt.ban_dm)
    addfield(conf_emb, 'DM Message, I/A (message)', to_upd.get('ban_dm_message') or opt.ban_dm_message)

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['deletion', 'dm', 'message', 'back'])

    cc = cfm.content.lower()

    if cc == 'deletion':
        await int_base(conf_emb, emb, 'Ban Command', 'Message Deletion Days', 'How many days of messages will be deleted when a user is banned?', 0, 7, client, to_upd, opt, 'ban_delete_days', m)
    elif cc == 'dm':
        await tf_base(conf_emb, emb, 'Ban Command', 'DM User', 'Should the user be DMed upon ban?', 'ban_dm', opt, awaitmsg, client, m, to_upd)
    elif cc == 'message':
        await subst_base(conf_emb, emb, 'Ban Command', 'DM Message', 'What message should be sent to the user upon being banned?', 'ban_dm_message', '\{MEM}: member being banned\n\{GUILD}: server name\n\{MOD}: responsible moderator\n\{REASON}: reason for ban', opt, client, m, to_upd)
    else:
        await commands(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    await ban(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)


async def kick(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Kick Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'DM User upon kick? (dm)', to_upd.get('kick_dm') or opt.kick_dm)
    addfield(conf_emb, 'DM Message, I/A (message)', to_upd.get('kick_dm_message') or opt.kick_dm_message)
    addfield(conf_emb, 'DM User an invite, I/A? (inv)', to_upd.get('kick_dm_invite') or opt.kick_dm_invite)
    addfield(conf_emb, 'DM Invite Message, I/A (invitemessage)',
             to_upd.get('kick_dm_inv_message') or opt.kick_dm_inv_message)

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['dm', 'message', 'inv', 'invitemessage', 'back'])

    cc = cfm.content.lower()

    if cc == 'dm':
        await tf_base(conf_emb, emb, 'Kick Command', 'DM User', 'Should the user be DMed upon kick?', 'kick_dm', opt, awaitmsg, client, m, to_upd)
    elif cc == 'message':
        await subst_base(conf_emb, emb, 'Kick Command', 'DM Message', 'What message should be sent to the user upon being kicked?', 'kick_dm_message', '\{MEM}: member being banned\n\{GUILD}: server name\n\{MOD}: responsible moderator\n\{REASON}: reason for ban\n\{INV}: invite (I/A)', opt, client, m, to_upd)
    elif cc == 'inv':
        await tf_base(conf_emb, emb, 'Kick Command', 'DM Invite', 'Should the user be DMed an Invite upon being kicked?', 'kick_dm_invite', opt, awaitmsg, client, m, to_upd)
    elif cc == 'invitemessage':
        await subst_base(conf_emb, emb, 'Kick Command', 'DM Invite Message', 'What message should be sent with the invite to the user being kicked (I/A)?', 'kick_dm_inv_message', '\{INV}: invite', opt, client, m, to_upd)
    else:
        await commands(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    await kick(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)


async def mute(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Mute Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'DM User upon mute? (dm)', to_upd.get('mute_dm') or opt.mute_dm)
    addfield(conf_emb, 'DM Message, I/A (message)', to_upd.get('mute_dm_message') or opt.mute_dm_message)

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['dm', 'message', 'back'])

    cc = cfm.content.lower()

    if cc == 'dm':
        await tf_base(conf_emb, emb, 'Mute Command', 'DM User', 'Should the user be DMed upon mute?', 'mute_dm', opt, awaitmsg, client, m, to_upd)
    elif cc == 'message':
        await subst_base(conf_emb, emb, 'Mute Command', 'DM Message', 'What message should be sent to the user upon being kicked?', 'mute_dm_message', '\{MEM}: member being banned\n\{GUILD}: server name\n\{MOD}: responsible moderator\n\{TIME}: time in hours of mute\n\{REASON}: reason for mute', opt, client, m, to_upd)
    else:
        await commands(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    await mute(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)


async def tags(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Tags Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'Require command to activate? (reqcmd)',
             opt.tag_require_command)
    addfield(conf_emb, 'Search the whole message? (search)', to_upd.get('tag_search_all') or opt.tag_search_all)
    addfield(conf_emb, 'Allow all to use addtag? (allow)', to_upd.get('allow_all_addtag') or opt.allow_all_addtag)

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['reqcmd', 'search', 'allow', 'back'])

    cc = cfm.content.lower()

    if cc == 'reqcmd':
        await tf_base(conf_emb, emb, 'Tag Command', 'Require Command Usage', 'Should the `~~tag` command have to be used in order to trigger?', 'tag_require_command', opt, awaitmsg, client, m, to_upd)
    elif cc == 'search':
        await tf_base(conf_emb, emb, 'Tag Command', 'Search Whole Message', 'Should the entire message be searched for the tag (I/A)?', 'tag_search_all', opt, awaitmsg, client, m, to_upd)
    elif cc == 'allow':
        await tf_base(conf_emb, emb, 'Tag Command', 'Allow All to use Addtag', 'Should ALL members be allowed to use `~~addtag`?', 'allow_all_addtag', opt, awaitmsg, client, m, to_upd)
    else:
        await commands(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    await tags(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)


async def clear(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Clear Configuration',
            'Configure the following options.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'Delete pinned messages? (delpins)',
             to_upd.get('clear_delete_pinned') or opt.clear_delete_pinned)

    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['delpins', 'back'])

    cc = cfm.content.lower()

    if cc == 'delpins':
        await tf_base(conf_emb, emb, 'Clear Command', 'Delete Pins', 'Should pinned messages be deleted?', 'clear_delete_pinned', opt, awaitmsg, client, m, to_upd)
    else:
        await commands(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    await clear(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)


async def main(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Server Configuration',
            'Welcome to the interactive server configuration module!\nPlease choose the module to enter by typing its name.')
    addfield(conf_emb, 'Commands', 'Individual command configuration.')
    addfield(conf_emb, 'Other', 'General configuration settings.')
    conf_emb.set_footer(text='Type "back" to go back at any time.')
    await emb.edit(embed=conf_emb)
    cfm = await awaitmsg(client, m, ['commands', 'other', 'back'])

    cc = cfm.content.lower()

    if cc == 'commands':
        await commands(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    if cc == 'other':
        await others(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    else:
        return await final(setbase, emb, conf_emb, opt, to_upd)


async def others(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Other Configuration',
            'Configure other settings.\nSyntax: OptionName (OptionMessage)\nType the OptionMessage to configure.')
    addfield(conf_emb, 'Mute Evasion (muteev)', to_upd.get('mute_evasion') or opt.mute_evasion)
    addfield(conf_emb, 'Mute Evasion Timeout (mutetime)', to_upd.get('mute_evasion_time') or opt.mute_evasion_time)

    await emb.edit(embed=conf_emb)

    cfm = await awaitmsg(client, m, ['muteev', 'mutetime', 'back'])

    cc = cfm.content.lower()

    if cc == 'muteev':
        await tf_base(conf_emb, emb, 'Other Configuration', 'Mute Evasion', 'Should mute evasion be punished?', 'mute_evasion', opt, awaitmsg, client, m, to_upd)
    elif cc == 'mutetime':
        await int_base(conf_emb, emb, 'Other Configuration', 'Mute Evasion Timeout', 'How many extra hours should be added to mute duration for mute evaders?', 1, 24, client, to_upd, opt, 'mute_evasion_time', m)
    else:
        await main(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)


async def commands(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Command Configuration',
            'Configure individual command settings.\nCommands:\nBan\nKick\nMute\nTags\nClear')

    await emb.edit(embed=conf_emb)

    cfm = await awaitmsg(client, m, ['ban', 'kick', 'mute', 'tags', 'clear', 'back'])

    cc = cfm.content.lower()

    if cc == 'ban':
        await ban(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    if cc == 'kick':
        await kick(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    if cc == 'mute':
        await mute(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    if cc == 'tags':
        await tags(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    if cc == 'clear':
        await clear(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
    else:
        await main(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)

async def final(setbase, emb, conf_emb, opt, to_upd):
    setbase(conf_emb, 'Final Settings', 'Thank you for using the interactive configuration!\nI am applying your settings. Meanwhile, please `~~contact` my master for bugs, issues, suggestions, etc. on this, as he is unfortunately not able to fully test this. Thank you!')
    conf_emb.set_footer(text='Thanks for using this!')
    await emb.edit(embed=conf_emb)

    db.update(server_config, {'guild': opt.guild}, to_upd)

    setbase(conf_emb, 'Finished', 'Settings have been applied. Once again, PLEASE contact the owner with any feedback or issues. Also once again, thank you!')
    await emb.edit(embed=conf_emb)
    exit(0)

async def run(env):
    client, g, c, m = [env[k] for k in ('client', 'g', 'c', 'm')]

    opt = db.fetch(server_config, {'guild': g.id}).fetchone()
    conf_emb = discord.Embed()

    to_upd = {}

    setbase(conf_emb, 'Server Configuration',
            'Welcome to the interactive server configuration module!\nPlease choose the module to enter by typing its name.')
    addfield(conf_emb, 'Commands', 'Individual command configuration.')
    addfield(conf_emb, 'Other', 'General configuration settings.')
    conf_emb.set_footer(text='Type "back" to go back at any time.')
    emb = await c.send(embed=conf_emb)

    await main(client, m, setbase, awaitmsg, emb, conf_emb, opt, to_upd)
