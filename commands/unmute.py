import discord

name = 'unmute'
long = 'Unmuted a muted user.'
syntax = "(user) (reason || none)"
ex1 = "id1 said sorry in dms"
ex2 = "id2"
notes = "The user is DMed when unmuted."
reqperms = "`mute members`\n`kick members`"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    m = kwargs['m']
    args = kwargs['args']
    conn = kwargs['conn']
    roles = kwargs['muted_roles']
    checks = kwargs['checks']
    db = kwargs['db']

    check1 = await checks.perms(['mute_members', 'kick_members'], g, c, m)
    if not check1: return

    result = db.fetch(roles, {'guild': g.id}, conn)
    if not result:
        return await c.send("No muted role is set! Please set one with `setmuted`.")
    role = result.fetchone()
    muted_role = discord.utils.get(g.roles, id=role.id)

    if g.me.top_role < muted_role:
        return await c.send("I am at a lower level on the hierarchy than the muted role.")

    if not kwargs['msg'].mentions:
        return await c.send("Please mention a valid member.")

    mem = kwargs['msg'].mentions[0]
    check2 = await checks.roles(m, mem, g, c)
    if not check2: return

    reason = " ".join(args[1:len(args)]) or "None"
    if not muted_role in mem.roles:
        return await c.send("This member is not muted.")
    await mem.remove_roles(muted_role, reason=reason)
    await c.send(f"Successfully unmuted {mem}.\nReason: {reason}")
    try:
        await mem.send(f"You've been unmuted in {g} by {m}.\nReason: {reason}")
    except:
        pass
