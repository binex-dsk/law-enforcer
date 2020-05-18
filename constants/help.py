prefix = '~~'

def helpCmd(emb, cmd, desc, syntax, ex1, ex2, notes, reqperms):
    emb.title = cmd
    emb.description = desc
    emb.add_field(name="Usage", value=f"\\{prefix}{cmd} {syntax}", inline=False)
    if ex1 and ex2: 
        emb.add_field(name="Examples", value=f"\\{prefix}{cmd} {ex1}\n\\{prefix}{cmd} {ex2}", inline=False)
    if notes: 
        emb.add_field(name="Extra Notes", value=notes)
    return emb.add_field(name="Required Permissions", value=reqperms.upper().replace(" ", "_"))