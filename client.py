import discord, json, math, asyncio, ast, random, subprocess, os
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine

from constants.auth import token, prefix, game, ids
from constants.info import oauth, staticinfo, endinfo
from constants.resp import botlower, userlower, owneronly, userperms, botperms
from constants.help import helpCmd

from commands import __dict__ as commands

client = discord.Client()

startTime = 0
conn = None
meta = None
tagsEngine = None
tags = None
rolesConn = None
rolesEngine = None
muted_roles = None
@client.event
async def on_ready():
    global startTime, conn, meta, tagsEngine, tags, rolesConn, rolesEngine, muted_roles
    # used for uptime
    startTime = datetime.now()
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))
    print("Successfully logged in.")
    tagsEngine = create_engine('sqlite:///tags.db')
    rolesEngine = create_engine('sqlite:///roles.db')
    meta = MetaData()
    conn = tagsEngine.connect()
    rolesConn = rolesEngine.connect()
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
    meta.create_all(tagsEngine)
    meta.create_all(rolesEngine)


@client.event
async def on_message(msg):
    # initialize muted role
    muted_role = False
    # ignore bots
    if msg.author.bot:
        return
    # ignore messages not starting with our prefix
    if not msg.content.startswith(prefix):
        return
    # the actual arguments
    args = msg.content[len(prefix):len(msg.content)].strip().split(" ")
    # get the command
    cmd = args[0].lower()
    # remove the command from args
    args.pop(0)
    # used for shortening code
    c = msg.channel
    g = msg.guild
    m = msg.author
    # grabs the guild muted role
    if not muted_role: 
        for role in g.roles:
            if role.name.lower() == "muted":
                muted_role = role
                break
    command = commands.get(cmd)
    if not command:
        return
    await command.run(args=args, msg=msg, client=client, g=g, c=c, m=m, botlower=botlower,
    userlower=userlower, botperms=botperms, userperms=userperms, owneronly=owneronly, ids=ids, 
    helpCmd=helpCmd, oauth=oauth, startTime=startTime, staticinfo=staticinfo, endinfo=endinfo, 
    muted_role=muted_role, conn=conn, rolesconn=rolesConn,tags=tags, muted_roles=muted_roles, prefix=prefix)
    
# tries to login with the token
try:
    client.run(token)
# if it fails, print the error
except discord.errors.LoginFailure as err:
    print(f"Failed to login. Token: {token}\n{err}")
