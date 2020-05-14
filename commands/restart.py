import subprocess

no_docs = True

async def run(**kwargs):
    if not kwargs['m'].id in kwargs['ids']:
        return await kwargs['c'].send(kwargs['owneronly'])
    await kwargs['c'].send("Restarting...")
    # runs the restart command, see constants
    exit()
