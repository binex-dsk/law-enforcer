from datetime import datetime

name = 'ping'
names = ['ping']
desc = 'Get the current Client and API ping.'
notes = 'Client ping is the hard Client latency, while the API ping is how long I take to respond.'
reqargs = ['client', 'c']

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})
    print(globals())
    # get the current time
    start = datetime.now()
    # send the client ping
    message = await c.send(f'Client Ping: {round(client.latency*1000)}')
    # then add the current time - the start time
    await message.edit(content=f'{message.content}\nAPI Ping: '\
    f'{round((datetime.now().microsecond-start.microsecond)/1000)}')
