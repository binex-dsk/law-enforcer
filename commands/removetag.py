name = 'removetag'
long = 'Remove a tag from the server.'
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
    checks = kwargs['checks']
    db = kwargs['db']

    check = await checks.perms(['manage_guild'], g, c, m)
    if not check: return
    
    if len(args) < 1:
        return await c.send("Please provide a tag name.")

    result = db.fetch(tags, {'guild': g.id, 'name': args[0]}, conn)
    if not result:
        return await c.send(f"That tag does not exist in this server.")
    await c.send("Are you SURE you want to remove this tag? Deleted tags are gone forever!\nType `y` to confirm or `n` to cancel.")
    res = await kwargs['client'].wait_for('message', check=lambda ms: ms.author.id == m.id and ms.content in ['y', 'n'])
    if res.content == 'n':
        return await c.send("Command cancelled by user.")
    try:
        db.delete(tags, {'guild': g.id, 'name': args[0]}, conn)
        return await c.send(f"Successfully deleted tag {args[0]}.")
    except Exception as e:
        await c.send(f"Error while deleting tag:\n{e}")
