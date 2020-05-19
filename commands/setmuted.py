import discord

name = 'setmuted'
long = 'Set the muted role for the server.'
syntax = "(role ID)"
ex1 = "705538476698763324"
ex2 = "644334910810619924"
notes = "The usage of the `mute` and `unmute` commands will not be available until this is used."
reqperms = "`manage server`\n`manage roles`"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    m = kwargs['m']
    args = kwargs['args']
    conn = kwargs['rolesconn']
    roles = kwargs['muted_roles']
    if not g.me.guild_permissions.manage_guild:
        return await c.send(kwargs['botperms']('manage the server'))
    if not m.guild_permissions.manage_guild:
        return await c.send(kwargs['userperms']('manage_guild'))
    if not g.me.guild_permissions.manage_roles:
        return await c.send(kwargs['botperms']('manage roles'))
    if not m.guild_permissions.manage_roles:
        return await c.send(kwargs['userperms']('manage_roles'))
    if len(args) < 1:
        return await c.send("Please provide a role ID.")
    role = discord.utils.get(g.roles, id=int(args[0]))
    if not role:
        return await c.send("This role is not present in the server.")
    gm = roles.select().where(roles.c.guild==g.id)
    result = conn.execute(gm)
    row = None
    try:
        row = result.fetchone()
    except:
        pass
    if row:
        try:
            conn.execute(roles.update().where(roles.c.guild==g.id).values(id=args[0]))
            return await c.send(f"Successfully set muted role to {role.mention}.")
        except Exception as e:
            return await c.send("Error while setting muted role:\n" + e)
    else:
        try:
            conn.execute(roles.insert(), [
                {'id': args[0], 'guild': g.id}
            ])
            return await c.send(f"Successfully set muted role to {role.mention}.")
        except Exception as e:
            return await c.send("Error while setting muted role:\n" + e)
    
