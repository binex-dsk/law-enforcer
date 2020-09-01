import constants.db as db
from tables import tags

name = 'tag'
names = ['tag', 'gettag']
desc = 'Access a tag in the server.'
examples = ['example']
notes = 'Tags are specific to servers. Global tags may be added later, '\
'but for now, tags can only be used in the server they were created in.'
reqargs = ['args', 'g', 'c']
cargs = [
    {
        'name': 'tag name',
        'aname': 'tag',
        'optional': False,
        'excarg': 'g',
        'check': lambda a, g: db.fetch(tags, {'name': a, 'guild': g.id}),
        'errmsg': 'That tag doesn\'t exist in this server.'
    }
]

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    await c.send(tag.fetchone().content)
    