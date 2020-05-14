import discord, random
from commands import __dict__ as commands

no_docs = True

async def run(**kwargs):
    args = kwargs['args']
    c = kwargs['c']
    helpCmd = kwargs['helpCmd']
    # initialize an embed
    helpEmb = discord.Embed()
    ids = kwargs['ids']
    # get 2 random ids from the owners
    id1 = f"<@{ids[random.randint(0, 1)]}>"
    id2 = f"<@{ids[random.randint(0, 1)]}>"
    prefix = kwargs['prefix']

    cmd = None
    if len(args) > 0: 
        cmd = commands.get(f"{args[0]}C")
    if not len(args) > 0:
        helpEmb.set_author(name="Invite me here!", url=kwargs['oauth'], icon_url=kwargs['client'].user.avatar_url)
        helpEmb.title = "All commands"
        helpEmb.description = "Here is a list of all commands I have."
        # the 2 lines below just filter out the commands and stuff
        cmdlist = list(filter(lambda x: (type(x) == type(discord) and not x.no_docs), commands.values()))
        for command in cmdlist[int(len(cmdlist)/2):len(cmdlist)-1]:
            helpEmb.add_field(name=command.name, value=command.short, inline=False)
        helpEmb.set_footer(text="Law Enforcer v0.7", icon_url=kwargs['client'].user.avatar_url)

    elif cmd and not cmd.no_docs:
        helpEmb = helpCmd(helpEmb, cmd.name, cmd.long, cmd.syntax, 
        cmd.ex1.replace("id1", id1), cmd.ex2.replace("id2", id2), cmd.notes, cmd.reqperms)
    # no valid command? go here
    else:
        helpEmb.title = "Invalid command!"
        helpEmb.description = f"The command you entered, {args[0]}, is invalid."
        helpEmb.set_footer(text=f"Use {prefix}help for a list of commands.", icon_url=kwargs['client'].user.avatar_url)
    await c.send(embed=helpEmb)

