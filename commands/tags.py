import discord
from constants import db

name = 'tags'
long = 'Get a list of all tags in the server.'
syntax = ""
ex1 = False
ex2 = False
notes = """Potentially, if you have enough tags, the bot won\'t be able to display them all. However, the amount of tags required 
for this to happen is huge, so don't worry about it."""
reqperms = "None"
no_docs = False

async def run(env):
    g = env['g']
    c = env['c']
    m = env['m']
    conn = env['conn']
    tags = env['tags']

    result = db.fetch(tags, {'guild': g.id}, conn)
    if not result:
        return await c.send("No tags exist on this server.")
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
    await c.send(embed=emb)
