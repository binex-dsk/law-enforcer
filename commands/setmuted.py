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
    conn = kwargs['conn']
    roles = kwargs['muted_roles']
    db = kwargs['db']
    checks = kwargs['checks']
    check = await checks.perms(['manage_guild', 'manage_roles'], g, c, m)
    if not check: return
    if len(args) < 1:
        return await c.send("Please provide a role ID.")
    role = discord.utils.get(g.roles, id=int(args[0]))
    if not role:
        return await c.send("This role is not present in the server.")
    fetched = db.fetch(roles, {'guild': g.id}, conn)
    row = fetched.fetchone()
    if row:
        if row.id == int(args[0]):
            return await c.send("This role is already the muted role.")
        try:
            db.update(roles, {'guild': g.id}, {'id': args[0]}, conn)
            return await c.send(f"Successfully set muted role to {role.mention}.")
        except Exception as e:
            print(e)
            await c.send(f"Error while setting muted role:\n{e}")
    else:
        try:
            db.insert(roles, {'id': args[0], 'guild': g.id}, conn)
            return await c.send(f"Successfully set muted role to {role.mention}.")
        except Exception as e:
            print(e)
            return await c.send(f"Error while setting muted role:\n{e}")
    
