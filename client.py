from commands import __dict__ as cmds
from types import ModuleType

import calendar, time
from datetime import datetime, timedelta

import thread
import discord

from constants.auth import token, prefix, game
from constants import db
from tables import conn, tags, muted_roles, muted_members

client = discord.Client()

start_time = 0

@client.event
async def on_ready():
    global start_time
    # used for uptime
    start_time = datetime.now()

    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))
    print('Successfully logged in.')
    await thread.checkMutes(client)

@client.event
async def on_message(msg):
    # ignore bots
    if msg.author.bot:
        return

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
    muted = muted_members.select().where(muted_members.c.unmute_after <= int(time.time())).where(muted_members.c.id == m.id)

    if muted:
        await m.add_roles(db.fetch(muted_roles, {'guild': m.guild.id}), 'Mute evasion; added 12 hours to mute time.')
        db.update(muted_members, {'id': m.id}, {'unmute_after': calendar.timegm((muted.unmute_after + timedelta(hours=12).timetuple()))})
        try:
            await m.send(f'Nice try mute evading in {m.guild}. Sorry, but your mute time has been extended by 12 hours. If you believe this is in error, please contact the admins/mods of the server.')
        except:
            pass
    
# tries to login with the token
try:
    client.run(token)
# if it fails, print the error
except discord.errors.LoginFailure as err:
    print(f'Failed to login. Token: {token}\n{err}')
