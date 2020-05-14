name = 'removetag'
long = 'Remove a tag from the server.'
short = long
syntax = "(tag name)"
ex1 = "example"
ex2 = "test"
notes = False
reqperms = "`manage guild`"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    m = kwargs['m']
    args = kwargs['args']
    conn = kwargs['conn']
    tags = kwargs['tags']
    if not g.me.guild_permissions.manage_guild:
        return await c.send(kwargs['botperms']('manage the server'))
    if not m.guild_permissions.manage_guild:
        return await c.send(kwargs['userperms']('manage_guild'))
    if len(args) < 1:
        return await c.send("Please provide a tag name.")
    tagname = args[0]
    s = tags.select().where(tags.c.name==tagname).where(tags.c.guild==g.id)
    result = conn.execute(s)
    try:
        result.fetchone()
    except Exception as e:
        await c.send(f"That tag does not exist in this server.")
        return print(e)
    try:
        # similar to addtag, but removes it
        d = tags.delete().where(tags.c.name==tagname).where(tags.c.guild==g.id)
        result = conn.execute(d)
        return await c.send(f"Successfully deleted tag {tagname}.")
    except Exception as e:
        await c.send(f"Error while deleting tag:\n{e}")
