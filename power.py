



from math import sqrt
import time
import random



class node:

    def __init__(self,):
        #only want to initialize this once
        self.lookup = {0:0}
        for e in range(2, 5000):
            self.lookup[e-1] = self.lookup[e-2]+e**2

    def find_viable(self,n,parent):
        i = parent # value of parent node
        il = parent-1
        re = []
        ma = int(sqrt(n))
        return [n for n in range(ma-1,0,-1)]

    def find_by_gen(self,n,parent):
        i = parent
        while i > 1: # once it dips below 2
            i -= 1
            try:
                if n == self.lookup[i]: # narrows down max value based on sum(i**2+(i-1)**2+...) > n in order to
                      yield [i for i in range(i,0,-1)]+[0]                  # get n to 0
                elif i**2 <= n: # since its narrowed down, just use the highest value
                    yield i
                else:
                    i = int(sqrt(n))+1 # if i is too high, this sets it to the max possible i value
            except KeyError:
                if i**2 <= n:
                    yield i
                else:
                    i = int(sqrt(n))+1
        yield -10 # for cases where i = 1; n < 0, throws out the containing list




def decompose(n,gen=True):
    root = node() # calling the dict holer
    iv = int(sqrt(n))

    ne =  search_tree(root,iv,n,gen)
    if ne:
        ne.reverse()
        return ne[1:]
    return None

def search_tree(root : node,val,next,gen=True):

    if gen:
        childeren = root.find_by_gen(next,val)
    else:
        childeren = root.find_viable(next,val)
    pot_branch = []

    for child in childeren:
        if child == -10: # non-viable solution
            #print('exir')
            break
        #print(f' child {child}',next)
        if isinstance(child,list):
            return child
        n = next - child**2

        if n == 0:
            extbranch = [child,0] # the 0 tells the program that this solution results in n = 0 and no repeats
            return extbranch # only one soln gives n = 0
        else:
            extbranch = [child] + search_tree(root,child,n) # stacking up the branch
        if not pot_branch and extbranch[-1] == 0:
            pot_branch = extbranch # if there are no possible solutions with the child values, this returns as empty
        elif pot_branch and extbranch[0] < pot_branch[0]: # testing to see if a new list is a better soluton
            if extbranch[0] < pot_branch[0]: # does the new array have larger squares?
                return pot_branch
    return pot_branch

if __name__ == '__main__':
    print(decompose(101))

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    import matplotlib.gridspec as gridspec
    from numpy import log10,log2
    import numpy as np
    r = [random.randrange(1,10000000) for _ in range(50)]
    r = sorted(r)
    time_per_item_gen = []
    time_per_item_list = []
    solcomplex = []
    numcomplex = []
    for z,i in enumerate(r):
        print(f'Iteraton : {z}\nNumber : {i}\n')
        t0 = time.time()
        a = decompose(i,False)
        ta = time.time()-t0
        t0 = time.time()
        b = decompose(i)
        tb = time.time()-t0
        if not a:
            time_per_item_gen.append([tb, tb])
            solcomplex.append(len(str(i)))
            numcomplex.append(numcomplex[-1])
            time_per_item_list.append([ta, ta])
        else:
            time_per_item_gen.append([tb,tb])
            solcomplex.append(len(str(i)))
            numcomplex.append(len(a))
            time_per_item_list.append([ta,ta])
        ttl,_ = zip(*time_per_item_list)
        ttz,_ = zip(*time_per_item_gen)
        avg = lambda tpi : sum([t for t in tpi])/len(tpi)

        print(f'With Generator : {tb}\nWith List Comp : {ta}\n'
              f'List Comp Scaling : {avg(ttl)}\n'
              f'Generator Scaling : {avg(ttz)}\n'
              f'List Result : {a}\nGen Result : {b}\n'
              )
    a,b = zip(*time_per_item_gen)
    c,d = zip(*time_per_item_list)
    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()
    ax = fig.add_subplot(gs[0,:])
    ax2 = fig.add_subplot(gs[1,:])
    r = [r**(3/4) for r in r]

    ax.scatter(x=r,y=d)
    ax.scatter(x=r, y=b)

    ax.set_ylabel('Time to Solve (s)')
    ax2.set_ylabel('Time to Solve (s)')
    ax.set_xlabel('Length of Number')
    ax.plot(np.unique(r), np.poly1d(np.polyfit(r, d, 3))(np.unique(r)))
    ax.plot(np.unique(r), np.poly1d(np.polyfit(r, b, 1))(np.unique(r)))
    ax2.set_xlabel('Length of Solution/ Number of Steps')
    ax2.scatter(x=numcomplex,y=d)
    ax2.scatter(x=numcomplex, y=b)
    ax2.plot(np.unique(numcomplex), np.poly1d(np.polyfit(numcomplex, d, 1))(np.unique(numcomplex)))
    ax2.plot(np.unique(numcomplex), np.poly1d(np.polyfit(numcomplex, b, 1))(np.unique(numcomplex)))
    plt.show()
