import json, os, subprocess, time, urllib.request, urllib.error
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
_port = "8081"
_proj = f"test-{os.getpid()}"

os.environ["APP_PORT"] = _port
URL = f"http://127.0.0.1:{_port}"

def run(*args, **kwargs):
    return subprocess.run(args, cwd=_root, check=True, timeout=180, **kwargs)

def compose(*args, **kwargs):
    return run("docker", "compose", "-p", _proj, *args, **kwargs)

def req(method, path):
    try:
        with urllib.request.urlopen(urllib.request.Request(URL + path, method=method), timeout=5) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.load(e)

def check(method, path, code, count=None):
    status, body = req(method, path)
    print(" "*3, method, path, "->", status, body)
    if status != code or (count is not None and body['count'] != count):
        raise RuntimeError(f"expected code: {code}, count: {count}")

def wait_ready():
    for _ in range(60):
        try:
            if req("GET", "/readyz")[0] == 200:
                return
        except OSError:
            pass
        time.sleep(1)
    raise TimeoutError("app hasn't started in 60s")


stage_count = 0

def set_stage(name):
    global stage, stage_count
    stage_count += 1
    stage = name
    print("-"*3, f"{stage_count}.", name.upper(), "-"*3, flush=True)




N = 3
try:
    set_stage(f"Запускаем {_proj}")
    compose("up", "-d", "--build", "--wait", "--wait-timeout", "120")
    wait_ready()

    set_stage("Проверяем счетчик")
    check("GET", "/", 200, 0)
    for _ in range(N):
        check("POST", "/increment", 200)
    check("GET", "/", 200, N)

    set_stage("Пересоздаем app")
    compose("up", "-d", "--no-deps", "--force-recreate", "--wait", "app")
    wait_ready()
    check("GET", "/", 200, N)

    set_stage("Отключаем Redis")
    compose("stop", "redis")
    check("GET", "/healthz", 200)
    check("GET", "/readyz", 503)
    check("POST", "/increment", 503)
    compose("start", "redis")
    wait_ready()
    check("GET", "/", 200, N)
    check("POST", "/increment", 200, N+1)

    set_stage("Делаем резервную копию")
    compose("stop")
    redis_id = compose("ps", "-aq", "redis", capture_output=True, text=True).stdout.strip()
    (_root / "backups").mkdir(exist_ok=True)

    with open(_root / "backups" / f"redis-{_proj}.tar", "wb") as f:
        run("docker", "run", "--rm", "--volumes-from", redis_id, "redis:7.4-alpine", "tar", "-cf", "-", "-C", "/data", ".", stdout=f)

    set_stage("Удаляем проект")
    compose("down", "-v", "--rmi", "local")
    
    print("ПРОВЕРКИ ПРОЙДЕНЫ")

except (Exception, KeyboardInterrupt) as e:
    raise SystemExit(f"Ошибка на этапе {stage_count}. {stage}:\n{e}")
finally: # аналог trap
    subprocess.run(["docker", "compose", "-p", _proj, "down", "-v", "--rmi", "local"], cwd=_root, capture_output=True)