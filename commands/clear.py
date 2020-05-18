name = 'clear'
long = 'Clear a certain amount of messages.'
syntax = "(amount || 20)"
ex1 = "40"
ex2 = " "
notes = "The limit for this is very high (10000), but higher values (>2000) will be slower."
reqperms = "`manaage messages`\n`read message history`"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    m = kwargs['m']
    if not g.me.guild_permissions.manage_messages:
        return await c.send(kwargs['botperms']('manage messages'))
    if not m.guild_permissions.manage_messages:
        return await c.send(kwargs['userperms']('manage_messages'))
    if not g.me.guild_permissions.read_message_history:
        return await c.send(kwargs['botperms']('read message history'))
    if not m.guild_permissions.read_message_history:
        return await c.send(kwargs['userperms']('read_message_history'))
    if len(kwargs['args']) < 1:
        amt = 20
    else:
        amt = int(kwargs['args'][0])
    if amt > 10000 or amt < 2:
        return await c.send("Please use a valid amount between 2 and 10000.")
    try:
        # deletes the messages. it's +1 to handle the original message
        # discord.py purge actually can support over 100, unlike d.js and the api
        # it uses separate calls for >100 values
        await c.purge(limit=amt+1)
        message = await c.send(f"Successfully cleared {amt} messages.")
        # delete the sent message after 3 secs
        await message.delete(delay=3)
    except Exception as er:
        await c.send(f"Error while clearing messages: {er}")