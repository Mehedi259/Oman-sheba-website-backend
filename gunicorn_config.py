"""Gunicorn configuration file for Sheba Backend"""

import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = '/var/log/gunicorn/sheba_access.log'
errorlog = '/var/log/gunicorn/sheba_error.log'
loglevel = 'info'

# Process naming
proc_name = 'sheba_backend'

# Server mechanics
daemon = False
pidfile = '/var/run/gunicorn/sheba.pid'
user = 'www-data'
group = 'www-data'
umask = 0o007

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
