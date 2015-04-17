from methods import *
from group   import *

class WeylGroupoid:
    def __init__(self, braid, order):
        """
        Initializes WeylGroupoid, which has the information of an ARS.
        This is useful for braidings of diagonal type.
        """
        self.Braid = braid # braiding w.r.t. canonical basis
        self.Order = order
        #FIXME (this should be dealt with better)
        try:
            self.NumberOfParameters = len(self.Braid[0][0])
        except TypeError:
            self.NumberOfParameters = 1
        self.Rank = len(self.Braid)
        self.Bases = [range(self.Rank)]
        self.Inverses = [range(self.Rank)]
        # Construct canonical basis, self.Bases and self.Inverses
        for i in xrange(self.Rank):
            self.Bases[0][i] = [0 for x in xrange(self.Rank)]
            self.Bases[0][i][i] = 1

            self.Inverses[0][i] = [0 for x in xrange(self.Rank)]
            self.Inverses[0][i][i] = 1
        # Initialize the groupoid with canonical basis
        self.__calculate_bases()
        self.change_basis(0)
        # Define self.Isogroup as a finite group
        self.Isogroup = FiniteGroup([],[[]])

    def change_basis(self, n):
        """
        We change CurrentBasis and we compute roots accordingly.
        """
        self.CurrentBasis = (n % len(self.Bases))
        self.__calculate_roots()

    def roots(self):
        return self.PosRoots, self.NegRoots

    def basis(self):
        return self.CurrentBasis, self.Bases[self.CurrentBasis]

    def newq(self,b):
        return self.braid_for_basis(b)

    def braid_for_basis(self,b):
        nb = [[0 for i in range(self.Rank)] for j in range(self.Rank)]
        for i in xrange(self.Rank):
            for j in xrange(self.Rank):
                nb[i][j] = self.braid_v1v2(b[i],b[j])
        return nb

    def apply_reflection(self, i):
        """
        Changes the variable CurrentBasis according to the reflection
        on the i-th basis element of the current basis
        """
        nbasis,ninv = self.__s( self.braid_for_basis(self.Bases[self.CurrentBasis]) ,\
                self.CurrentBasis , (i % self.Rank) )
        self.change_basis( self.Bases.index(nbasis) )

    def __calculate_bases(self):
        # Calculate the bases of the WeylGroupoid
        cal = 0
        while cal < len(self.Bases):
            newbraid = self.braid_for_basis(self.Bases[cal])

            for i in xrange(self.Rank):
                newbasis,newinv = self.__s(newbraid, cal, i)
                if newbasis not in self.Bases:
                    self.Bases = self.Bases + [newbasis]
                    self.Inverses = self.Inverses + [newinv]
            cal += 1

    def __calculate_roots(self):
        self.Roots = []
        self.PosRoots = []
        self.NegRoots = []
        for i in self.Bases:
            for j in i:
                if j not in self.Roots:
                    self.Roots = self.Roots + [j]
                    #if self.__ispositive(j,0):
                    if self.__ispositive(j):
                        self.PosRoots = self.PosRoots + [j]
                    else:
                        self.NegRoots = self.NegRoots + [j]

    def calculate_isogroup(self):
        """
        Calculates the isotropy group of the Dynkin diagram of the standard basis
        """
        braid0 = triang(self.NumberOfParameters,self.braid_for_basis(self.Bases[0]),self.Order)
        elts = []
        for i in range(len(self.Bases)):
            braid = triang(self.NumberOfParameters,self.braid_for_basis(self.Bases[i]),self.Order)
            if braid0 == braid:
                elts.append(i)
        paths = []
        for i in elts:
            paths.append(self.find_path(0,i))
        Ct = []
        for i in elts:
            Ctline = []
            for j in range(len(elts)):
                Ctline.append(self.endbasis(i,paths[j]))
            Ct.append(Ctline)
        self.Isogroup = FiniteGroup(elts, Ct)

    def pathlength(self, b1, b2):
        """Calculates the length of the path between two bases"""
        pl=0
        for j in self.Roots:
            if self.__ispositive(j,b1):
                if not(self.__ispositive(j,b2)):
                    pl+=1
        return pl

    def find_path(self, b1, b2):
        # Find a shortest path between two bases
        b1 = b1 % len(self.Bases)
        b2 = b2 % len(self.Bases)
        path = []
        pl=self.pathlength(b1,b2)
        while not pl==0:
            newbraid = self.braid_for_basis(self.Bases[b1])
            for i in xrange(self.Rank):
                newbasis = self.Bases.index(self.__s4findpath(newbraid, self.Bases[b1], i))
                if self.pathlength(newbasis ,b2)<pl:
                    b1=newbasis
                    pl -=1
                    path.append(i)
                    break
        return path

    def allpaths(self,b1,b2,trunc):
        """
        Finds all shortest paths between two bases. Stops if more than <trunc> paths are available.
        If trunc = 0 then there is no truncation.
        Returns an array of paths and the boolean value True/False
        which tells whether the array is truncated or not.
        """
        b1 = b1 % len(self.Bases)
        b2 = b2 % len(self.Bases)
        pl=self.pathlength(b1,b2)
        if pl==0:
            return [[]],False
        newbraid = self.braid_for_basis(self.Bases[b1])
        paths=[]
        for i in xrange(self.Rank):
            newbasis = self.Bases.index(self.__s4findpath(newbraid, self.Bases[b1], i))
            if self.pathlength(newbasis ,b2)<pl:
                if trunc == 0:
                    npaths,tr = self.allpaths(newbasis,b2,0)
                    for p in npaths:
                        paths.append([i]+p)
                else:
                    t1 = trunc - len(paths)
                    if t1 == 0:
                        return paths, True
                    npaths,tr = self.allpaths(newbasis,b2,t1)
                    for p in npaths:
                        paths.append([i]+p)
                    if tr:
                        return paths, True
        return paths, False            

    def endbasis(self, startbasis, path):
        """
        Calculates the basis corresponding to a given path with a given starting basis.
        The reflections are applied from left to right in the path.
        """
        for i in path:
            newbraid = self.braid_for_basis(self.Bases[startbasis])
            startbasis = self.Bases.index(self.__s4findpath(newbraid, self.Bases[startbasis], i))
        return startbasis
    
    def cox_ij(self,basis,i,j):
        """
        Calculates the number of elements of self.Posroots which are linear
        combinations of self.Bases[basis][i] and self.Bases[basis][j]
        (assume that i is different from j).
        """
        cij=0
        bi=self.Bases[basis][i]
        bj=self.Bases[basis][j]
        for r in self.PosRoots:
            co = True
            i1=0
            while (i1<self.Rank) and co:
                i2=i1+1
                while (i2<self.Rank) and co:
                    i3=i2+1
                    while (i3<self.Rank) and co:
                        m=[[r[i1],r[i2],r[i3]],[bi[i1],bi[i2],bi[i3]],[bj[i1],bj[i2],bj[i3]]]
                        if not(det3(m)==0):
                            co = False
                        i3+=1
                    i2+=1
                i1+=1
            if co:
                cij+=1
        return cij

    def print_bases(self):
        print 'Bases:';
        for i in xrange(len(self.Bases)):
            print i, self.Bases[i];
        #if self.CurrentBasis != None:
        print 'Current basis: ', self.CurrentBasis;

    def print_roots(self):
        print '\nSimple roots are: ',self.Bases[self.CurrentBasis];
        print 'Positive roots:';
        for v in self.PosRoots:
            print v;
        print 'Negative roots:';
        for v in self.NegRoots:
            print v;

    def print_path(self,path):
        """
        Returns a string containing a given path in the Weyl groupoid.
        """
        if self.Rank<10:
            sep=""
        else:
            sep=" "
        pp = ""
        for i in path:
            pp = pp + sep + str(i+1)
        return pp

    def save4gnuplot(self, filename, description, drawsimples=True, drawarrows=False, pointsize=3):
        # only save if rank is 2 or 3
        try:
            file=open(filename, 'w')
        except:
            print 'File error: can\'t open file',filename;
            sys.exit(0);
        file.write('# Arithmetic Root System\n');
        file.write('# for %s with basis %s\n' % ( description, self.Bases[self.CurrentBasis] ))
        file.write('# use: load <filename>\n\n');
        file.write('unset arrow\n');
        file.write('unset label\n');
        file.write('set key off\n');
        file.write('set title \"%s with basis %s\"\n' % (description, self.Bases[self.CurrentBasis]));
        file.write('set pointsize %d\n' % pointsize);
        file.write('set ticslevel 0\n');
        file.write('set border -1 lw 1 lt 0\n');
        file.write('set xtics 1; set ytics 1; set ztics 1;\n');

        # we always have self.Rank==2 or self.Rank==3
        if self.Rank==2:
            orig = '0,0'
        else:
            orig = '0,0,0'
        # if arrows are wanted, we draw them
        if drawarrows:
            for v in self.PosRoots:
                file.write('set arrow from '+orig+' to ')
                for i in xrange(self.Rank-1):
                    file.write('%d,' % v[i] );
                file.write('%d lt -1 nohead \n' % v[self.Rank-1]);
            for v in self.NegRoots:
                file.write('set arrow from '+orig+' to ')
                for i in xrange(self.Rank-1):
                    file.write('%d,' % v[i]  );
                file.write('%d lt -1 nohead \n' % v[self.Rank-1]);
        # we draw the canonical basis
        elif drawsimples:
            epsilon = 1.2
            for i in xrange(self.Rank):
                file.write('set arrow from '+orig+' to ')
                for j in xrange(self.Rank-1):
                    file.write('%d,' % self.Bases[self.CurrentBasis][i][j])
                file.write('%d lt -1 nohead\n' % self.Bases[self.CurrentBasis][i][self.Rank-1])
            for i in xrange(self.Rank):
                file.write('set label \'v%d\' at ' % (i+1))
                for j in xrange(self.Rank-1):
                    file.write('%.2f,' %(epsilon*self.Bases[self.CurrentBasis][i][j]))
                file.write('%.2f\n' %(epsilon*self.Bases[self.CurrentBasis][i][self.Rank-1]))
        if self.Rank == 3:
            file.write('splot "-" pt 7, "-" pt 7 lt 3, "-" pt 7 lt -1 ps 4\n\n')
        elif self.Rank == 2:
            file.write('plot "-" pt 7, "-" pt 7 lt 3, "-" pt 7 lt -1 ps 4\n\n')

        file.write('# positive roots:\n')
        for v in self.PosRoots:
            for i in xrange(self.Rank):
                file.write('%5d ' %v[i]);
            file.write('\n')

        file.write('end\n\n# negative roots:\n')
        for v in self.NegRoots:
            for i in xrange(self.Rank):
                file.write('%5d ' %v[i]);
            file.write('\n')

        file.write('end\n\n# origin:\n '+orig+'\nend\n')
        file.write('\npause -1\n')
        file.close()

    def __m(self, braid, i, j):
        """Computes m_{ij}=min { m >=0 | (m+1)*q_ii=0 or m*q_ii+q_ij+q_ji = 0}, where q_ij=braid[i][j]"""
        m = 0;
        if (i==j):
            return -2;
        else:
            while notone(self.NumberOfParameters, \
                    add( self.NumberOfParameters, \
                        mult(self.NumberOfParameters, braid[i][i], m), \
                        braid[i][j], braid[j][i] ) , self.Order) \
                    and notone( self.NumberOfParameters, mult(self.NumberOfParameters, braid[i][i], m+1) , self.Order ):
                m+=1;
            return m;

    # s_i(e_j)=e_j+m_ij*e_i
    def __s(self,braid,basis,i):
        """Computes the array newbasis=[s_i(e_1),...,s_i(e_n)], where n=self.Rank and
           basis=(number of the basis {e_1,...,e_n}).
           Uses braid=array of the structure constants of the braiding corresponding to basis.
           Computes also the array newinverse, which is the transposed matrix of the inverse of newbasis
           (considered as a matrix).
        """
        newbasis = [];
        for j in xrange(self.Rank):
            tmp_basis = [0 for x in xrange(self.Rank)]
            for k in xrange(self.Rank):
                tmp_basis[k] = self.__m(braid,i,j) * self.Bases[basis][i][k] + self.Bases[basis][j][k];
            newbasis.append(tmp_basis);
        newinverse = [];
        newinverse = [[self.Inverses[basis][j][k] for k in xrange(self.Rank)] for j in xrange(self.Rank)]
        for j in xrange(self.Rank):
            for k in xrange(self.Rank):
                newinverse[i][j] += self.__m(braid,i,k) * self.Inverses[basis][k][j]
        return newbasis,newinverse;

    def braid_v1v2(self,v1,v2):
    # calculates braid(v,w) for vectors v1, v2 with integer coefficients
        if self.NumberOfParameters == 1:
            s = 0
        else:
            s = [0 for k in range(self.NumberOfParameters)]
        for k in xrange(self.Rank):
            for l in xrange(self.Rank):
                s = add(self.NumberOfParameters, s, mult(self.NumberOfParameters, self.Braid[k][l], v1[k] * v2[l]))
        return normalize(self.NumberOfParameters,s,self.Order)

    def __s4findpath(self,braid,b,i):
        """
        Calculates the basis s_i(b), where b corresponds to the braiding
        braid.
        i takes values between 0 and self.Rank-1.
        """
        newbasis = []
        for j in xrange(self.Rank):
            tmp_basis = [0 for x in xrange(self.Rank)]
            for k in xrange(self.Rank):
                tmp_basis[k] = self.__m(braid,i,j) * b[i][k] + b[j][k]
            newbasis.append(tmp_basis)
        return newbasis

    def __ispositive(self, root, basis=None):
        """Returns True if root is positive with respect to basis (number
        between 0 and number of bases -1) and False otherwise."""
        if basis==None:
            basis=self.CurrentBasis
        for i in xrange(self.Rank):
            tmp = 0
            for j in xrange(self.Rank):
                tmp += self.Inverses[basis][i][j] * root[j]
            if tmp > 0:
                return True
            elif tmp < 0:
                return False


# Path objects are created to be used in connection with Weyl groupoids.
# Most functions require a Weyl groupoid as an argument.
#
# class Path:
#     def __init__(self, wg, reflarray, startbasis):
#         """
#         Initialize a Path object using a WeylGroupoid object wg, an array
#         of reflections (array of integers) and a startbasis (integer).
#         """
#         self.ReflArray = reflarray
#         self.Bases = range(len(reflarray))
#         self.Bases[0]=startbasis
#         i=1
#         while i<len(reflarray):
#             self.Bases[i]=wg.endbasis(self.Bases[i-1],[reflarray[i-1]])
#             i+=1
#         self.EndBasis=wg.endbasis(self.Bases[i-1],[reflarray[i-1]])
# 
#     def s2(self,kill):
#         """
#         Looks for places i in the path where
#         self.ReflArray[i]=self.ReflArray[i+1]. If kill is True then the
#         function is shortening the path by killing these repetitions.
#         Otherwise the first place is returned where such a repetition
#         appears (-1 for no repetitions).
#         """
#         i=1
#         while i<len(self.ReflArray):
#             if self.ReflArray[i]==self.ReflArray[i-1]:
#                 if kill:
#                     self.ReflArray.pop(i)
#                     self.ReflArray.pop(i-1)
#                     if i>1:
#                         i-=1
#                 else:
#                     return i-1
#             else:
#                 i+=1
#         if not kill:
#             return -1
# 
#     def coxeter(self,wg,i):
#         """
#         Looks for the first position >=i in the path where a Coxeter
#         relation can be applied. It will be assumed that there are no
#         repetitions in the path.
#         If there is no such position, the return value is -1.
#         There is a second return value, which is the number c_ij determining
#         the Coxeter relation on the determined position.
#         """
#         i+=1
#         while i<len(self.ReflArray):
#             i0=self.ReflArray[i-1]
#             i1=self.ReflArray[i]
#             if i0==i1:
#                 i+=1
#                 continue
#             cij=wg.cox_ij(self.Bases[i-1],i0,i1)
#             if i+cij>len(self.ReflArray)+1:
#                 i+=1
#                 continue
#             con = True
#             for k in range(1,cij-1):
#                 if not(self.ReflArray[i+k]==i0):
#                     con = False
#                     break
#                 i2=i0
#                 i0=i1
#                 i1=i2
#             if con:
#                 return i-1,cij
#             i+=1
#         return -1,0
# 
#     def coxclass(self,wg,trunc):
#         """
#         Determines all paths which can be obtained from the given path using
#         Coxeter relations.
#         No simplifications s^2=id are used.
#         """
#         cc = [self.ReflArray]
#         cc1 = [self]
#         while len(cc1)>0:
#             pth = cc1.pop()
#             i,cij=pth.coxeter(wg,0)
#             while i>=0:
#                 rarray=pth.ReflArray[:]
#                 rarray.insert(i+cij,rarray[i+cij-2])
#                 rarray.pop(i)
#                 pth1=Path(wg,rarray,pth.Bases[0])
#                 try:
#                     j=cc.index(pth1.ReflArray)
#                 except ValueError:
#                     if len(cc)==trunc:
#                         return cc,True
#                     cc1.append(pth1)
#                     cc.append(pth1.ReflArray)
#                 i,cij=pth.coxeter(wg,i+1)
#         return cc,False
# 
# 
# vim:ts=4:sw=4:expandtab:
