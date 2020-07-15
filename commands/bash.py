import os
from constants import checks

names = ['bash']
no_docs = True
arglength = 0

async def run(env):
    args, c, m = [env[k] for k in ('args', 'c', 'm')]

    try:
        await checks.owner(c, m)
    except:
        return

    if not len(args) > 0:
        return await c.send('You must include bash code to execute!')
    try:
        await c.send(os.popen(' '.join(args)).read())
    except Exception as e:
        await c.send(str(e))
