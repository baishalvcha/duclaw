#!/usr/bin/env python3
p = '/opt/du-claw/docker-compose.yml'
with open(p) as f:
    c = f.read()
c = c.replace('5433:5432', '5435:5432')
c = c.replace('6378:6379', '6379:6379')  # Actually port 6378 was fine, but let's just avoid all conflicts
with open(p, 'w') as f:
    f.write(c)
print("Ports updated")
# Also kill any docker proxy still holding ports
import subprocess as sp
sp.run(['pkill', '-f', 'docker-proxy.*5433'], capture_output=True)
