import subprocess

no_docs = True

async def run(**kwargs):
    checks = kwargs['checks']
    check = await checks.owner(kwargs['c'], kwargs['m'])
    if not check: return
    await kwargs['c'].send("Restarting...")

    exit()
