import os
from constants import checks

names = ['bash']
no_docs = True
arglength = 0

async def run(env):
    args = env['args']
    c = env['c']
    m = env['m']

    try:
        await checks.owner(c, m)
    except:
        return

    if not len(args) > 0:
        return await c.send('You must include bash code to execute!')
    try:
        # execute the bash code
        a = os.popen(' '.join(args))
        # read the result
        result = a.read()
        # and send it
        await c.send(result)
    except Exception as e:
        await c.send(str(e))
