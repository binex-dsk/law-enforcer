# This file contains everything related to response construction.
import platform, os, subprocess, requests, psutil, discord
from constants.auth import prefix, main_owner, token
from init import client

def safe_get(id):
    get = requests.get(f'https://discord.com/api/v8/users/{id}', headers={'Authorization': f'Bot {token}'})
    if get.status_code == 200:
        user = discord.User(state=client._connection, data=get.json())
        return user
    return False

uname = platform.uname()
ps = psutil.Process(os.getpid())
lscpu = subprocess.check_output('lscpu', shell=True).strip().decode().split('\n')

info = f'```Owner: {safe_get(main_owner)}\nOwner ID: {main_owner}\n'\
f'Running on: {uname.release} {uname.machine}\nCPU: {lscpu[4].split()[-1]} × {" ".join(lscpu[13].split()[2:]).split(" CPU")[0]}\n'\
f'CPU frequency: {int(float(lscpu[17].split()[-1]))/1000}GHz\nCPU usage: {ps.cpu_percent()}%\n'\
f'Total memory: {str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"}\nMemory usage: {round(ps.memory_info()[0]/2.**30*1000, 2)} MB'\
'{}```Join the official support server: https://discord.gg/PVTBgK6 \nSee the code for yourself: '\
f'https://github.com/binex-dsk/law-enforcer \nSupport is appreciated! Please use {prefix}contact to contact my creator!'
