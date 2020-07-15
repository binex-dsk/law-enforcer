from constants import db
from tables import tags

name = 'tag'
names = ['tag', 'gettag']
long = 'Access a tag in the server.'
syntax = '(tag name)'
ex1 = 'example'
ex2 = 'test'
notes = 'Tags are specific to servers. Global tags may be added later, '\
'but for now, tags can only be used in the server they were created in.'
reqperms = 'None'
no_docs = False
arglength = 1

async def run(env):
    args, g, c = [env[k] for k in ('args', 'g', 'c')]

    if len(args) < 1:
        return await c.send('Please provide a tag.')

    tagname = args[0]

    tag = db.fetch(tags, {'name': tagname, 'guild': g.id})

    if not tag:
        return await c.send('That tag doesn\'t exist in this server.')
    tag = tag.fetchone()
    await c.send(tag.content)
    