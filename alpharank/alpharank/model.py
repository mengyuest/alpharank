class MetaQuery:
    def __init__(self):
        self.state="off" # On/Off/All
        self.key=None
        self.val=None
        self.prev=None
        self.change=None

class SelectQuery(MetaQuery):
    def __init(self):
        self.childrens=None

class RangeQuery(MetaQuery):
    def __init__(self):
        self.left_val=None
        self.right_val=None

class HierQuery(SelectQuery):
    def __init__(self):
        self.genre=None
        self.father=None
        self.childrens=[]

    def include(self,item):
        self.childrens.append(item)
        item.father=self

class Queries(MetaQuery):
    def __init__(self):
        self.SelectQueries=[]
        self.RangeQueries=[]
        self.HierQueries=[]
    
    def include(self,item):
        if type(item) is HierQuery:
            self.HierQueries.append(item)
        elif type(item) is RangeQuery:
            self.RangeQueries.append(item)
        elif type(item) is SelectQuery:
            self.SelectQueries.append(item)
