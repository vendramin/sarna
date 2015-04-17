#def sum(self, v):
#    s = 0
#    for i in range(len(v)):
#        s += v[i]
#    return s

def multpol(p,q, trunc=0):
    lp,lq = len(p),len(q)
    if (len(p) > len(q)):
        for i in range(len(q)+1, len(p)+1):
            q += [0]
    else:
        for i in range(len(p)+1, len(q)+1):
            p += [0]
    for i in range(len(p)+1, 2*len(p)+1):
        p += [0]
        q += [0]
    ret = [ sum([p[i]*q[n-i] for i in range(n+1)]) for n in range(len(p)) ]
    if trunc>0:
        return ret[:trunc+1]
    else:
        return ret[:lp+lq-1]

def normalize(numofpars, numb, order):
    """
    Returns normalized form of numb.
    numb = [a_0,a_1,...,a_n] means  z^a_0 * q_1^a_1 * ... * q_n^a_n
    (n = numofpars, order = order(z); all parameters q_1,...,q_n are algebraically independent)
    """
    if numofpars == 1:
        if order !=0:
            numb = numb % order
    else:
        if order !=0:
            numb[0] = numb[0] % order
    return numb

def notone(numofpars, numb, order):
    """
    Returns True if numb != 1.
    numb = [a_0,a_1,...,a_n] means  z^a_0 * q_1^a_1 * ... * q_n^a_n
    (n = numofpars, order = order(z))
    """
    if numofpars == 1:
        if order == 0:
            return (numb != 0)
        else:
            return ((numb % order) != 0)
    if order != 0:
        if (numb[0] % order) != 0:
            return True
    else:
        if numb[0] != 0:
            return True
    for i in range(1, numofpars):
        if numb[i] != 0:
            return True
    return False

def add(numofpars, s1, s2, s3=None):
    """
    Returns s1 + s2 + s3 (or s1 + s2 if there's no s3)
    """
    if s3 == None:
        if numofpars == 1:
            return s1 + s2
        else:
            return [ s1[i]+s2[i] for i in range(numofpars) ]
    else:
        if numofpars == 1:
            return s1 + s2 + s3
        else:
            return [ s1[i]+s2[i]+s3[i] for i in range(numofpars) ]
        
def mult(numofpars, s, m):
    """Returns s*m"""
    if numofpars == 1:
        return s * m
    else:
        return [ s[i] * m for i in range(numofpars) ]

def gcd(a,b):
    """Return greatest common divisor using Euclid's Algorithm"""
    a = abs(a)
    b = abs(b)
    if (a == 0) or (b == 0):
        return a+b
    while b:
        a, b = b, a % b
    return a

def height(order, j):
    """Returns the height of 'number' j"""
    if order == 0:
        # TODO: change this for char k > 0 and j = 0
        return 0
    try:
        j0 = j[0]
        if sum([abs(i) for i in j[1:]]) > 0:
            return 0
    except TypeError:
        j0 = j
    if (j0 == 0):
        # TODO: change this for char k > 0 and j = 0
        return 0
    return order/gcd(order,j0)

def triang(numofpars,matr,order):
    """Computes for any quadratic matrix <mathr> of multinumbers the upper triangular matrix <tmatr>
       such that tmatr_{ij}=0 for i>j and tmatr_{ij}=matr_{ij}+matr_{ji} for i<=j.
    """
    tmatr=matr
    for i in range(len(matr)):
        for j in range(i):
            if numofpars == 1:
                tmatr[i][j] = 0
            else:    
                tmatr[i][j] = [0 for k in range(numofpars)]
        for j in range(i+1,len(matr)):
            tmatr[i][j] = normalize(numofpars,add(numofpars, tmatr[i][j], matr[j][i]),order)
    return tmatr

def det3(m):
    """Calculates the determinant of a 3x3-matrix m."""
    return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[1][0]*(m[0][1]*m[2][2]-m[0][2]*m[2][1])+m[2][0]*(m[0][1]*m[1][2]-m[0][2]*m[1][1])

# vim:ts=4:sw=4:expandtab:
