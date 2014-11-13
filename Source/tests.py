import redis
from Node import Node
from Relation import Relation

rcli=redis.StrictRedis()

var = rcli.get('foo')
print var

node = Node(pvalue='b', prefid_dic = {Relation('next'):'1'}, pindexes={r'list\:1':'1'})
node.store()
rcli.set(node.id, node.json_value())
node2 = Node.Loads(rcli.get(node.id))
print node2
print node2.id
print node2.value
# rcli.zadd('')