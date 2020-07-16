import sys
import constants.checks as checks

names = ['restart', 'reset', 'update']
no_docs = True
arglength = 0

async def run(env):
    c, m = [env[k] for k in ('c', 'm')]

    try:
        await checks.owner(c, m)
    except:
        return
    await c.send('Restarting...')

    sys.exit(0)
