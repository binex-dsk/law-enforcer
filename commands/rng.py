import random

name = 'rng'
long = 'Generate a random number.'
syntax = '(min \|\| 0) (max \|\| 10)'
ex1 = '5 13'
ex2 = ' '
notes = 'This only generates integers at the moment.'
reqperms = 'none'
no_docs = False

async def run(env):
    args = env['args']
    c = env['c']

    if len(args) < 1:
        min = 0
    else:
        try:
            min = int(args[0])
        except:
            return await c.send('Please provide a valid maximum.')

    if len(args) < 2:
        max = 10
    else:
        try:
            max = int(args[1])
        except:
            return await c.send('Please provide a valid maximum.')

    await c.send(str(random.randint(min, max)))
    