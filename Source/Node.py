import json
import redis

redclt = redis.StrictRedis()

def serialize(strlist):
    if strlist and isinstance(strlist, list):
        root = Node[strlist[0]]
        last = root
        for s in strlist[1:]:
            last = Node(pvalue=s, prefid=last.id)
        return root
    else:
        return None

class Node(object):
#     new_id = 0
    def __init__(self, pid = None, pvalue = None, prefid= None):
            
        if pid:
            self.id = pid
        else:
            self.id = redclt.incr('new_id')
#             self.id = Node.new_id
#             Node.new_id += 1
            
        if pvalue:
            self.value = pvalue
        else:
            self.value = None
            
        if prefid:
            self.refid = prefid
        else:
            self.refid = None
        
    def json_value(self):
        return json.dumps([self.id, self.value])
    
    @staticmethod
    def Loads(json_value):
        tid, tvalue = json.loads(json_value)
        return Node(tid, tvalue)
        