from datetime import datetime
from constants.resp import info

names = ['info']
no_docs = True
arglength = 0

async def run(env):
    # staticinfo and endinfo are used to shorten this a bit, see constants
    # the uptime is just the current total of seconds it's been up
    c, start_time, client = [env[k] for k in ('c', 'start_time', 'client')]

    await c.send(info.format('\nCurrent uptime: '\
    f'{round((datetime.now()-start_time).total_seconds())}'\
    f' seconds\nCurrent latency: {round(client.latency*1000)}'))
