from commands import __dict__ as cmds
from types import ModuleType
from init import client

import calendar, time
from datetime import datetime, timedelta

from thread import Thread
import discord

from constants.auth import token, prefix, game
from constants import db, checks
from tables import muted_roles, muted_members, server_config, tags, conn

def hasval(dictt, val):
    try:
        dictt[val]
        return True
    except:
        return False

client.start_time = None
start = time.time()
@client.event
async def on_ready():
    print(time.time() - start)
    # used for uptime
    client.start_time = datetime.now()

    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))
    print('Successfully logged in.')
    Thread.start(block=False)

@client.event
async def on_message(msg):
    # ignore bots
    if msg.author.bot:
        return
    # the actual arguments
    args = msg.content[len(prefix):].strip().split(' ')

    # get the command
    cmd = args.pop(0).lower()

    # used for shortening code
    c = msg.channel
    g = msg.guild
    m = msg.author

    conf = db.fetch(server_config, {'guild': g.id}).fetchone()
    # extremely inefficient system but idgaf
    if not 'tag' in cmd:
        if (tagss := db.fetch(tags, {'guild': msg.guild.id})):
            tagls = tagss.fetchall()
            if not conf.tag_require_command:
                if conf.tag_search_all:
                    found = [x.content for x in [x for x in tagls if msg.content.find(x.name) != -1]]
                else:
                    found = [x.content for x in [x for x in tagls if msg.content == x.name]]
                if len(found) > 0:
                    return await msg.channel.send(found[0])

    # ignore messages not starting with our prefix
    if not msg.content.startswith(prefix):
        return

    if cmd in conf.disabled_cmds.split():
        return await c.send('This command exists, but has been disabled. Please contact the admins if you believe this is in error.')

    command = discord.utils.find(lambda cm: cmd in cm.names, [x for x in list(cmds.values()) if isinstance(x, ModuleType)])
    if not command:
        return

    if hasattr(command, 'reqperms'):
        try:
            await checks.perms([s.replace(' ', '_') for s in command.reqperms], g, c, m)
        except:
            return
    if hasattr(command, 'owner_only'):
        try:
            await checks.owner(c, m)
        except:
            return

    locals()['client'] = client
    env = {}
    for r in command.reqargs:
        lc = locals().get(r)
        env.update({r: lc})
    # and this, folks, is the most retarded thing I have ever written, and probably one of the most unnecessarily complicated ones.
    # I wish I could've made a better one but I already spent 5 hours on this so yeah no
    if hasattr(command, 'cargs'):
        ca = command.cargs
        if len([x for x in ca if not x['optional']]) > len(args):
            return await c.send(f'This command requires more arguments. You are missing the '\
            f'`{ca[len(args)]["name"]}` argument. Please use `{prefix}help {cmd}` for help.')
        for x, arg in enumerate(ca):
            varname = None
            checked = None
            if not hasval(arg, 'novar'):
                varname = arg['name'] if not hasval(arg, 'aname') else arg['aname']
            print(arg)
            if hasval(arg, 'check'):
                if len(args) >= x + 1:
                    if hasval(arg, 'excarg'):
                        checked = arg['check'](args[x], locals().get(arg['excarg']))
                    else:
                        checked = arg['check'](args[x])
                    if not checked:
                        return await c.send(arg['errmsg'])
            if varname:
                print(varname, checked)
                if checked:
                    toupd = {varname: checked}
                else:
                    if ca[-1] == arg:
                        toupd = {varname: ' '.join(args[x:]) or arg['default']}
                    else:
                        toupd = {varname: args[x] if len(args) >= x + 1 else arg['default']}
                print(toupd)
                env.update(toupd)
                
    try:
        await command.run(**env)
    except Exception as e:
        await c.send(f'Error during command execution:\n{e}\n'\
        'Please contact the owner with details of this error immediately.')
        print(e)

# to prevent mute evasion!
@client.event
async def on_member_join(m):
    mgc = db.fetch(server_config, {'guild': m.guild.id}).fetchone()
    if mgc.mute_evasion:
        muted = conn.execute(muted_members.select().where(muted_members.c.unmute_after <= int(time.time())).where(muted_members.c.id == m.id)).fetchone()

        if muted:
            await m.add_roles(db.fetch(muted_roles, {'guild': m.guild.id}), f'Mute evasion; added {mgc.mute_evasion_time} hours to mute time.')
            db.update(muted_members, {'id': m.id}, {'unmute_after': calendar.timegm((muted.unmute_after + timedelta(hours=mgc.mute_evasion_time).timetuple()))})
            try:
                await m.send(f'Looks like you were mute evading in {m.guild}.\nYour mute time has been extended by {mgc.mute_evasion_time} hours. If you believe this is in error, please contact the admins/mods of the server.')
            except:
                pass

@client.event
async def on_guild_join(g):
    try:
        db.insert(server_config, {'guild': g.id})
    except:
        pass
if __name__ == '__main__':
    # tries to login with the token
    try:
        client.run(token)
    # if it fails, print the error
    except discord.errors.LoginFailure as err:
        print(f'Failed to login. Token: {token}\n{err}')
