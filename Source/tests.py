import redis
from Node import Node

rcli=redis.StrictRedis()

var = rcli.get('foo')
print var

node = Node(pvalue='a')
rcli.set(node.id, node.json_value())
node2 = Node.Loads(rcli.get(node.id))
print node2
print node2.id
print node2.value
# rcli.zadd('')