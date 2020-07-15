import discord
from constants import db
from tables import tags

name = 'tags'
names = ['tags', 'taglist']
long = 'Get a list of all tags in the server.'
syntax = ''
ex1 = False
ex2 = False
notes = 'Potentially, if you have enough tags, the bot won\'t be able to display them all. '\
'However, the amount of tags required for this to happen is huge, so don\'t worry about it.'
reqperms = 'None'
no_docs = False
arglength = 0

async def run(env):
    g, c = [env[k] for k in ('g', 'c')]

    result = db.fetch(tags, {'guild': g.id})
    if not result:
        return await c.send('No tags exist on this server.')
    tags_str = ''
    fieldnum = 0
    emb = discord.Embed()
    emb.title = f'All tags in server {g}'
    emb.description = 'Use ~~taginfo (tag name) for info on these tags.'

    # basically gets all the tags and formats them to fit on an embed
    for row in result:
        print(row)
        if len(tags_str) > 1000:
            if fieldnum == 0:
                emb.add_field(name='Tags', value=tags_str, inline=False)
            else:
                emb.add_field(name='Continued', value=tags_str, inline=False)
            fieldnum += 1
            tags_str = ''
        tags_str += f'{row.name}\n'
    if fieldnum == 0:
        emb.add_field(name='Tags', value=tags_str, inline=False)
    else:
        emb.add_field(name='Continued', value=tags_str, inline=False)
    await c.send(embed=emb)
