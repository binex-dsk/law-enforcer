from commands import __dict__ as cmds
from types import ModuleType

import calendar, time
from datetime import datetime, timedelta

from thread import Thread
import discord

from constants.auth import token, prefix, game
from constants import db
from tables import muted_roles, muted_members, server_config, tags, conn

client = discord.Client()

start_time = 0

@client.event
async def on_ready():
    for g in client.guilds:
        try:
            db.insert(server_config, {'guild': g.id})
        except:
            pass
    global start_time
    # used for uptime
    start_time = datetime.now()

    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))
    print('Successfully logged in.')
    Thread.start(client, block=False)

@client.event
async def on_message(msg):
    # ignore bots
    if msg.author.bot:
        return

    # extremely inefficient system but idgaf
    tagss = db.fetch(tags, {'guild': msg.guild.id})
    if tagss:
        conf = db.fetch(server_config, {'guild': msg.guild.id}).fetchone()
        tagls = tagss.fetchall()
        if not conf.tag_require_command:
            if conf.tag_search_all:
                found = [x.content for x in [x for x in tagls if msg.content.find(x.name) != -1]]

                if len(found) > 0:
                    return await msg.channel.send(found[0])
            else:
                found = [x.content for x in [x for x in tagls if msg.content == x.name]]

                if len(found) > 0:
                    return await msg.channel.send(found[0])


    # ignore messages not starting with our prefix
    if not msg.content.startswith(prefix):
        return

    # the actual arguments
    args = msg.content[len(prefix):len(msg.content)].strip().split(' ')

    # get the command
    cmd = args[0].lower()
    # remove the command from args
    args.pop(0)

    # used for shortening code
    c = msg.channel
    g = msg.guild
    m = msg.author

    if cmd in db.fetch(server_config, {'guild': g.id}).fetchone().disabled_cmds.split():
        return await c.send('This command exists, but has been disabled. Please contact the admins if you believe this is in error.')

    command = discord.utils.find(lambda cm: cmd in cm.names,
        [x for x in list(cmds.values()) if isinstance(x, ModuleType)])
    if not command:
        return
    # environment to run commands
    env = {
        'args': args,
        'msg': msg,
        'client': client,
        'g': g,
        'c': c,
        'm': m,
        'start_time': start_time
    }
    if command.arglength > len(args):
        return await c.send(f'This command requires more arguments. Please use '\
            f'`{prefix}help {command.name}` for more info.')
    try:
        await command.run(env)
    except Exception as e:
        await c.send(f'Error during command execution:\n{e}\n'\
        'Please contact the owner with details of this error immediately.')
        print(e)

# to prevent mute evasion!
@client.event
async def on_member_join(m):
    #db.insert(server_config, {'guild': m.guild.id})
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

# tries to login with the token
try:
    client.run(token)
# if it fails, print the error
except discord.errors.LoginFailure as err:
    print(f'Failed to login. Token: {token}\n{err}')
