import time, asyncio, json
from datetime import timedelta
from timeloop import Timeloop
from constants import db, auth
from tables import muted_members, muted_roles, conn
import requests

def req(path, data, meth):
    return requests.request(meth, f"https://discord.com/api/v8/{path}", headers={'Authorization': f'Bot {auth.token}', 'Content-Type': 'application/json'}, data=data)
timer = Timeloop()

checkTime = 5

class Thread():
    """Thread class to manage the mute timers."""
    @staticmethod
    def start(block=False):
        try:
            timer.start(block)
        except Exception as e:
            print(e)

    @staticmethod
    def stop():
        try:
            timer.stop()
        except Exception as e:
            print(e)

async def search():
    """Searches through muted members and unmutes them if their mute time is up."""
    mems = conn.execute(muted_members.select().where(muted_members.c.unmute_after <= int(time.time()))).fetchall()

    for m in mems:
        gid = m[1]
        mid = m[0]
        try:
            roles = req(f'guilds/{gid}/members/{mid}', {}, 'get').json()['roles']
        except KeyError as e:
            print(e)
            continue
        rid = db.fetch(muted_roles, {'guild': gid}).fetchone().id
        try:
            del roles[roles.index(str(rid))]
        except:
            pass
        rm = req(f'guilds/{gid}/members/{mid}', json.dumps({'roles': roles}), 'patch')
        if rm.status_code == 204:
            db.delete(muted_members, {'id': mid, 'guild': gid})
        else:
            return
        try:
            cid = req('users/@me/channels', json.dumps({'recipient_id': mid}), 'post').json()['id']
            gname = req(f'guilds/{gid}', {}, 'get').json()['name']
            req(f'channels/{cid}/messages', {'content': f'You have been automatically unmuted in {gname}.'}, 'post')
        except:
            pass

@timer.job(interval=timedelta(seconds=checkTime))
def checkMutes():
    """Timer to start the search function."""
    asyncio.run(search())
