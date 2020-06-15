from constants import checks

no_docs = True

async def run(env):
    c = env['c']
    m = env['m']

    try:
        await checks.owner(c, m)
    except:
        return
    await c.send('Restarting...')

    exit()
