name = 'ban'
long = 'Ban a user from the server.'
syntax = "(user) (reason || none)"
ex1 = "id1 dumb stupid"
ex2 = "id2"
notes = "The user is DMed upon being banned."
reqperms = "`ban members`"
no_docs = False

async def run(**kwargs):
    c = kwargs['c']
    m = kwargs['m']
    checks = kwargs['checks']
    check1 = await checks.perms(['ban_members'], kwargs['g'], c, m)
    if not check1: return
    # checks for mentions
    if not kwargs['msg'].mentions:
        return await c.send("Please provide a member to ban.")

    member = kwargs['msg'].mentions[0]

    check2 = await checks.roles(m, member, kwargs['g'], c)
    if not check2: return

    reason = " ".join(kwargs['args'][1:len(kwargs['args'])]) or "None"

    try:
        # try to tell the member they've been banned
        try:
            await member.send(f"{member}, you have been **banned** from {kwargs['g']} by {m}.\nReason: {reason}")
        # if it doesn't work, ignore it and move on
        except:
            pass
        await member.ban(reason=reason)
        await c.send(f"{m}, I have **banned** {member}.\nReason: {reason}")
    # if any error occurs, catch it and send it
    except Exception as e:
        await c.send(f"Error while banning user: {e}")

