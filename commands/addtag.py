from datetime import datetime
from constants import checks, db

name = 'addtag'
names = ['addtag']
long = 'Add a tag to the server.'
syntax = '(tag name)'
ex1 = 'example Some tag'
ex2 = 'test Test tag'
notes = 'Access tags with the `tag` command, or their info with the `taginfo` command.'
reqperms = '`manage guild`'
no_docs = False
arglength = 2

async def run(env):
    args = env['args']
    g = env['g']
    c = env['c']
    m = env['m']
    conn = env['conn']
    tags = env['tags']
    try:
        await checks.perms(['manage_guild'], g, c, m)
    except:
        return

    tagname = args[0]

    if db.exists(tags, {'name': tagname}, conn):
        return await c.send('That tag is already in the server.')

    tagcont = ' '.join(args[1:len(args)])
    now = datetime.now()

    # basically, this code just adds the tag to a SQL table
    try:
        db.insert(tags,
            {'name': tagname, 'content': tagcont, 'creatortag': str(m),
            'creatorid': m.id, 'createdat': f'{now.month}/{now.day}/{now.year}, '\
            f'at {now.hour}:{now.minute}', 'guild': g.id}, conn)
        return await c.send(f'Successfully added tag {tagname}, with content:\n{tagcont}')
    except Exception as e:
        await c.send(f'Error while adding tag:\n{e}')
    