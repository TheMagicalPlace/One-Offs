



from math import sqrt
import time
import random

from collections import defaultdict

class node:

    def __init__(self):
        #only want to initialize this once
        self.lookup = {0:0}
        for e in range(2, 5000):
            self.lookup[e-1] = self.lookup[e-2]+e**2
        self.gen = defaultdict(list)
    def find_viable(self,n,parent):
        i = parent # value of parent node
        il = parent-1
        re = []
        ma = int(sqrt(n))
        return [n for n in range(ma-1,0,-1)]

    def find_by_gen(self,n,parent):
        i = parent+1
        while i > 1: # once it dips below
            if i == 1:
                yield 1
            try:
                if i**2 <= n and n !=1: # since its narrowed down, just use the highest value
                    yield i
                else:
                    i = int(sqrt(n))+1 # if i is too high, this sets it to the max possible i value
                i -= 1
            except GeneratorExit:
                raise GeneratorExit






def decompose(n,gen=True):
    root = node() # calling the dict holer
    iv = int(sqrt(n))
    if n <= 3:
        return [1 for _ in range(n)]
    if iv**2 == n:
        return [iv]

    ne =  search_tree(root,iv,n,last_pot=None,gen=True,generation=1)
    print("\n\n".join([f"\n{k} :".join([f"".join(str(l)) for l in root.gen[k]]) for k in sorted(root.gen)]))

    if ne:
        ne.reverse()
        return ne[:-1]
    return None

def search_tree(root : node,parent,next,last_pot = None,gen=True,generation=0):

    if gen:
        childeren = root.find_by_gen(next,parent)
    else:
        childeren = root.find_viable(next,parent)
    pot_branch = []
    last = None
    par = [parent]
    for child in childeren:
        if child == last == 1:
            if next == 1:
                pot_branch = [1]
                break
            else:
                pot_branch = [_ for _ in range(next)]
                break
        else:
            last = next
            n = next - child**2
            if n < 0: break

        if pot_branch:
            print(generation,pot_branch,child)

        if n <=3 and n > 0:
            pot = [child]+[1 for i in range(n)]
            pot_branch = pot
        elif child == 1:
            if last_pot and len(last_pot) > n:
                pot = last_pot
            else:
                pot_branch =[child for n in range(n)]
                break
        else:
            pot = search_tree(root, child, n, last_pot=pot_branch,generation=1+generation)

        if not pot_branch:
            pot_branch = pot
        elif pot_branch and len(pot) <= len(pot_branch):
            if len(pot) < len(pot_branch):
                pot_branch = pot
            elif pot[0] > pot_branch[0]:
                pot_branch = pot
        elif pot_branch:
            if len(pot_branch) < len(pot):
                break


    par = par + pot_branch
    #print(f'returned : {par}\ngeneration : {generation}')
    root.gen[generation].append(par)
    return par

if __name__ == '__main__':
    td = time.time()
    print(f'decompose {decompose(188739465)}')
    #print(sum([x**2 for x in decompose(15)]))
    print(decompose(4 *9 *82))
    for i in range(-1,0,-1):
        t0 = time.time()
        res =  decompose(i)

        print(f'resultant vector for {i} = {res}\n')
        print(f'Total Time : {time.time()-t0}\n')
        res = sum([r**2 for r in res])
        assert res == i
    print(f'Total Time : {time.time()-td}\n Runs Per Second : {(time.time()-td)/100000}')

if __name__ == 'mem':
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
