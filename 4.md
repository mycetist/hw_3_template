me@mac hw_3_template % docker build -t counter-app .
[+] Building 1.4s (10/10) FINISHED  docker:desktop-linux
 => [internal] load build definition from Dockerfi  0.0s
 => => transferring dockerfile: 268B                0.0s
 => [internal] load metadata for docker.io/library  1.3s
 => [internal] load .dockerignore                   0.0s
 => => transferring context: 64B                    0.0s
 => [1/5] FROM docker.io/library/python:3.13-slim@  0.0s
 => => resolve docker.io/library/python:3.13-slim@  0.0s
 => [internal] load build context                   0.0s
 => => transferring context: 94B                    0.0s
 => CACHED [2/5] WORKDIR /app                       0.0s
 => CACHED [3/5] COPY app/requirements.txt .        0.0s
 => CACHED [4/5] RUN pip install --no-cache-dir -r  0.0s
 => CACHED [5/5] COPY app/app.py .                  0.0s
 => exporting to image                              0.0s
 => => exporting layers                             0.0s
 => => exporting manifest sha256:b57ed37869236f5e4  0.0s
 => => exporting config sha256:a1be41178cce14b4940  0.0s
 => => exporting attestation manifest sha256:3dd36  0.0s
 => => exporting manifest list sha256:b372cfc45e36  0.0s
 => => naming to docker.io/library/counter-app:lat  0.0s
 => => unpacking to docker.io/library/counter-app:  0.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/4srmrry10yzopabz7kax65yn2
me@mac hw_3_template % docker run -d --name counter -p 8080:8000 -e GREETING="hi docker" counter-app
123f5840c72f53259764867b22de7e7a941bacd3f75718500300c5bc6c88e255
me@mac hw_3_template % curl http://127.0.0.1:8080/
{"greeting": "hi docker", "count": 0, "hostname": "123f5840c72f", "storage": "sqlite"}%                           
me@mac hw_3_template % curl -X POST http://127.0.0.1:8080/increment
{"greeting": "hi docker", "count": 1, "hostname": "123f5840c72f", "storage": "sqlite"}%                           
me@mac hw_3_template % curl -X POST http://127.0.0.1:8080/increment
{"greeting": "hi docker", "count": 2, "hostname": "123f5840c72f", "storage": "sqlite"}%                           
me@mac hw_3_template % curl http://127.0.0.1:8080/
{"greeting": "hi docker", "count": 2, "hostname": "123f5840c72f", "storage": "sqlite"}%                           
me@mac hw_3_template % docker logs counter
2026-11-17 11:21:55,510 listening port=8000 storage=sqlite
2026-11-17 11:22:00,629 http 192.168.65.1 "GET / HTTP/1.1" 200 -
2026-11-17 11:22:05,957 http 192.168.65.1 "POST /increment HTTP/1.1" 200 -
2026-11-17 11:22:09,376 http 192.168.65.1 "POST /increment HTTP/1.1" 200 -
2026-11-17 11:22:12,634 http 192.168.65.1 "GET / HTTP/1.1" 200 -
me@mac hw_3_template % docker rm -f counter
counter
me@mac hw_3_template % 