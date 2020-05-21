name = 'kick'
long = 'Kick a user from the server.'
syntax = "(user) (reason || none)"
ex1 = "id1 don't do that again"
ex2 = "id2"
notes = f"The user is DMed upon being kicked. Additionally, they are given a one-time invite to rejoin with."
f"\nIn later versions, there will be options to disable this."
reqperms = "`kick members`\n`create instant invite`"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    m = kwargs['m']
    checks = kwargs['checks']

    check1 = await checks.perms(['kick_members', 'create_instant_invite'], g, c, m)
    if not check1: return

    if not kwargs['msg'].mentions:
        return await c.send("Please provide a member to kick.")

    member = kwargs['msg'].mentions[0]

    check2 = await checks.roles(m, member, g, c)
    if not check2: return

    reason = " ".join(kwargs['args'][1:len(kwargs['args'])]) or "None"
    inv = await c.create_invite(reason=f"Temporary invite for {member}", max_uses=1)
    
    try:
        try:
            await member.send(f"{member}, you have been **kicked** from {g} by {m}.\nReason: {reason}\nI have created a one-time invite for you to join back with: {inv}")
        except:
            pass
        await member.kick(reason=reason)
        await c.send(f"{m}, I have **kicked** {member}.\nReason: {reason}")
    except Exception as e:
        await c.send(f"Error while kicking user: {e}")
