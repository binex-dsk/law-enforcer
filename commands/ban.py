name = 'ban'
long = 'Ban a user from the server.'
short = "Ban a user"
syntax = "(user) (reason || none)"
ex1 = "id1 dumb stupid"
ex2 = "id2"
notes = "The user is DMed upon being banned."
reqperms = "`ban members`"
no_docs = False

async def run(**kwargs):
    c = kwargs['c']
    m = kwargs['m']
    if not kwargs['g'].me.guild_permissions.ban_members:
        return await c.send(kwargs['botperms']('ban members'))
    # checks user perms, see constants
    if not m.guild_permissions.ban_members:
        return await c.send(kwargs['userperms']('ban_members'))
    # checks for mentions
    if not kwargs['msg'].mentions:
        return await c.send("Please provide a member to ban.")
    # uses the first mention
    member = kwargs['msg'].mentions[0]
    # the reason, or "None"
    reason = " ".join(kwargs['args'][1:len(kwargs['args'])]) or "None"
    # checks role hierarchy, see constants
    if kwargs['g'].me.top_role < member.top_role:
        return await c.send(kwargs['botlower'])
    if m.top_role < member.top_role:
        return await c.send(kwargs['userlower'])
    # try block
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

