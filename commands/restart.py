import sys
import constants.checks as checks

names = ['restart', 'reset', 'update']
owner_only = True
no_docs = True
reqargs = ['c', 'm']
arglength = 0

async def run(**env):
    for _, a in enumerate(reqargs):
        globals().update({a: env.get(a)})

    try:
        await checks.owner(c, m)
    except:
        return
    await c.send('Restarting...')

    sys.exit(0)
