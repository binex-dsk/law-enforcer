from datetime import datetime

no_docs = True
async def run(**kwargs):
    # staticinfo and endinfo are used to shorten this a bit, see constants
    # the uptime is just the current total of seconds it's been up
    await kwargs['c'].send(f"{kwargs['staticinfo']}\nCurrent uptime: "
    f"{round((datetime.now()-kwargs['startTime']).total_seconds())} "
    f"seconds\nCurrent latency: {round(kwargs['client'].latency*1000)}```\n{kwargs['endinfo']}")
