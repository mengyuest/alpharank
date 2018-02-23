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

class University(object):
    def __init__(self):
        #load
        self.name="Tsinghua University"
        self.faculties=[]

        #cal
        self.g=0 #geomean score
        self.f=0 #faculty with more than one papers

    def allocate(self, areaNum):
        self.g=[0 for x in range(areaNum)]

    def updateG(self, credit, areaId):
        self.g[areaId]+=credit

    def calG(self):
        G=1
        M=len(self.g)
        for g in self.g:
            G=G*((1+g)**(1.0/M))
        self.g=G

    def calF(self):
        self.f=0
        for faculty in self.faculties:
            self.f+=int(faculty.p>0.5)#Tricky...Never compare to zero...

    def sort(self):
        self.faculties=sorted(self.faculties, key=lambda x:x.p, reverse=True)

    def __str__(self):
        return self.name+"@"+str(self.g)+"$"+str(self.f)#+"@@"+(str)([str(x) for x in self.faculties])

    def __repr__(self):
        return repr((self.name,self.faculties,self.g,self.f))

    def valid(self):
        return (self.g>1.001)

    def dump(self):
        faculties = [x.dump() for x in self.faculties if x.valid()]
        return{
        "name":self.name,
        "faculties":faculties,
        "g":"{0:.2f}".format(self.g),
        "f":self.f
        }


class Faculty(object):
    def __init__(self):
        #load
        self.name=[]
        self.scholarid="google scholar ID"
        self.affiliation=None
        self.homepage="WWW"

        #cal
        self.p=0 #papers
        self.c=0 #credits


    def __repr__(self):
        return repr((self.name,self.scholarid,self.affiliation,self.homepage))

    def allocate(self):#, areaNum):
        self.p=0#[0 for x in range(areaNum)]
        self.c=0#[0 for x in range(areaNum)]

    def updateP(self):#, areaId):
        self.p+=1 #self.p[areaId]=1

    def updateC(self, credit):#, areaId):
        self.c+=credit #self.c[areaId]=1

    def __str__(self):
        return "$$FAC$$"+str(self.name)+"$$"+str(self.p)

    def valid(self):
        return self.p>0.5 and self.c > 0.09

    def dump(self):
        return {
        "name":self.name[0],
        "scholarId":self.scholarid,
        "affiliation":self.affiliation,
        "homepage":self.homepage,
        "p":"{0}".format(self.p),
        "c":"{0:.2f}".format(self.c)
        }
