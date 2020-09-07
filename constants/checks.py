from constants.auth import ids

async def perms(perms, g, c, m):
    """Checks permissions of the bot and the member."""
    for perm in perms:
        if not dict(g.me.guild_permissions).get(perm):
            await c.send(f'I must have the `{perm.upper()}` permission to do this.')
            raise Exception()
        if not dict(m.guild_permissions).get(perm):
            await c.send(f'You must have the `{perm.upper()}` permission to do this.')
            raise Exception()
    return True

async def owner(c, m):
    """Checks if the user is a bot owner."""
    if not m.id in ids:
        await c.send('You must be an owner to use this command.')
        raise Exception()
    return True

async def roles(auth, mem, g, c):
    """Checks role positions."""
    if g.me.top_role <= mem.top_role:
        await c.send('I am at an equal or lower level on the role hierarchy than this member.')
    elif auth.top_role <= mem.top_role:
        await c.send('This member has an equal or higher role than you.')
    else:
        return True
    raise Exception()

def cid(id, get):
    """Executes a function based on an ID."""
    return get(to_id(id))

def to_id(id):
    """Converts a mention or ID into a proper int."""
    return int(id.strip('<@&#!>')) if id.isdigit() else id.strip('<@&#!>')
