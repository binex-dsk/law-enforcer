import math, asyncio

name = 'mute'
long = 'Mute a user for a certain amount of time'
short = "Mute a user"
syntax = "(user) (time) (reason || none)"
ex1 = "id1 24 stop spamming"
ex2 = "id2 0.5"
notes = "The user is DMed when they are muted, as well as automatically unmuted."
reqperms = "`mute members`\n`kick members`"
no_docs = False

async def unmute(m, t, r, role):
    await asyncio.sleep(t*60*60)
    if not role in m.roles:
        return
    await m.remove_roles(role, reason=r)
    try:
        await m.send(f"You've been automatically unmuted in {m.guild}.")
    except:
        pass

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
    # checks the muted role
    if not muted_role:
        return await c.send("No muted role exists. Please create one.")
    if g.me.top_role < muted_role:
        return await c.send("I am at a lower level on the hierarchy than the muted role.")
    if not kwargs['msg'].mentions:
        return await c.send("Please mention a valid member.")
    mem = kwargs['msg'].mentions[0]
    if g.me.top_role < mem.top_role:
        return await c.send(kwargs['botlower'])
    if m.top_role < mem.top_role:
        return await c.send(kwargs['userlower'])
    # makes sure they aren't already muted
    if muted_role in mem.roles:
        return await c.send("That member is already muted.")
    if not len(args) > 1:
        return await c.send("Please provide an amount of time to mute this user for.")
    if math.isnan(float(args[1])):
        return await c.send("Please provide a valid number.")
    reason = " ".join(args[2:len(args)]) or "None"
    time = float(args[1])
    try:
        # add the muted role to the member
        await mem.add_roles(muted_role, reason=reason)
        await c.send(f"Successfully muted {mem} for {time} hours. Reason: {reason}")
        try:
            await mem.send(f"You've been muted in {g} by {m} for {time} hours.\nReason: {reason}")
        except:
            pass
        # goes to the unmute function, muting them for the specified time
        await unmute(mem, time, "Mute time expired", muted_role)
    except Exception as e:
        await c.send(f"Error while muting member: {e}")
