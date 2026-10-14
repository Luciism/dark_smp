import os, time, datetime, zoneinfo
from mcrcon import MCRcon

HOST = os.environ["RCON_HOST"]
PORT = int(os.environ.get("RCON_PORT", 25575))
PASSWORD = os.environ["RCON_PASSWORD"]
RESTART_TIME = os.environ.get("RESTART_TIME", "04:00")  # 24h HH:MM, in TZ below
TZ = zoneinfo.ZoneInfo(os.environ.get("TZ", "UTC"))
WARN_SECONDS_BEFORE = [600, 300, 60, 10, 5, 4, 3, 2, 1]

def send(cmd):
    with MCRcon(HOST, PASSWORD, port=PORT) as mcr:
        return mcr.command(cmd)

def warn(message):
    payload = {"text": message, "color": "yellow"}
    import json
    send(f"tellraw @a {json.dumps(payload)}")

def next_target(now):
    hh, mm = map(int, RESTART_TIME.split(":"))
    target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if target <= now:
        target += datetime.timedelta(days=1)
    return target

print("Restarter active")

while True:
    now = datetime.datetime.now(TZ)
    target = next_target(now)

    for lead in WARN_SECONDS_BEFORE:
        warn_at = target - datetime.timedelta(seconds=lead)
        wait = (warn_at - datetime.datetime.now(TZ)).total_seconds()
        if wait > 0:
            time.sleep(wait)
        label = f"{lead // 60} minute(s)" if lead >= 60 else f"{lead} seconds"
        try:
            warn(f"Server restarting in {label}")
        except Exception as e:
            print(f"warning failed: {e}", flush=True)

    wait = (target - datetime.datetime.now(TZ)).total_seconds()
    if wait > 0:
        time.sleep(wait)
    try:
        send("stop")
    except Exception as e:
        print(f"stop failed: {e}", flush=True)

    time.sleep(90)  # let the container actually cycle before recomputing tomorrow's target

