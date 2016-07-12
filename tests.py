# Tests for dht
from dht import *

d = DHT(10)

# Add nodes
for i in range(10, 1024, 10):
    d.join(Node(i))

for i in range(5, 1024, 10):
    d.store(d._startNode, i, "hello" + str(i))

for i in range(5, 100, 10):
    print(d.lookup(d._startNode, i))
