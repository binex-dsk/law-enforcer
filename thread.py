import time, asyncio
from datetime import timedelta
from timeloop import Timeloop
import constants.db as db
from tables import muted_members, muted_roles, conn

timer = Timeloop()

checkTime = 5
client = None

class Thread():
    @staticmethod
    def start(cli, block=False):
        global client
        try:
            timer.start(block)
            client = cli
        except Exception as e:
            print(e)

    @staticmethod
    def stop():
        try:
            timer.stop()
        except Exception as e:
            print(e)

async def search():
    global client
    mems = conn.execute(muted_members.select().where(muted_members.c.unmute_after <= int(time.time()))).fetchall()

    for m in mems:
        mem = await client.fetch_user(m.id)
        gmem = client.get_guild(m.guild).member(mem)
        await gmem.remove_roles(db.fetch(muted_roles, {'guild': m.guild}).fetchone().id, "Automatic unmute")
        try:
            await mem.send(f'You have been automatically unmuted in {client.get_guild(m.guild)}.')
        except:
            pass

@timer.job(interval=timedelta(seconds=checkTime))
def checkMutes():
    asyncio.run(search())
