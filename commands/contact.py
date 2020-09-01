from constants.auth import main_owner

name = 'contact'
names = ['contact']
desc = 'Contact the main bot owner.'
examples = ['The bot crashes during the server setup!', 'I\'m getting an error "optional" which makes no sense when running ~~ban!']
notes = 'Abuse of the contact system will result in you being **blacklisted** from it.'
reqargs = ['args', 'client', 'c', 'm']
cargs = [
    {
        'name': 'message',
        'optional': False
    }
]

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    owner = client.get_user(main_owner)
    try:
        await owner.send(f'Message from {m}:\n{message}')
        await c.send('Thank you for contacting the owner. Your support is appreciated.')
    except Exception as e:
        await c.send(f'Error while contacting the owner:\n{e}')
        print(e)
        