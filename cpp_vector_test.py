
from typing import List,Any
from copy import copy
class CPPVector():
    """python implimentation of a c++ style vector, essentially the same behavior as a pythom
    list since python doesn't have pointers. """
    class node():

        def __init__(self,datum,container):
            self.pos = container.length
            self._datum = datum
            container.length += 1
            self.child = None

        def reassign_pos(self,new_pos):
            self.pos = new_pos
            if self.child is None:

                return
            else:
                self.child.reassign_pos(new_pos+1)
                return


        def __str__(self):
            return str(self._datum)

    def reassign_pos(self, node,new_pos):
        node.pos = new_pos
        if node.child is None:
            self.enode = node
            return
        else:
            self.reassign_pos(node.child,new_pos + 1)
            return

    def __init__(self,data: List[Any]):
        self.length = 0
        if not isinstance(data, list):
            self.snode = self.node(data,self)
            self.enode = self.snode
        else:
            self.snode = self.node(data[0],self)
            lastnode = self.snode
            if not isinstance(data,list):
                lastnode
            for datum in data[1:]:
                lastnode.child = self.node(datum,self)
                lastnode = lastnode.child
            self.enode = lastnode

    def __getitem__(self, index):
        if isinstance(index,slice):
            return self._get_many(index.start,index.stop,index.step)
        if index < 0:
            index = self.length + index
        lnode = self.snode
        while lnode.child is not None or lnode.pos <= index:
            if lnode.pos == index:
                return lnode._datum
            lnode = lnode.child
        else:
            raise IndexError

    def __setitem__(self, index, value):
        if index < 0:
            index = self.length + index
        lnode = self.snode # current node, starting from 0
        while lnode.child is not None or lnode.pos <= index:
            if lnode.pos == index:
                # when assigning a value from one vector to another i.e. v[2] = vv[2]
                if isinstance(value,self.node):
                    lnode._datum = value._datum  # to emulate immutable behavior, since copy doesnt create a new
                                                       # object for references(i.e. a list) but does for an immutable type
                # when assigning a new value from a non-vector i.e. v[2] = 1
                else:
                    lnode._datum = value # just modify the extant node
                return
            lnode = lnode.child
        else:
            raise IndexError

    def __iadd__(self, other):
        if isinstance(other,list) or isinstance(other,tuple):
            for datum in other:
                self.append(datum)
        elif isinstance(other,type(self)):
            olnode= other.snode
            while olnode.child is not None:
                self.append(olnode)
                olnode = olnode.child
            else:
                self.append(olnode)
                return self

    def append(self,value):
        if isinstance(value,type(self.snode)):
            self.enode.child = self.node(value._datum,self)
        else:
            self.enode.child = self.node(value,self)
        self.enode = self.enode.child

    def pop(self,start,end=None):
        if end is not None:
            return self._pop_many(start,end)
        else:
            index = start
        lnode = self.snode

        while lnode.pos <= index:
            # if the first node is the index node, return it and make its child the new start node
            if lnode.pos == index and lnode == self.snode:
                tmp = self.snode._datum
                self.snode = self.snode.child
                self.reassign_pos(self.snode,0)
                self.length -= 1
                return tmp

            # if the child node is the end node, return it and make the parent the new end node
            elif lnode.child.pos == index and lnode.child == self.enode:
                tmp = lnode.child._datum
                lnode.child = None
                self.enode = lnode
                self.length -= 1
                return tmp

            # otherwise the list has to be changed such that the remaining nodes are reassigned their positions
            elif lnode.child.pos == index and lnode.child is not self.enode:
                    tmp = lnode.child._datum
                    lnode.child = lnode.child.child
                    self.reassign_pos(lnode.child,index)
                    self.length -= 1
                    return tmp
        else:
            raise IndexError

    def _pop_many(self,start,end):
        i = start+1
        new_list = CPPVector(self.pop(start))
        while i != end:
            new_list.append(self.pop(start))
            i += 1
        return new_list

    def _get_many(self,start,end,step=1):
        new = CPPVector(self[start])
        if step is None: step =1
        i = start + step
        while i < end:
            new.append(self[i])
            i +=2
        return new

    def __str__(self):
        pass


if __name__ == '__main__':
    v1 = CPPVector([1,2,'bepis',1,1])
    v2 = CPPVector([2,2,2,2,2])
    v3 = v2
    v3[2] = v1[2]
    v1[2] = 'yeet'
    t1 = [1,2,3]
    t2 = [4,5,6]
    t2[2] = t1[2]
    t1[2] = 22
    t = v1.pop(1)
    t2 = v2.pop(0,3)
    t3 = v1[1:3]
    t3+=t2
    print(v2[4].pos,v1[4].pos,v2 is v3)
    print(v2)