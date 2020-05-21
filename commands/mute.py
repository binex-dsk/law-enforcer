import math, asyncio, discord

name = 'mute'
long = 'Mute a user for a certain amount of time'
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
    conn = kwargs['conn']
    roles = kwargs['muted_roles']
    checks = kwargs['checks']
    db = kwargs['db']

    check1 = await checks.perms(['mute_members', 'kick_members'], g, c, m)
    if not check1: return
    
    # checks the muted role
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

    # makes sure they aren't already muted
    if muted_role in mem.roles:
        return await c.send("That member is already muted.")

    if not len(args) > 1:
        return await c.send("Please provide an amount of time to mute this user for.")

    if math.isnan(float(args[1])):
        return await c.send("Please provide a valid number.")

    reason = " ".join(args[2:len(args)]) or "None"
    time = float(args[1])
    # this checks if it's an integer number of hours, i.e. 5, to stop it from displaying 5.0, etc.
    if float(int(time)) == time:
        time = int(time)
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
