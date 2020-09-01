from datetime import datetime
from constants import checks, db
from tables import tags, server_config

name = 'addtag'
names = ['addtag']
desc = 'Add a tag to the server.'
examples = ['example Some tag.']
notes = 'Access tags with the `tag` command, or their info with the `taginfo` command.\nSome servers may allow anyone to add tags.'
reqargs = ['args', 'g', 'c', 'm', 'conf']
cargs = [
    {
        'name': 'tag name',
        'novar': True,
        'optional': False,
        'excarg': 'g',
        'check': lambda t, g: not db.exists(tags, {'name': t, 'guild': g.id}),
        'errmsg': 'That tag is already in the server.'
    },
    {
        'name': 'tag content',
        'aname': 'tagcont',
        'optional': False
    }
]

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    if not conf.allow_all_addtag:
        try:
            await checks.perms(['manage_guild'], g, c, m)
        except:
            return

    tagname = args[0]
    #tagcont = ' '.join(args[1:len(args)])
    now = datetime.now()

    # basically, this code just adds the tag to a SQL table
    try:
        db.insert(tags,
            {'name': tagname, 'content': tagcont, 'creatortag': str(m),
            'creatorid': m.id, 'createdat': f'{now.month}/{now.day}/{now.year}, '\
            f'at {now.hour}:{now.minute}', 'guild': g.id})
        return await c.send(f'Successfully added tag {tagname}, with content:\n{tagcont}')
    except Exception as e:
        await c.send(f'Error while adding tag:\n{e}')
    