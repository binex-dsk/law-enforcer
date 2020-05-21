import discord

name = 'taginfo'
long = 'Get info on a tag in the server.'
syntax = "(tag name)"
ex1 = "example"
ex2 = "test"
notes = "Similarly to the `tag` command, tags are specific to servers. This command gives you the tag name, content, author, and creation date."
reqperms = "None"
no_docs = False

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    args = kwargs['args']
    conn = kwargs['conn']
    tags = kwargs['tags']
    db = kwargs['db']
    if len(args) < 1:
        return await c.send("Please provide a tag to search for.")
    tag = db.fetch(tags, {'name': args[0], 'guild': g.id}, conn)
    if not tag:
        return await c.send("That tag doesn't exist in this server.")
    tag = tag.fetchone()
    emb = discord.Embed()
    emb.title = f"Tag {tag.name}"
    emb.description = tag.content
    emb.add_field(name="Created By", value=f"{tag.creatortag}\n{tag.creatorid}", inline=False)
    emb.set_footer(text=tag.createdat, icon_url = kwargs['client'].user.avatar_url)
    await c.send(embed=emb)
