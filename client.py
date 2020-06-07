from commands import __dict__ as commands

from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
import discord

from constants.auth import token, prefix, game

client = discord.Client()

start_time = 0
conn = None
meta = None
engine = None
tags = None
muted_roles = None

@client.event
async def on_ready():
    global start_time, conn, meta, engine, tags, muted_roles

    # used for uptime
    start_time = datetime.now()

    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))
    print('Successfully logged in.')

    engine = create_engine('sqlite:///database.db')
    meta = MetaData()
    conn = engine.connect()
    tags = Table(
        'tags', meta,
        Column('name', String, primary_key=True),
        Column('content', String),
        Column('creatortag', String),
        Column('creatorid', Integer),
        Column('createdat', String),
        Column('guild', Integer)
    )
    muted_roles = Table(
        'muted_roles', meta,
        Column('id', Integer),
        Column('guild', Integer)
    )

    meta.create_all(engine)

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

    command = commands.get(cmd)
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
        'start_time': start_time,
        'conn': conn,
        'tags': tags,
        'muted_roles': muted_roles
    }
    try:
        await command.run(env)
    except Exception as e:
        await c.send(f'Error during command execution:\n{e}\n'\
        'Please contact the owner with details of this error immediately.')
        print(e)

# tries to login with the token
try:
    client.run(token)
# if it fails, print the error
except discord.errors.LoginFailure as err:
    print(f'Failed to login. Token: {token}\n{err}')
