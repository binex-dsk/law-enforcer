from constants import checks, db

name = 'removetag'
names = ['removetag', 'deletetag', 'deltag']
long = 'Remove a tag from the server.'
syntax = '(tag name)'
ex1 = 'example'
ex2 = 'test'
notes = False
reqperms = '`manage guild`'
no_docs = False
arglength = 1

async def run(env):
    args = env['args']
    client = env['client']
    g = env['g']
    c = env['c']
    m = env['m']
    conn = env['conn']
    tags = env['tags']

    try:
        await checks.perms(['manage_guild'], g, c, m)
    except:
        return

    if len(args) < 1:
        return await c.send('Please provide a tag name.')

    result = db.fetch(tags, {'guild': g.id, 'name': args[0]}, conn)
    if not result:
        return await c.send('That tag does not exist in this server.')

    await c.send('Are you SURE you want to remove this tag? '\
    'Deleted tags are gone forever!\nType `y` to confirm or `n` to cancel.')

    res = await client.wait_for('message',
    check=lambda ms: ms.author.id == m.id and ms.content in ['y', 'n'])

    if res.content == 'n':
        return await c.send('Command cancelled by user.')
    try:
        db.delete(tags, {'guild': g.id, 'name': args[0]}, conn)
        return await c.send(f'Successfully deleted tag {args[0]}.')
    except Exception as e:
        await c.send(f'Error while deleting tag:\n{e}')
