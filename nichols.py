from methods import gcd,height,multpol

class NicholsAlgebra:
    def __init__(self, groupoid = None):
        if groupoid != None:
            self.Groupoid = groupoid
            self.Rank = self.Groupoid.Rank

    def __hiln(self, n, v):
        if n == 0:
            return ""
        h = 0;
        for d in range(self.Rank):
            h += v[d]
        if h<0:
            h=-h
        h = n*h
        if h==1:
            return ("(1-x)")
        else:
            return ("(1-x^" + str(h)+")")

    def __hilnq(self, n, v, trunc=0):
        r = [1]
        h = 0;
        for d in range(self.Rank):
            h += v[d]
        if h<0:
            h=-h
        if trunc>0:
            if n==0:
                n = trunc/h + 1
            else:
                n = min( (trunc/h) + 1, n)
        for i in xrange(1,n):
            for j in xrange(1,h):
                r += [0]
            r += [1]
        return r

    def dimension(self):
        """ calculates the dimension of the Nichols algebra """
        if self.Groupoid.Order == 0:
            return 0
        dim = 1
        for i in self.Groupoid.PosRoots:
            j = self.Groupoid.braid_v1v2(i,i)
            dim *= height(self.Groupoid.Order, j)
        return dim

    def roots_coefs(self):
        ret = []
        for v in self.Groupoid.PosRoots:
            j = self.Groupoid.braid_v1v2(v,v)
            ret.append([v,j,height(self.Groupoid.Order, j)])
        return ret

    def hilbertseries(self, pp=False):
        """ calculates the Hilbert series of the Nichols algebra """
        nom,denom = "",""
        for i in self.Groupoid.PosRoots:
            j = self.Groupoid.braid_v1v2(i,i)
            denom = denom + self.__hiln(1,i)
            nom = nom + self.__hiln( height(self.Groupoid.Order, j) ,i)
        if (nom == ""):
            nom = "1"
        if pp:
            ml = max(len(nom),len(denom))
            mlnot = int( (ml - len(nom)) / 2 )
            mldot = int( (ml - len(denom)) / 2 )
            return ['\n', ' '*mlnot, nom, '\n', '-'*ml, '\n', ' '*mldot, denom, '\n']
        else:
            return [nom,'/',denom]

    def hilberttable(self, trunc=0):
        """ computes Hilbert series as a table of dimensions
        (works only in the finite dimensional case). """
        dim = [1]
        if (self.dimension() == 0) and (trunc == 0):
            return dim
        for i in self.Groupoid.PosRoots:
            j = self.Groupoid.braid_v1v2(i,i)
            p = self.__hilnq( height(self.Groupoid.Order, j), i , trunc )
            dim = multpol(dim,p, trunc)
        return dim

    def GKdim(self):
        """ calculates the Gelfand-Kirillov dimension of the Nichols algebra """
        if self.Groupoid.Order == 0:
            return len(self.Groupoid.PosRoots)
        gk = 0
        if self.Groupoid.NumberOfParameters == 1:
            for i in self.Groupoid.PosRoots:
                j = self.Groupoid.braid_v1v2(i,i) % self.Groupoid.Order
                if j == 0:
                    gk = gk + 1
        else:
            for i in self.Groupoid.PosRoots:
                j = self.Groupoid.braid_v1v2(i,i)
                if j[0] == 0:
                    gk = gk + 1
                else:
                    j[0] = 1
                for n in range(1, self.Groupoid.NumberOfParameters):
                    if j[n] != 0:
                        gk = gk + j[0]
                        break
        return gk
# vim:ts=4:sw=4:expandtab:
