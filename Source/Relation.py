from __init__ import redclt


class Relation(object):
    
    def __init__(self, description):
        self.id = redclt.incr('relation:new_id')
        self.pattern = None
        self.description = description
    
    @property
    def pk(self):
        return 'relation:%s' % self.id