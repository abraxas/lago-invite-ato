#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME=lago-invite-ato-lab

echo "== docker compose up (getlago/lago:v1.53.0, loopback) =="
docker compose up -d

echo "== wait for GraphQL =="
ok=0
for i in $(seq 1 90); do
  if curl -fsS -o /dev/null http://127.0.0.1:13000/health; then
    echo "IOC lago-up"
    ok=1
    break
  fi
  sleep 3
done
if [[ "$ok" != 1 ]]; then
  echo "FAIL Lago API did not become ready on 127.0.0.1:13000"
  docker compose logs --tail=80
  exit 1
fi

# Give migrations / boot a beat after /health.
sleep 5

if [ -f poc.py ]; then
  POC=./poc.py
elif [ -f ../lago-invite-ato-Abraxas-Labs.py ]; then
  POC=../lago-invite-ato-Abraxas-Labs.py
else
  echo "FAIL no poc.py"
  exit 1
fi
chmod +x "$POC"

echo "== poc.py =="
python3 "$POC" http://127.0.0.1:13000
