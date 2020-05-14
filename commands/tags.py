import discord

name = 'tags'
long = 'Get a list of all tags in the server.'
short = "List tags in the server"
syntax = ""
ex1 = False
ex2 = False
notes = f"Potentially, if you have enough tags, the bot won\'t be able to display them all. "
f"However, the amount of tags required for this to happen is huge, so don't worry about it."
reqperms = "None"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    conn = kwargs['conn']
    tags = kwargs['tags']
    tagg = g.id
    s = tags.select().where(tags.c.guild==tagg)
    result = conn.execute(s)
    tags = ""
    fieldnum = 0
    emb = discord.Embed()
    emb.title = f"All tags in server {g}"
    emb.description="Use ~~taginfo (tag name) for info on these tags."
    # basically gets all the tags and formats them to fit on an embed
    for row in result:
        print(row)
        if len(tags) > 1000:
            if fieldnum == 0:
                emb.add_field(name="Tags", value=tags, inline=False)
            else:
                emb.add_field(name="Continued", value=tags, inline=False)
            fieldnum += 1
            tags = ""
        tags+=f"{row.name}\n"
    if fieldnum == 0:
        emb.add_field(name="Tags", value=tags, inline=False)
    else:
        emb.add_field(name="Continued", value=tags, inline=False)
    try:
        await c.send(embed=emb)
    except Exception as e:
        await c.send("No tags exist on this server.")
        print(e)