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
    def __init__(self, pid = None, pvalue = None, prefid_dic= {}, pindexes = []):
            
        # ----    id    ----
        if pid:
            self.id = pid
        else:
            self.id = redclt.incr('node:new_id')
#             self.id = Node.new_id
#             Node.new_id += 1
            
        # ----    value    ----
        if pvalue:
            self.value = pvalue
        else:
            self.value = None
            
        # ----    refid_dic    ----
        if prefid_dic:
            self.refid_dic = prefid_dic
        else:
            self.refid_dic = None
            
        # ----    indexes    ----
        if pindexes:
            self.indexes = pindexes
        else:
            self.indexes = None
            
    def store(self):
        
        redclt.hset('node:%s' % self.id, 'value', self.value)
        
        indexes_k = redclt.incr('node:indexes_k')
        for index in self.indexes:
            redclt.sadd('node:%s' % indexes_k, index)
        redclt.hset('node:%s' % self.id, 'indexes', indexes_k)
        
        refids_k =  redclt.incr('node:refids_k')
        for relation, refid in self.refid_dic.items():
            redclt.hset('node:%s' % refids_k, relation.pk, refid)
        redclt.hset('node:%s' % self.id, 'refid_dic', refids_k)
        
    def json_value(self):
        return json.dumps([self.id, self.value])
    
    @staticmethod
    def Loads(json_value):
        tid, tvalue = json.loads(json_value)
        return Node(tid, tvalue)
        