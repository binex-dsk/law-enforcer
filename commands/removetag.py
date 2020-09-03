from constants import db
from tables import tags

name = 'removetag'
names = ['removetag', 'deletetag', 'deltag']
desc = 'Remove a tag from the server.'
examples = ['example', 'test']
reqperms = ['manage guild']
reqargs = ['args', 'client', 'g', 'c', 'm']
cargs = [
    {
        'name': 'tag name',
        'optional': False,
        'noarg': True,
        'excarg': 'g',
        'check': lambda a, g: db.fetch(tags, {'guild': g.id, 'name': a}),
        'errmsg': 'That tag does not exist in this server.'
    }
]

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    await c.send('Are you SURE you want to remove this tag? '\
    'Deleted tags are gone forever!\nType `y` to confirm or `n` to cancel.')

    res = await client.wait_for('message',
    check=lambda ms: ms.author.id == m.id and ms.content in ['y', 'n'])

    if res.content == 'n':
        return await c.send('Command cancelled by user.')
    try:
        db.delete(tags, {'guild': g.id, 'name': args[0]})
        return await c.send(f'Successfully deleted tag {args[0]}.')
    except Exception as e:
        await c.send(f'Error while deleting tag:\n{e}')
