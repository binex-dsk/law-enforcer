from datetime import datetime

name = 'addtag'
long = 'Add a tag to the server.'
syntax = "(tag name)"
ex1 = "example Some tag"
ex2 = "test Test tag"
notes = "Access tags with the `tag` command, or their info with the `taginfo` command."
reqperms = "`manage guild`"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    m = kwargs['m']
    args = kwargs['args']
    conn = kwargs['conn']
    tags = kwargs['tags']
    db = kwargs['db']
    checks = kwargs['checks']
    check = await checks.perms(['manage_guild'], g, c, m)
    if not check: return
    if len(args) < 1:
        return await c.send("Please provide a tag name.")
    tagname = args[0]
    if db.exists(tags, {'name': tagname}, conn):
        return await c.send("That tag is already in the server.")
    if len(args) < 2:
        return await c.send("Please provide tag content.")
    tagcont = " ".join(args[1:len(args)])
    now = datetime.now()
    # basically, this code just adds the tag to a SQL table
    try:
        db.insert(tags,
            {'name': tagname, 'content': tagcont, 'creatortag': str(m), 
            'creatorid': m.id, 'createdat': f"{now.month}/{now.day}/{now.year}, at {now.hour}:{now.minute}",
            'guild': g.id}, conn)
        return await c.send(f"Successfully added tag {tagname}, with content:\n{tagcont}")
    except Exception as e:
        await c.send(f"Error while adding tag:\n{e}")
    