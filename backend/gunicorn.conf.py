# Gunicorn configuration for ZhaoLuSi FastAPI application

import multiprocessing

# Server socket
bind = "unix:/run/gunicorn/zhaolusi.sock"
umask = 0o007
user = "ubuntu"
group = "www-data"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
timeout = 120
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "/var/log/gunicorn/zhaolusi-access.log"
errorlog = "/var/log/gunicorn/zhaolusi-error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "zhaolusi-fastapi"

# Daemonize
daemon = False
pidfile = "/run/gunicorn/zhaolusi.pid"

# Security
limit_request_line = 0
limit_request_fields = 100
limit_request_field_size = 8190