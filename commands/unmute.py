name = 'unmute'
long = 'Unmuted a muted user.'
short = "Unmute a user"
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
    muted_role = kwargs['muted_role']

    if not g.me.guild_permissions.mute_members:
        return await c.send(kwargs['botperms']('mute members'))
    if not m.guild_permissions.mute_members:
        return await c.send(kwargs['userperms']('mute_members'))
    if not g.me.guild_permissions.kick_members:
        return await c.send(kwargs['botperms']('kick members'))
    if not m.guild_permissions.kick_members:
        return await c.send(kwargs['userperms']('kick_members'))
    if not muted_role:
        return await c.send("No muted role exists.")
    if g.me.top_role < muted_role:
        return await c.send("I am at a lower level on the hierarchy than the muted role.")
    if not kwargs['msg'].mentions:
        return await c.send("Please mention a valid member.")
    mem = kwargs['msg'].mentions[0]
    if g.me.top_role < mem.top_role:
        return await c.send(kwargs['botlower'])
    if m.top_role < mem.top_role:
        return await c.send(kwargs['userlower'])
    reason = " ".join(args[1:len(args)]) or "None"
    if not muted_role in mem.roles:
        return await c.send("This member is not muted.")
    await mem.remove_roles(muted_role, reason=reason)
    await c.send(f"Successfully unmuted {mem}.\nReason: {reason}")
    try:
        await mem.send(f"You've been unmuted in {g} by {m}.\nReason: {reason}")
    except:
        pass
