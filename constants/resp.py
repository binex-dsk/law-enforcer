# This file contains everything related to response construction.
from constants.auth import prefix

nl = '\n'
escapedpref = f'\\{prefix}'
info = '```Owner: roach#2386\nOwner ID: 728694582086205550\n'\
'Running on: 5.6.3-arch1-1 x86_64 64 bit\nProcessors: 4 × Intel Core i5-3210M '\
'CPU @ 2.50GHz\nMemory: 7.7 GB{}```Join the official support server: '\
'https://discord.gg/PVTBgK6 \nSee the code for yourself: '\
'https://github.com/binex-dsk/law-enforcer \nSupport is appreciated! Please use '\
f'{escapedpref}contact to contact my creator!'

def helpCmd(emb, cmd, desc, syntax, ex1, ex2, notes, names, reqperms):
    emb.title = cmd
    emb.description = desc
    emb.add_field(name='Usage', value=f'\\{prefix}{cmd} {syntax}', inline=False)
    if ex1 and ex2:
        emb.add_field(name='Examples',
        value=f'\\{prefix}{cmd} {ex1}\n\\{prefix}{cmd} {ex2}', inline=False)
    if len(names) > 1:
        emb.add_field(name='Aliases',
        value=f'\\{prefix}{f"{nl}{escapedpref}".join(names[1:])}', inline=False)
    if notes:
        emb.add_field(name='Extra Notes', value=notes)
    return emb.add_field(name='Required Permissions', value=reqperms.upper().replace(' ', '_'))
