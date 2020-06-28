from datetime import datetime

name = 'ping'
names = ['ping']
long = 'Get the current Client and API ping.'
syntax = ''
ex1 = False
ex2 = False
notes = 'Client ping is the hard Client latency, while the API ping is how long I take to respond.'
reqperms = 'None'
no_docs = False
arglength = 0

async def run(env):
    # get the current time
    start = datetime.now()
    # send the client ping
    message = await env['c'].send(f'Client Ping: {round(env["client"].latency*1000)}')
    # then add the current time - the start time
    await message.edit(content=f'{message.content}\nAPI Ping: '\
    f'{round((datetime.now().microsecond-start.microsecond)/1000)}')
