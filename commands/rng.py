import random

name = 'rng'
names = ['rng', 'random']
desc = 'Generate a random number.'
examples = ['5 13', '']
notes = 'This only generates integers at the moment.'
cargs = [
    {
        'name': 'minimum',
        'optional': True,
        'check': lambda a: a.isdigit() and int(a),
        'errmsg': 'Please provide a valid minimum.',
        'default': 0
    },
    {
        'name': 'maximum',
        'optional': True,
        'check': lambda a: a.isdigit() and int(a),
        'errmsg': 'Please provide a valid maximum',
        'default': 10
    }
]
reqargs = ['args', 'c']

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    await c.send(str(random.randint(minimum, maximum)))
    