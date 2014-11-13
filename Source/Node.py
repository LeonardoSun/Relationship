import json
from __init__ import redclt

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
    def __init__(self, pid = None, pvalue = None, prefid_dic= {}, pindexes = {}):
            
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
            self.refid_dic = {}
            
        # ----    indexes    ----
        if pindexes:
            self.indexes = pindexes
        else:
            self.indexes = {}
            
    def store(self):
        
#         pipeline = redclt.pipeline()
        redclt.hset('node:%s' % self.id, 'value', self.value)
        
#         lua_index = r'''
#         local indexes_k = redis.call('incr', 'node:indexes_k')
#         for i=1, #ARGV do
#             redis.call('sadd', 'node:'..indexes_k, ARGV[i])
#         end
#         redis.call('hset', 'node:'..KEYS[1], 'indexes', indexes_k)
#         return indexes_k
#         '''
#         store_index = redclt.register_script(lua_index)
#         store_index(keys=[self.id], args=self.indexes.keys(), client=pipeline)
                
        indexes_k = redclt.incr('node:indexes_k')
        for key, value in self.indexes.items():
            redclt.sadd(r'node\:%s' % indexes_k, r'%s\:%s' % (key, value))
        redclt.hset('node:%s' % self.id, 'indexes', indexes_k)
        
#         lua_refid = r'''
#         local refids_k = redis.call('incr', 'node:refids_k')
#         for i=1, #ARGV do
#             redis.call('hset', 'node:'..refids_k, KEYS[i+1], ARGV[i])
#         end
#         redis.call('hset', 'node:'..KEYS[1], 'refid_dic', refids_k)
#         return refids_k
#         '''
#         store_index = redclt.register_script(lua_refid)
#         keys = [self.id]
#         args = []
#         for relation, refid in self.refid_dic.items():
#             keys.append(relation.pk)
#             args.append(refid)
#         store_index(keys=keys, args=args, client=pipeline)
        
        refids_k =  redclt.incr('node:refids_k')
        for relation, refid in self.refid_dic.items():
            redclt.hset('node:%s' % refids_k, relation.pk, refid)
        redclt.hset('node:%s' % self.id, 'refid_dic', refids_k)
        
#         pipeline.execute()
        
    def json_value(self):
        return json.dumps([self.id, self.value])
    
    @staticmethod
    def Loads(json_value):
        tid, tvalue = json.loads(json_value)
        return Node(tid, tvalue)
        