import math

async def run(args, client, g, c, m, botperms, userperms):
    if not g.me.guild_permissions.ban_members:
        return await c.send(botperms('ban members'))
    if not m.guild_permissions.ban_members:
        return await c.send(userperms('ban_members'))
    # checks the length of the args
    if len(args) < 1:
        return await c.send(f"Please enter a user ID to unban.\n"
        f"To get a user ID, enable **Developer Mode** in the **Appearance** tab in settings, then right-click the user and select **\"Copy ID.\"**")
    # makes sure its a number
    if math.isnan(int(args[0])):
        return await c.sned("Please enter a user ID to unban.")
    id = int(args[0])
    reason = " ".join(args[1:len(args)]) or "None"
    ban = None
    try:
        # fetch the ban for that user
        user = client.get_user(id)
        ban = await g.fetch_ban(user)
    except Exception as e:
        # fetch_ban throws an exception if the user isn't banned, so catch it here to notify the user
        await c.send("This user is not banned.")
        return print(f"{e}")
    try:
        await g.unban(ban.user, reason=reason)
        await c.send(f"Successfully unbanned {ban.user}.\nReason: {reason}")
        try:
            await ban.user.send(f"You have been **unbanned** in {g} by {m}.\nReason: {reason}")
        except:
            pass
    except Exception as e:
        await c.send(f"Error while unbanning user.\n{e}")