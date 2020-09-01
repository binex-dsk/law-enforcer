from datetime import datetime
from constants.resp import info

names = ['info']
no_docs = True
reqargs = ('c', 'client')

async def run(**env):
    # staticinfo and endinfo are used to shorten this a bit, see constants
    # the uptime is just the current total of seconds it's been up
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    await c.send(info.format('\nCurrent uptime: '\
    f'{round((datetime.now()-client.start_time).total_seconds())}'\
    f' seconds\nCurrent latency: {round(client.latency*1000)}'))
