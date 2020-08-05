from constants.auth import main_owner

name = 'contact'
names = ['contact']
long = 'Contact the main bot owner.'
syntax = '(message...)'
ex1 = 'The bot crashes during the server setup!'
ex2 = 'Can you add a channel setup to the server setup?'
notes = 'Abuse of the contact system will result in you being **blacklisted** from it.'
reqargs = ['args', 'client', 'c', 'm']
no_docs = False
arglength = 1

async def run(**env):
    for _, a in enumerate(reqargs):
        globals().update({a: env.get(a)})

    message = ' '.join(args)
    owner = client.get_user(main_owner)
    try:
        await owner.send(f'Message from {m}:\n{message}')
        await c.send('Thank you for contacting the owner. Your support is appreciated.')
    except Exception as e:
        await c.send(f'Error while contacting the owner:\n{e}')
        print(e)
        