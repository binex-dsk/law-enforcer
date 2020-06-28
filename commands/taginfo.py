import discord
from constants import db

name = 'taginfo'
names = ['taginfo']
long = 'Get info on a tag in the server.'
syntax = '(tag name)'
ex1 = 'example'
ex2 = 'test'
notes = 'Similarly to the `tag` command, tags are specific to servers. '\
'This command gives you the tag name, content, author, and creation date.'
reqperms = 'None'
no_docs = False
arglength = 1

async def run(env):
    args = env['args']
    client = env['client']
    g = env['g']
    c = env['c']
    conn = env['conn']
    tags = env['tags']

    if len(args) < 1:
        return await c.send('Please provide a tag to search for.')

    tag = db.fetch(tags, {'name': args[0], 'guild': g.id}, conn)

    if not tag:
        return await c.send('That tag doesn\'t exist in this server.')

    tag = tag.fetchone()
    emb = discord.Embed()

    emb.title = f'Tag {tag.name}'

    emb.description = tag.content

    emb.add_field(name='Created By', value=f'{tag.creatortag}\n{tag.creatorid}', inline=False)\
    .set_footer(text=tag.createdat, icon_url=client.user.avatar_url)
    await c.send(embed=emb)
