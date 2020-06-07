# This file contains everything related to response construction.
from constants.auth import prefix

info = '```Owner: literal monkey#9193\nOwner ID: 694643777146454096\n'\
'Running on: 5.6.3-arch1-1 x86_64 64 bit\nProcessors: 4 × Intel Core i5-3210M '\
'CPU @ 2.50GHz\nMemory: 7.7 GB{}```Join the official support server: '\
'https://discord.gg/PVTBgK6 \nSee the code for yourself: '\
'https://github.com/spergmoment/law-enforcer\nNOTE: The above '\
'repository is an old, public version. The private, current version will be released eventually.'

def helpCmd(emb, cmd, desc, syntax, ex1, ex2, notes, reqperms):
    emb.title = cmd
    emb.description = desc
    emb.add_field(name='Usage', value=f'\\{prefix}{cmd} {syntax}', inline=False)
    if ex1 and ex2:
        emb.add_field(name='Examples',
        value=f'\\{prefix}{cmd} {ex1}\n\\{prefix}{cmd} {ex2}', inline=False)
    if notes:
        emb.add_field(name='Extra Notes', value=notes)
    return emb.add_field(name='Required Permissions', value=reqperms.upper().replace(' ', '_'))
