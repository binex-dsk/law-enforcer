from constants import checks, db
from tables import server_config

name = 'ban'
names = ['ban', 'snipe']
long = 'Ban a user from the server.'
syntax = '(user mention/id) (reason || none)'
ex1 = 'id1 dumb stupid'
ex2 = '728694582086205550 leaving won\'t save you'
notes = 'The user is DMed upon being banned.'
reqperms = ['ban members']
reqargs = ['client', 'args', 'msg', 'g', 'c', 'm']
no_docs = False
arglength = 1

async def run(**env):
    for _, a in enumerate(reqargs):
        globals().update({a: env.get(a)})

    conf = db.fetch(server_config, {'guild': g.id}).fetchone()
    try:
        id = args[0] if args[0].isdigit() else msg.mentions[0].id
        user = await client.fetch_user(int(id))
    except:
        return await c.send('Please provide a valid user mention or ID to ban.')
    if g.get_member(id):
        try:
            await checks.roles(m, user, g, c)
        except:
            return

    reason = ' '.join(args[1:len(args)]) or 'None'

    try:
        if conf.ban_dm:
            try:
                await user.send(conf.ban_dm_message.format(MEM=user, GUILD=g, MOD=m, REASON=reason))
            # if it doesn't work, ignore it and move on
            except:
                pass
        await g.ban(user, reason=reason, delete_message_days=conf.ban_delete_days)
        await c.send(f'{m}, I have **banned** {user}.\nReason: {reason}')
    # if any error occurs, catch it and send it
    except Exception as e:
        await c.send(f'Error while banning user: {e}')
