import discord, random, sys
from . import __dict__ as commands
from groups import __dict__ as groups
from constants.auth import ids, prefix
from constants.resp import helpCmd

no_docs = True

async def run(env):
    args = env['args']
    client = env['client']
    g = env['g']
    c = env['c']
    m = env['m']

    # initialize an embed
    helpEmb = discord.Embed()
    # get 2 random ids from the owners
    id1 = f"<@{ids[random.randint(0, 1)]}>"
    id2 = f"<@{ids[random.randint(0, 1)]}>"

    cmd = None
    if len(args) > 0: 
        cmd = commands.get(args[0])
    if not len(args) > 0:
        helpEmb.set_author(name="Invite me here!", url=discord.utils.oauth_url(client.user.id,
        permissions=discord.Permissions(permissions=268561591)), icon_url=client.user.avatar_url)
        helpEmb.title = "All commands"
        helpEmb.description = "This is a list of all groups and their commands."
        for group in list(filter(lambda x: (type(x) == type(discord)), groups.values())):
            # i could do this way better but im too lazy
            helpEmb.add_field(name=group.name, value=f"{group.description}\n`{'`, `'.join(group.commands)}`", inline=False)
        helpEmb.set_footer(text="Law Enforcer v0.9", icon_url=client.user.avatar_url)
    elif cmd:
        if cmd.no_docs:
            return await c.send("The command you entered exists but lacks documentation. If you believe this is in error, contact an owner.")
        ex1 = cmd.ex1
        ex2 = cmd.ex2
        if type(ex1) == str:
            ex1 = ex1.replace("id1", id1)
            ex2 = ex2.replace("id2", id2)
        helpEmb = helpCmd(helpEmb, cmd.name, cmd.long, cmd.syntax, 
        ex1, ex2, cmd.notes, cmd.reqperms)
    # no valid command? go here
    else:
        helpEmb.title = "Invalid command!"
        helpEmb.description = f"The command you entered, {args[0]}, is invalid."
        helpEmb.set_footer(text=f"Use {prefix}help for a list of commands.", icon_url=client.user.avatar_url)
    await c.send(embed=helpEmb)

