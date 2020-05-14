name = 'tag'
long = 'Access a tag in the server.'
short = long
syntax = "(tag name)"
ex1 = "example"
ex2 = "test"
notes = "Tags are specific to servers. Global tags may be added later, but for now, tags can only be used in the server they were created in."
reqperms = "None"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    args = kwargs['args']
    conn = kwargs['conn']
    tags = kwargs['tags']
    if len(args) < 1:
        return await c.send("Please provide a tag.")
    tagname = args[0]
    tagg = g.id
    s = tags.select().where(tags.c.name==tagname).where(tags.c.guild==tagg)
    result = conn.execute(s)
    try:
        # just checks for a tag that is in the current guild and is the specified name
        row = result.fetchone()
        return await c.send(row.content)
    except Exception as e:
        await c.send(f"That tag does not exist in this server.")
        print(e)