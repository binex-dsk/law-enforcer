import subprocess
from constants import checks

no_docs = True

async def run(env):
    c = env['c']
    m = env['m']

    check = await checks.owner(c, m)
    if not check: return
    await c.send("Restarting...")

    exit()
