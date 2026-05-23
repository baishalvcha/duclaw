
import re
p = '/opt/du-claw/docker-compose.yml'
with open(p) as f:
    c = f.read()
c = c.replace('"5432:5432"', '"5433:5432"')
c = c.replace('"6379:6379"', '"6378:6379"')
c = c.replace('"8000:8000"', '"8001:8000"')
with open(p, 'w') as f:
    f.write(c)
print("Ports fixed")
