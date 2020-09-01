import discord
import constants.db as db
from tables import tags

name = 'taginfo'
names = ['taginfo']
desc = 'Get info on a tag in the server.'
examples = ['example']
notes = 'Similarly to the `tag` command, tags are specific to servers. '\
'This command gives you the tag name, content, author, and creation date.'
reqargs = ['args', 'client', 'g', 'c']
cargs = [
    {
        'name': 'tag name',
        'aname': 'tag',
        'optional': False,
        'excarg': 'g',
        'check': lambda a, g: db.fetch(tags, {'name': a, 'guild': g.id}),
        'errmsg': 'That tag doesn\'t exist in this server.'
    }
]

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    tagf = tag.fetchone()
    emb = discord.Embed()

    emb.title = f'Tag {tagf.name}'

    emb.description = tagf.content

    emb.add_field(name='Created By', value=f'{tagf.creatortag}\n{tagf.creatorid}', inline=False)\
    .set_footer(text=tagf.createdat, icon_url=client.user.avatar_url)
    await c.send(embed=emb)
