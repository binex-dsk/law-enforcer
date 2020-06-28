import sys
from constants import checks

names = ['restart', 'reset', 'update']
no_docs = True
arglength = 0

async def run(env):
    c = env['c']
    m = env['m']

    try:
        await checks.owner(c, m)
    except:
        return
    await c.send('Restarting...')

    sys.exit()
