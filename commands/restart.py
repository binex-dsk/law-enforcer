import sys
import constants.checks as checks

names = ['restart', 'reset', 'update']
owner_only = True
no_docs = True
reqargs = ['c', 'm']

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    try:
        await checks.owner(c, m)
    except:
        return
    await c.send('Restarting...')

    sys.exit(0)
