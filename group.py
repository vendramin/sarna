from methods import *

class FiniteGroup:
    def __init__(self, elts, Ct):
        """
        Initializes an abstract finite group by giving the set of its elements as a list and the Cayley table for the group operation as a double array.
        The neutral element has to be the first element of the list.
        """
        self.Elements = elts
        self.Cayleytable = Ct

    def mul(self,a,b):
        """
        Computes the product of two elements of the group.
        """
        return self.Cayleytable[self.Elements.index(a)][self.Elements.index(b)]

    def inv(self,a):
        """
        Computes the inverse of an element of the group.
        """
        b=a
        c=a
        while b != self.Elements[0]:
            c=b
            b=self.mul(a,b)
        return c

    def grouporder(self):
        """
        Determines the order of the group (number of its elements).
        """
        return len(self.Elements)

    def eltorder(self,a):
        """
        Determines the order of the element a.
        """
        b = self.mul(a,a)
        eo = 0
        while b != a:
            b = self.mul(a,b)
            eo += 1
        return eo

    def maxeltorder(self):
        """
        Computes the maximal element order in the group.
        """
        meo = 0
        for i in self.Elements:
            eo = self.eltorder(i)
            if eo > meo:
                meo = eo
        return meo

    def iscyclic(self):
        """
        Checks whether the group is cyclic.
        """
        if self.maxeltorder() == self.grouporder():
            return True
        else:
            return False

    def isabelian(self):
        """
        Checks whether the group is abelian.
        """
        for a in self.Elements:
            for b in self.Elements:
                c1 = self.mul(a,b)
                c2 = self.mul(b,a)
                if c1 !=c2:
                    return False
        return True

# vim:ts=4:sw=4:expandtab:
