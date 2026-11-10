#!/bin/sh
set -e

# If running as root (container default), fix permissions on persistent volumes and drop privileges
if [ "$(id -u)" = "0" ]; then
    for dir in /app/instance /app/uploads /app/data /app/data/keys /app/data/uploads /app/data/vault /app/keys; do
        if [ -d "$dir" ]; then
            chown -R 1000:1000 "$dir" 2>/dev/null || true
            chmod 775 "$dir" 2>/dev/null || true
        fi
    done
    exec setpriv --reuid=1000 --regid=1000 --init-groups "$@"
fi

exec "$@"
