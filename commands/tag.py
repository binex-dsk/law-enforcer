name = 'tag'
long = 'Access a tag in the server.'
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
    db = kwargs['db']
    if len(args) < 1:
        return await c.send("Please provide a tag.")
    tagname = args[0]
    tag = db.fetch(tags, {'name': tagname, 'guild': g.id}, conn)
    if not tag:
        return await c.send("That tag doesn't exist in this server.")
    tag = tag.fetchone()
    await c.send(tag.content)