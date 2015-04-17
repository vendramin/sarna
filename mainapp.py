import os
from GnuplotBiDir import Gnuplot
from groupoid import *
from nichols import *

class MainApp:
    def __init__(self, filename, opengnuplotwindow=True):
        self.Options = { 'OpenGnuplotWindow':opengnuplotwindow, 'ShowSimples':True, 'ShowArrows':False, 'PointSize':3 }
        self.__Temp_filename = '.tempfile.gp'
        self.FileName = filename
        if self.Options['OpenGnuplotWindow']:
            self.GnuplotWindow = Gnuplot()
            self.GnuplotWindow("set mouse")

        type, order, braid = self.__read(filename)
        # self.Groupoid = 0
        # self.Nichols = 0
        if type == 'diagonal':
            self.Groupoid = WeylGroupoid(braid, order)
            self.Nichols = NicholsAlgebra(self.Groupoid)

    def __del__(self):
        try:
            os.remove(self.__Temp_filename)
        except:
            pass

    def change_option(self, opt, value=None):
        if value == None:
            self.Options[opt] = not self.Options[opt]
        else:
            self.Options[opt] = value
        self.draw()
        print 'Debug information: %s is now %s'%(opt, self.Options[opt]);

    def draw(self):
        if (self.Groupoid.Rank in [2,3]) and (self.Options['OpenGnuplotWindow']):
            self.Groupoid.save4gnuplot(self.__Temp_filename, self.Description, self.Options['ShowSimples'], self.Options['ShowArrows'], self.Options['PointSize'])
            self.GnuplotWindow("clear\n")
            self.GnuplotWindow("set mouse;\n")
            self.GnuplotWindow("load \'"+self.__Temp_filename+"\';\n")

    def show(self):
        print "Rank: %d" % self.Groupoid.Rank;
        print "Order of z: %d" %self.Groupoid.Order;
        print "Description: %s" %self.Description;
        print "Braid";
        for i in xrange(self.Groupoid.Rank):
            for j in xrange(self.Groupoid.Rank):
                if self.Groupoid.NumberOfParameters == 1:
                    print "z^%d" % self.Groupoid.Braid[i][j],
                else:
                    print "z^%d" % self.Groupoid.Braid[i][j][0],
                    for k in range(1,self.Groupoid.NumberOfParameters):
                        print "q_%d^%d" % (k,self.Groupoid.Braid[i][j][k]),
                if j == self.Groupoid.Rank - 1:
                    print "\n",
                else:
                    print " ",
        
    def __make_ints(self, s, numofpars):
        for i in range(len(s)):
            try:
                s[i] = int(s[i])
            except ValueError:
                print "The string %s can not be part of the braiding." % s[i]
                sys.exit(1)
        for i in range(len(s),numofpars):
            s = s + [0]
        if numofpars == 1:
            return s[0]
        else:
            return s


    def __read(self, filename):
        try:
            file = open(filename, 'r');
        except:
            print 'File error: can\'t open file',filename;
            sys.exit(0);
        buffer = "";

        self.Description = ""
        rank = 0
        type = ""
        order = 0
        braid = []

        self.FileData = ""
        
        for line in file.readlines():
            self.FileData = self.FileData + line
            for i in range(0, len(line)):
                if (line[i] == '#'):
                    buffer = buffer + '\n'
                    break;
                if (line[i] != ' ') or (line.find('description=') != -1):
                    buffer = buffer + line[i];

        newbuffer = buffer.split('\n');
        for line in newbuffer:
            if line.find("description=") != -1:
                tmp = line.split('description=')
                tmp = tmp[1].split('"');
                self.Description = tmp[1];

            if line.find("type=") != -1:
                tmp = line.split('type=')
                type = tmp[1]

            if (line.find('rank=') != -1):
                tmp = line.split('rank=');
                rank = int(tmp[1]);
                braid = [];
                braid = [[0 for i in range(rank)] for j in range(rank)]
            if (line.find('order=') != -1):
                tmp = line.split('order=');
                try:
                    order = int(tmp[1]);
                    if order<0:
                        print 'Order of z has to be a nonnegative integer!'
                        sys.exit(1)
                except ValueError:
                    print 'Order of z has to be a nonnegative integer!'
                    sys.exit(1)

            #if (line.find('arrows') != -1) and (line.find('noarrows') == -1):
            #    self.DrawArrows = True
            #if (line.find('nosimpleroots') != -1):
            #    self.DrawSimples = False

        # read the matrix
        if 'braid' in newbuffer:
            numofpars = -1
            position = newbuffer.index('braid');
            for i in range(0, rank):
                tmp = newbuffer[position+i+1].split(';');
                for j in range(0,rank):
                    tmpentry = tmp[j].split(',')
                    if numofpars == -1:
                        numofpars = len(tmpentry)
                    braid[i][j] = self.__make_ints(tmpentry, numofpars);
        return type, order, braid

# vim:ts=4:sw=4:expandtab:
