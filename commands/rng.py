import random

name = 'rng'
names = ['rng', 'random']
long = 'Generate a random number.'
syntax = '(min \|\| 0) (max \|\| 10)'
ex1 = '5 13'
ex2 = ' '
notes = 'This only generates integers at the moment.'
no_docs = False
reqargs = ['args', 'c']
arglength = 0

async def run(**env):
    for _, a in enumerate(reqargs):
        globals().update({a: env.get(a)})

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
    