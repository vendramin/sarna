#!/usr/bin/env python
# -*- coding: latin-1 -*-
import sys
from mainapp import *

class OptionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
    
def getoptions(str,num,num2=None):
    """
    Checks whether <str> is a list of <num>
    (or <num>, <num>+1, ..., <num2>) elements separated by ','.
    If so, it returns an array of the elements of the list,
    with leading and trailing white spaces deleted.
    Otherwise OptionError is raised.
    """
    if num2==None:
        num2=num
    op=str.split(',')
    if len(op) >= num and len(op) <= num2:
        for i in range(len(op)):
            op[i]=op[i].strip()
        return op
    else:
        raise OptionError, "WrongNumber"
     
def getintoptions(str,num,num2=None):
    """
    Checks whether <str> is a list of <num>
    (or <num>, <num>+1, ..., <num2>) integers separated by ','.
    If so, it returns an array of the elements of the list,
    with leading and trailing white spaces deleted.
    Otherwise error is raised.
    """
    if num2==None:
        num2=num
    op=str.split(',')
    if len(op) <= num2 and len(op) >= num:
        try:
            for i in range(len(op)):
                op[i]=int(op[i])
            return op
        except ValueError:
            raise Option.Error, "WrongType"
    else:
        raise OptionError, "WrongNumber"

def quit():
    pass

def help():
    print """
Use: console.py <filename> [options]
Options:
    -i  Interactive mode 
    -b  [num] Use basis # num for simple roots.
        If num is not present, show all bases and quit.
        This option is overridden by -i.
    -d  Draw root systems in gnuplot windows (only when rank < 4).
    -sa Draw arrows (only valid for gnuplot)
    -ss Do not draw simple roots (only valid for gnuplot)
    -o <filename> Save gnuplot file (only when rank < 4).
    -h  Print this help.
"""
    #-w  Open different gnuplot windows.

if __name__ == "__main__":
    onlyshowbases = False
    interactivemode = False
    prettyprint = False
    truncate = 0
    css = False
    csa = False
    
    if '-b' in sys.argv:
        pos = sys.argv.index('-b')
        if pos < len(sys.argv)-1:
            try:
                option = int(sys.argv[pos+1])
                sys.argv = sys.argv[:pos] + sys.argv[pos+2:]
            except ValueError:
                onlyshowbases = True
                sys.argv.remove('-b')
        else:
            onlyshowbases = True
            sys.argv.remove('-b')
    
    if '-o' in sys.argv:
        pos = sys.argv.index('-o')
        if pos < len(sys.argv)-1 and sys.argv[pos+1][0] != '-':
            writegnuplotfile = True
            gnuplot_file = sys.argv[pos+1]
            sys.argv = sys.argv[:pos] + sys.argv[pos+2:]
            print 'Output gnuplot file will be: %s' % gnuplot_file;
        else:
            print 'Missing destination file operand after -o';
            sys.exit(0)

    if '-ss' in sys.argv:
        css = True
        sys.argv.remove('-s')

    if '-sa' in sys.argv:
        csa = True
        sys.argv.remove('-a')

    if '-i' in sys.argv:
        interactivemode = True
        sys.argv.remove('-i')
        onlyshowbases = False

    if '-d' in sys.argv:
        drawinwindow = True
        sys.argv.remove('-d')

    if (len(sys.argv) == 1) or ('-h' in sys.argv):
        help()
        sys.exit(0)

    filename = sys.argv[1]
    app = MainApp(filename)
    if css:
        app.change_option('ShowSimples')
    if csa:
        app.change_option('ShowArrows')

    done = False
    askagain = False

    if onlyshowbases:
        app.Groupoid.print_bases()
        done = True

    while not done:

        if interactivemode:
            print "There are %d bases (0 = Canonical = Standard)." % len(app.Groupoid.Bases);
            option = raw_input('Please make your choice (h for help, q to quit): ')
            if option == 'h':
                print """
                Math:
                -----
                <enter>   to print and draw roots
                <num>     to choose the <num>-th basis as your working basis,
                ap <num>,<num> to calculate all paths in the Weyl groupoid between two bases,
                b         to show bases,
                br  <num> to show the braiding corresponding to the basis <num>
                tbr <num> to show the triangulated braiding corresponding to the basis <num>
                cox     to calculate the Coxeter matrix C=(c_ij) associated to the current basis,
                        where c_ij with i=/=j is the number of those positive roots
                        which are linear combinations of the ith and jth basis vector.
                dim     to calculate the dimension of the Nichols algebra,
                rq      to print the coefficients  q_ff, for f in the set of positive roots
                eb <path> to calculate the end basis corresponding to the path <path>,
                        where the starting basis is the current basis
                ig      to calculate the isotropy group of the Dynkin diagram of the standard basis
                ig_ab   to check whether the isotropy group is abelian
                ig_cyc  to check whether the isotropy group is cyclic
                lw      to show longest word in the Weyl groupoid (lw = p 0,-1)
                p <num>,<num> to calculate path in the Weyl groupoid between two bases,
                pl <num>,<num> to calculate the length of the shortest path in the Weyl groupoid between two bases,
                r <num> to reflect on the <num>-th basis vector of the current basis
                t <num> to truncate dimension vectors and sets of paths up to num

                Other:
                ------
                d    to toggle whether to draw,
                sa   to toggle ShowArrows,
                ss   to toggle ShowSimples,
                sp   to toggle PrettyPrint,
                h    to show this help,
                i    to show all information,
                G    gnuplot commmand,
                q    to quit
                """
                askagain = True
            elif option == '':
                askagain = False
            elif option == 'dim':
                i  = app.Nichols.dimension()
                if (i > 0) or (truncate > 0):
                    dt = app.Nichols.hilberttable(truncate)
                else:
                    dt = []
                hs = app.Nichols.hilbertseries(prettyprint)
                gk = app.Nichols.GKdim()
                if i == 0:
                    i = 'infinite'
                else:
                    i = str(i)
                print 'Dimension of the Nichols algebra: %s' % i
                print 'Hilbert series:'
                for line in hs:
                    print line,
                print
                print 'Gelfand-Kirillov dimension of the Nichols algebra: %s' % gk
                if (len(dt) > 0):
                    print 'Dimensions: '
                    if prettyprint:
                        ml = int( len(dt) / 2 )
                        print 'deg      dim      deg      dim\n============      ============'
                        for j in xrange(ml):
                            print '%3d %8d      %3d %8d' % (j, dt[j], j+ml, dt[j+ml])
                        if (len(dt)%2 == 1):
                            print ' '*18 + '%3d %8d' % (len(dt)-1, dt[-1])
                    else:
                        print dt
                    print 'Top degree: ', len(dt)-1
                askagain = True
            elif option == 'rq':
                rtsqs = app.Nichols.roots_coefs()
                print '%16s %10s %5s' % ('root','q_ff','order') + '\n' + '='*33
                for i in rtsqs:
                    print '%16s %10s %5d' % (i[0],i[1],i[2])
                askagain = True
            elif option == 'lw':
                w = app.Groupoid.find_path(0,-1)
                print "Longest word: " + app.Groupoid.print_path(w) + ". Length:", app.Groupoid.pathlength(0,-1)
                askagain = True
            elif option == 'ig':
                if len(app.Groupoid.Isogroup.Elements) == 0:
                    app.Groupoid.calculate_isogroup()
                print(app.Groupoid.Isogroup.Elements)
                print(app.Groupoid.Isogroup.Cayleytable)
                askagain = True
            elif option == 'ig_ab':
                if len(app.Groupoid.Isogroup.Elements) == 0:
                    app.Groupoid.calculate_isogroup()
                if app.Groupoid.Isogroup.isabelian():
                    print "The isotropy group is abelian."
                else:
                    print "The isotropy group is not abelian."
                askagain = True
            elif option == 'ig_cyc':
                if len(app.Groupoid.Isogroup.Elements) == 0:
                    app.Groupoid.calculate_isogroup()
                if app.Groupoid.Isogroup.iscyclic():
                    print "The isotropy group is cyclic."
                else:
                    print "The isotropy group is not cyclic."
                askagain = True
            elif option == 'cox':
                cm = [[0 for i in range(app.Groupoid.Rank)] for j in range(app.Groupoid.Rank)]
                wi = 1
                for i in range(app.Groupoid.Rank):
                    cm[i][i]='2'
                    for j in range(i+1,app.Groupoid.Rank):
                        cm[i][j]=str(app.Groupoid.cox_ij(app.Groupoid.CurrentBasis,i,j))
                        cm[j][i]=cm[i][j]
                        if len(cm[i][j])>wi:
                            wi = len(cm[i][j])
                print "Coxeter matrix:"        
                for i in range(app.Groupoid.Rank):
                    for j in range(app.Groupoid.Rank):
                        print cm[i][j].rjust(wi),
                    print
                askagain = True
            elif option.startswith('pl '):
                try:
                    op = getintoptions(option[3:],2)
                    pl = app.Groupoid.pathlength(op[0],op[1])
                    print "Pathlength: ", pl
                except OptionError:
                    print "Option pl requires two numbers and a , between them."
                askagain = True
            elif option.startswith('p '):
                try:
                    op = getintoptions(option[2:],2)
                    w = app.Groupoid.find_path(op[0],op[1])
                    print "Path: " + app.Groupoid.print_path(w) + ". Length:", len(w)
                except OptionError:
                    print "Option p requires two numbers and a , between them."
                askagain = True
            elif option.startswith('eb '):
                try:
                    option = getoptions(option[3:],1)[0]
                    option = option.strip()
                    if app.Groupoid.Rank<10:
                        option = option.replace('',' ')
                    option = option.split()
                    try:
                        for i in range(len(option)):
                            option[i]=int(option[i])-1
                        pth = app.Groupoid.endbasis(app.Groupoid.CurrentBasis,option)
                        print "End basis of path " + app.Groupoid.print_path(option) + ":", pth 
                    except ValueError:
                        print "Option eb requires a sequence of integers between 1 and", str(app.Groupoid.Rank)
                except OptionError:
                    print "Option eb requires a sequence of integers between 1 and", str(app.Groupoid.Rank)
                askagain = True
            elif option.startswith('ap '):
                try:
                    option = getintoptions(option[3:],1)[0]
                    pc,tr = app.Groupoid.allpaths(app.Groupoid.CurrentBasis,option,truncate)
                    if tr:
                        print len(pc), "paths (truncated):"
                    else:
                        print len(pc), "paths:"
                    pc0=pc.pop(len(pc)-1)
                    for p in pc:
                        print app.Groupoid.print_path(p)+",",
                    print app.Groupoid.print_path(pc0)
                except OptionError:
                    print "Option ap requires an integer between 0 and", (len(app.Groupoid.Bases)-1)
                askagain = True
            elif option.startswith('tbr'):
                try:
                    option = int(option[4:]) % len(app.Groupoid.Bases)
                    thebraid = triang(app.Groupoid.NumberOfParameters,app.Groupoid.braid_for_basis(app.Groupoid.Bases[option]), app.Groupoid.Order)
                    for i in range(app.Groupoid.Rank):
                        print thebraid[i]
                except ValueError:
                    print "Option tbr requires an integer value between 0 and %d." %(len(app.Groupoid.Bases)-1);
                askagain = True
            elif option.startswith('t '):
                try:
                    truncate = int(option[2:])
                    if truncate > 0:
                        print "We now truncate dimension table up to degree", truncate
                        print "and the set of paths between two bases."
                        print "Enter 't 0' to go back to normal mode."
                    else:
                        print "We do not truncate dimension tables and sets of paths now."
                except ValueError:
                    print "Option t requires an integer"
                askagain = True
            elif option == 'd':
                app.change_option('OpenGnuplotWindow')
                print "OpenGnuplotWindow =", app.Options['OpenGnuplotWindow']
                askagain = True
            elif option == 'sa':
                app.change_option('ShowArrows')
                print "ShowArrows =", app.Options['ShowArrows']
                askagain = False
            elif option == 'ss':
                app.change_option('ShowSimples')
                print "ShowSimples =", app.Options['ShowSimples']
                askagain = False
            elif option == 'sp':
                prettyprint = not prettyprint
                askagain = True
            elif option == 'q':
                askagain = True
                done = True
            elif option == 'G':
                if app.Options['OpenGnuplotWindow']:
                    command = raw_input('GnuPlot command: ')
                    app.GnuplotWindow(command + '\n')
                askagain = True
            #elif option == 'g':
            #    writegnuplotfile = not writegnuplotfile;
            #    if writegnuplotfile:
            #        print 'SaveGnuplotFile=',WriteGnuplotFile;
            #        gnuplot_file = raw_input('Enter the new gnuplot file: ')
            #        if gnuplot_file == '':
            #            print 'No gnuplot file will be saved';
            #            writegnuplotfile = False
            #    else:
            #        print 'Now savegnuplotfile is:', writegnuplotfile;
            #    askagain = True
            elif option == 'i':
                app.show()
                askagain = True
            elif option == 'b':
                app.Groupoid.print_bases()
                askagain = True
            elif option[0] == 'b' and option[1] == 'r':
                try:
                    option = int(option[2:]) % len(app.Groupoid.Bases)
                    thebraid = app.Groupoid.braid_for_basis(app.Groupoid.Bases[option])
                    for i in range(app.Groupoid.Rank):
                        print thebraid[i]
                except ValueError:
                    print "Option br requires an integer value between 0 and %d." %(len(app.Groupoid.Bases)-1);
                askagain = True
            elif option[0] == 'r':
                option = option[1:].strip()
                try:
                    for j in xrange(len(option)):
                        k = int(option[j]) - 1
                        app.Groupoid.apply_reflection(k)
                    print "New basis: ", app.Groupoid.CurrentBasis
                    askagain = False
                except ValueError:
                    print "Option 'r' requires an integer values between 1 and %d." % app.Groupoid.Rank;
                    askagain = True
            else:
                try:
                    app.Groupoid.change_basis(int(option))
                    askagain = False
                except ValueError:
                    print "%s is not a valid option." % option;
                    askagain = True
        else:
            done = True

        if not askagain:
            app.Groupoid.print_roots()
            app.draw()
            # ugliest code in universe
            if done and app.Options['OpenGnuplotWindow']:
                raw_input("Press enter to finish")
    quit()

# vim:ts=4:sw=4:expandtab:
