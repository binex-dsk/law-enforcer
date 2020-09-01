import os

names = ['bash']
owner_only = True
no_docs = True
reqargs = ['args', 'c']
arglength = 0

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    if not len(args) > 0:
        return await c.send('You must include bash code to execute!')
    try:
        await c.send(os.popen(' '.join(args)).read())
    except Exception as e:
        await c.send(str(e))
