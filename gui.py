#!/usr/bin/python
# -*- coding: latin-1 -*-

import tkSimpleDialog
import tkMessageBox
import sys

from SimpleDialog import *

from string import *
from mainapp import *
from Tkinter import *
from tkFileDialog import *

from os import getcwd

class GUIApp:
    """
    Class for the Tkinter application 
    """
    def __init__(self, filename):
        self.Filename = filename

        self.__root = Tk()
        self.__root.title('Arithmetic Root Systems')
        
        if self.Filename == None:
            try:
                self.Filename = askopenfilename(title="Open", initialdir=getcwd(),\
                    filetypes=[("ARS files","*.ars"), ("All files","*.*")], parent=self.__root)
            except:
                sys.exit

        # Create the application
        self.__app = MainApp(self.Filename, True)
        
        # Create the main frame
        self.__frame = Frame(self.__root, width=600, height=400, bd=1)
        self.__frame.pack()

        # Create the menu bar
        self.__create_menubar()

        # Create the roots dialog
        self.__create_rootsframe()

        # Create the information dialogs
        self.__create_finfoframe()

        # Open gnuplot window
        self.__app.draw()

        self.__root.mainloop() 

    def __create_rootsframe(self):
        """ Show roots for the current basis """
        
        #tmp = 'Current basis is %s\n'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis]
        #tmp = tmp + 'Positive Roots:\n'
        #for v in self.__app.Groupoid.PosRoots:
        #    tmp = tmp + '%s\n'%v
        #tmp = tmp + '\nNegative Roots:\n'
        #for v in self.__app.Groupoid.NegRoots:
        #    tmp = tmp + '%s\n'%v
        
        self.__rframe = Frame(self.__frame, bd=2, relief=SUNKEN)
        text=Text(self.__rframe, height=10, width =65)
        text.insert(END, self.__roots())
        text.pack(side=LEFT, fill=X, padx=5)
        sb = Scrollbar(self.__rframe, orient=VERTICAL, command=text.yview)
        sb.pack(side=RIGHT, fill=Y)
        text.configure(yscrollcommand=sb.set,state=DISABLED)
        self.__rframe.pack(expand=1, fill=X, pady=10, padx=5)

    def __create_finfoframe(self):
        """ Show all the information of the braid file """ 

        # Show the ARS file 
        self.__fframe = Frame(self.__frame, bd=2, relief=SUNKEN)
        text=Text(self.__fframe, height=10, width =65)
        text.state = DISABLED
        text.insert(END, self.__app.FileData)
        text.pack(side=LEFT, fill=X, padx=5)
        sb = Scrollbar(self.__fframe, orient=VERTICAL, command=text.yview)
        sb.pack(side=RIGHT, fill=Y)
        text.configure(yscrollcommand=sb.set,state=DISABLED)
        self.__fframe.pack(expand=1, fill=X, pady=10, padx=5)

        # All information retrieved from file
        self.__iframe = Frame(self.__frame, bd=2, relief=FLAT)
        Message(self.__iframe, text='Rank: %d - File: %s'%(self.__app.Groupoid.Rank, self.Filename),\
                width=400,relief=SUNKEN).pack(fill=X, padx=5)
        self.__iframe.pack(expand=1, fill=X, pady=10, padx=5)

    def __create_menubar(self):
        """ Create the main pulldown menu """

        self.__mbar = Frame(self.__frame, relief = 'raised', bd=1)
        self.__mbar.pack(fill = X)

        # Create "File" menu
        self.__filebutton = Menubutton(self.__mbar, text = 'File', underline=0)
        self.__filebutton.pack(side = LEFT)
        self.__filemenu = Menu(self.__filebutton, tearoff=0)
        self.__filebutton['menu'] = self.__filemenu
        self.__filemenu.add('command', label = 'New', underline=0, command = main)
        self.__filemenu.add('command', label = 'Open...', underline=0, command = self.f_open)
        #self.__filemenu.add('command', label = 'Save Gnuplot', underline=0, command = self.gp_save)
        self.__filemenu.add('separator')
        self.__filemenu.add('command', label = 'Quit', underline=0, command = sys.exit)

        # Create "Gnuplot" menu
        # TODO: disable the first two options if there is no Gnuplot window
        # TODO: I don't want the dictionary for gnuplot options, only boolean variables 
        
        # FIXME: for default options...
        self.__gnuplotbutton = Menubutton(self.__mbar, text = 'Gnuplot', underline=0)
        self.__gnuplotbutton.pack(side = LEFT)
        self.__gnuplotmenu = Menu(self.__gnuplotbutton, tearoff=1)
        self.__gnuplotbutton['menu'] = self.__gnuplotmenu
        self.__gnuplotmenu.add_checkbutton(label='Show simple roots', underline=5, command=self.__gp_change_ssr)
        self.__gnuplotmenu.add_checkbutton(label='Show arrows', underline=5, command=self.__gp_change_sa)
        self.__gnuplotmenu.add_checkbutton(label='Open Gnuplot window', underline=0, command=self.__gp_change_gpw)
        self.__gnuplotmenu.add('separator')
        self.__gnuplotmenu.add('command', label='Redraw', underline=0, command=self.__app.draw)
        self.__gnuplotmenu.add('command', label='Save Gnuplot file', underline=5, command=self.gp_save)
        self.__gnuplotmenu.add('command', label='Enter Gnuplot command', underline=0, command=self.gp_command)

        if self.__app.Options['ShowSimples']:
            self.__app.change_option('ShowSimples')
            self.__gnuplotmenu.invoke(1)
        
        if self.__app.Options['ShowArrows']:
            self.__app.change_option('ShowArrows')
            self.__gnuplotmenu.invoke(2)
        
        if self.__app.Options['OpenGnuplotWindow']:
            self.__app.change_option('OpenGnuplotWindow')
            self.__gnuplotmenu.invoke(3)

        # Gnuplot menu only for rank 2,3
        if self.__app.Groupoid.Rank not in [2,3]:
            self.__gnuplotbutton["state"] = DISABLED
        
        # Create "ARS" menu
        self.__arsbutton = Menubutton(self.__mbar, text = 'ARS', underline=0)
        self.__arsbutton.pack(side = LEFT)
        self.__arsmenu = Menu(self.__arsbutton, tearoff=1)
        self.__arsbutton['menu'] = self.__arsmenu
        self.__arsmenu.add('command', label='Change current basis', underline=10, command = self.ars_changebasis)
        self.__arsmenu.add('command', label='Show roots', underline=5, command = self.ars_showroots)
        self.__arsmenu.add('command', label='Show Dynkin diagram', underline=5, command = self.ars_dynkin)
        self.__arsmenu.add('separator') 
        for i in range(self.__app.Groupoid.Rank):
            self.__arsmenu.add('command', label='Reflect to simple root %d'%(i+1), underline=23,\
                command = lambda i=i: self.ars_reflection(i))

        # Create "Nichols Algebra" menu
        self.__nicholsbutton = Menubutton(self.__mbar, text = 'Nichols Algebra', underline=0)
        self.__nicholsbutton.pack(side = LEFT)
        self.__nicholsmenu = Menu(self.__nicholsbutton, tearoff=1)
        self.__nicholsbutton['menu'] = self.__nicholsmenu
        self.__nicholsmenu.add('command', label='Dimension', underline=0, command = self.n_dim)
        self.__nicholsmenu.add('command', label='Dimensions table', underline=8, command = self.n_table)
        self.__nicholsmenu.add('command', label='GK Dimension', underline=0, command = self.n_GKdim)
        self.__nicholsmenu.add('command', label='Hilbert series', underline=0, command = self.n_hilbert)
        
        # Create help menu
        self.__helpbutton = Menubutton(self.__mbar, text = 'Help', underline=0 )
        self.__helpbutton.pack(side = RIGHT)
        self.__helpmenu = Menu(self.__helpbutton, tearoff=0)
        self.__helpbutton['menu'] = self.__helpmenu
        self.__helpmenu.add('command', label = 'License', underline=0, command = self.license)
        self.__helpmenu.add('command', label = 'About', underline=0, command = self.help)
   
    def f_open(self):
        """ Open file """
        # TODO
        pass

    def gp_save(self):
        """ Save the gnuplot file (only valid for rank 2,3) """

        if self.__app.Groupoid.Rank in [2,3]:
            tmp = tkSimpleDialog.askstring('Save Gnuplot file', 'Enter a valid gnuplot filename')
            if tmp != None:
               self.__app.Groupoid.save4gnuplot(tmp, self.__app.Description, \
                        self.__app.Options['ShowSimples'], \
                        self.__app.Options['ShowArrows'], \
                        self.__app.Options['PointSize'])
               print 'Debug information: [%s] gnuplot file saved!'%tmp;

    def __gp_change_sa(self):
        """ To toggle ShowArrows (show arrows) """
        self.__app.change_option('ShowArrows')
        self.__app.draw()

    def __gp_change_ssr(self):
        """ To toggle ShowSimples (show simple roots) """
        self.__app.change_option('ShowSimples')
        self.__app.draw()

    def __gp_change_gpw(self):
        """ To toggle OpenGnuplotWindow (open a gnuplot window?) """
        self.__app.change_option('OpenGnuplotWindow')
        if not self.__app.Options['OpenGnuplotWindow']:
            self.__app.GnuplotWindow('quit')
            self.__app.GnuplotWindow = Gnuplot()
        else:
            self.__app.draw()

    def n_dim(self):
        """ Show the dimension of the Nichols Algebra """
        
        i = self.__app.Nichols.dimension()
        if i == 0:
            i = 'infinite'
        else:
            i = str(i)
        tkMessageBox.showinfo('Nichols algebra','The dimension of the Nichols Algebra is %s'%i)
    
    def n_table(self):
        """ Show table with dimensions """

        i  = self.__app.Nichols.dimension()
        if i > 0:
            dt = self.__app.Nichols.hilberttable()
        else:
            dt = []
            hs = self.__app.Nichols.hilbertseries(True)
        if (len(dt) > 0):
            table = '' #'Dimensions:\n===========\n'
            ml = int( len(dt) / 2 )
            #table = table + 'deg      dim\n===      ===\n'
            #ml = int( len(dt) / 2 )
            table = table + 'deg        dim     deg        dim\n==============     ==============\n'
            for j in xrange(ml):
                table = table + '%3d %10d     %3d %10d\n' % (j, dt[j], j+ml, dt[j+ml])
            if (len(dt)%2 == 1):
                table = table + ' '*19 + '%3d %10d\n' % (len(dt)-1, dt[-1])
            #for j in xrange(len(dt)):
            #    table = table + '%3d %8d\n'%(j, dt[j])
            table = table + 'Top degree: ' + str(len(dt)-1)

        top = Toplevel() 
        top.title('Dimension table')

        frame = Frame(top, bd=2, relief=SUNKEN)
        frame.label = Label(frame, relief=FLAT, anchor=NW, borderwidth=0)
        frame.label.pack(fill=X)
        
        text=Text(frame, height=10, width=40)
        text.insert(END, table)
        text.pack(side=LEFT, fill=X, padx=5)
        sb = Scrollbar(frame, orient=VERTICAL, command=text.yview)
        sb.pack(side=RIGHT, fill=Y)
        text.configure(yscrollcommand=sb.set,state=DISABLED)
        frame.pack(expand=1, fill=X, pady=10, padx=5)

        #text.update()

    def n_GKdim(self):
        """ Show the GK-dimension of the Nichols Algebra """

        i = self.__app.Nichols.GKdim()
        tkMessageBox.showinfo('Nichols algebra','The GK-dimension of the Nichols Algebra is %s'%i)

    def n_hilbert(self):
        """ Show the Hilbert series """
        hs = self.__app.Nichols.hilbertseries(True)
        top = Toplevel()
        top.title('Hilbert Series')
        text = Text(top, height=6, width=max([len(i) for i in hs]))
        for line in hs:
            text.insert(END, line)
        text.pack(fill=X)
        text.configure(state=DISABLED)
        text.update()

    def ars_reflection(self, i):
        """ 
        Changes the variable CurrentBasis according to the reflection
        on the i-th basis element of the current basis
        """
        self.__app.Groupoid.apply_reflection(i)
        self.__app.draw()

    def ars_showroots(self):
        """ Ask for a basis and then show all the roots """

        #tmp = 'Current basis: %s\n==============\n'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis]
        #tmp = tmp + 'Positive Roots:\n==============\n'
        #for v in self.__app.Groupoid.PosRoots:
        #    tmp = tmp + '%s\n'%v
        #tmp = tmp + '\nNegative Roots:\n===============\n'
        #for v in self.__app.Groupoid.NegRoots:
        #    tmp = tmp + '%s\n'%v
        
        top = Toplevel()
        top.title('Roots')
        
        frame = Frame(top, bd=2, relief=SUNKEN)
        frame.label = Label(frame, relief=FLAT, anchor=NW, borderwidth=0,\
                text='The current basis is %s'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis])
        frame.label.pack(fill=X)
        
        text=Text(frame, height=10, width =65)
        text.insert(END, self.__roots())
        text.pack(side=LEFT, fill=X, padx=5)
        sb = Scrollbar(frame, orient=VERTICAL, command=text.yview)
        sb.pack(side=RIGHT, fill=Y)
        text.configure(yscrollcommand=sb.set,state=DISABLED)
        frame.pack(expand=1)

    def gp_command(self):
        """ enter a Gnuplot command """

        notvalid = ['quit', 'reset']
        if self.__app.Groupoid.Rank in [2,3] and self.__app.Options['OpenGnuplotWindow']:
            tmp = tkSimpleDialog.askstring('Enter a Gnuplot command', 'Enter a valid gnuplot command')
            if tmp != None:
                if tmp not in notvalid:
                    self.__app.GnuplotWindow(tmp)
                else:
                    tkMessageBox.showerror('Error', '\'%s\' is not a valid Gnuplot command'%tmp)

    def ars_changebasis(self):
        """ Open a dialog box with all the bases of the Weyl Groupoid """
        
        top = Toplevel()
        top.title('Change current basis')
        
        top.vscroll = Scrollbar(top, orient=VERTICAL)
        top.list = Listbox(top, relief=SUNKEN, yscroll=top.vscroll.set)
        
        # Make the list with all of the bases 
        for i in xrange(len(self.__app.Groupoid.Bases)):
            top.list.insert(END, str(i) + '  ' + str(self.__app.Groupoid.Bases[i]))

        top.vscroll['command'] = top.list.yview
        top.vscroll.pack(side=RIGHT, fill=Y)
        top.list.pack(expand=1, fill=BOTH)
        top.list.bind('<Motion>', self.__cb_do_motion)
        top.list.bind('<Leave>', self.__cb_do_leave)
        top.list.bind('<1>', self.__cb_do_1)

    def __cb_do_motion(self, e):
        e.widget.select_clear(0, END)
        e.widget.select_set(e.widget.nearest(e.y))

    def __cb_do_leave(self, e):
        e.widget.select_clear(0, END)

    def __cb_do_1(self, e):
        """ When a basis is selected we have to recalculate all the roots """
        self.__app.Groupoid.change_basis(int(split(e.widget.get(e.widget.nearest(e.y)))[0]));
        self.__app.draw()

        print 'Debug information: now the current basis is %s'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis];

    def ars_dynkin(self):
        """ 
        Show the dynkin diagram associated to the current basis.
        This function must be rewritten!
        """

        # TODO: everything :-P
        if self.__app.Groupoid.Rank not in [2,3]:
            return 

        top = Toplevel()
        top.title('Generalized Dynkin diagram')
        nq = self.__app.Groupoid.braid_for_basis(self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis])
        
        canvas = Canvas(top, background = "white", height = 80*5, width = 80*5)
        canvas.pack()
        
        widget_point = [0,0,0]
        widget_line = [0,0,0]
        p = [[15,50],[60,50],[40,20]]
        for i in xrange(self.__app.Groupoid.Rank):
            widget_point[i] = canvas.create_oval(-1,-1,1,1)
            canvas.create_text(p[i][0]*5, p[i][1]*5-20, text=str(nq[i][i]))
            canvas.coords(widget_point[i],p[i][0]*5-10,p[i][1]*5-10,p[i][0]*5+10,p[i][1]*5+10)

        # Some text...
        canvas.create_text(150, 50, text='Generalized dynkin diagram\nThe basis is %s'\
                %self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis])

        for i in xrange(self.__app.Groupoid.Rank):
            for j in xrange(i+1, self.__app.Groupoid.Rank):
                if notone(self.__app.Groupoid.NumberOfParameters, \
                        add(self.__app.Groupoid.NumberOfParameters,nq[i][j],nq[j][i]), \
                        self.__app.Groupoid.Order):
                    widget_line[i] = canvas.create_line(p[i][0], p[i][1], p[j][0], p[j][1])
                    canvas.create_text( 5 * (p[i][0] + p[j][0]) / 2, 5 * (p[i][1] + p[j][1]) / 2, text=str(nq[i][j]))
                    canvas.coords(widget_line[i], p[i][0] * 5, p[i][1] * 5, p[j][0]*5, p[j][1]*5)

    def __roots(self):
        """ Returns a string with all the roots """

        tmp = 'Current basis: %s\n==============\n'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis]
        tmp = tmp + 'Positive Roots:\n==============\n'
        for v in self.__app.Groupoid.PosRoots:
            tmp = tmp + '%s\n'%v
        tmp = tmp + '\nNegative Roots:\n===============\n'
        for v in self.__app.Groupoid.NegRoots:
            tmp = tmp + '%s\n'%v
        return tmp

    def license(self):
        """ License """

        try:
            file = open('COPYING')
        except:
            return

        license = ""
        for line in file.readlines():
            license = license + line

        top = Toplevel()
        frame = Frame(top, bd=2, relief=SUNKEN)
        
        text=Text(frame, wrap=NONE, height=10, width=65)
        text.insert(END, license) 
       
        # Vertical scrollbar
        v_sb = Scrollbar(frame, orient=VERTICAL, command=text.yview)
        v_sb.pack(side=RIGHT, fill=Y)

        # Horizontal scrollbar
        h_sb = Scrollbar(frame, orient=HORIZONTAL, command=text.xview)
        h_sb.pack(side=BOTTOM, fill=X)
        
        text.pack(side=LEFT, padx=5, fill=BOTH)
        text.configure(xscrollcommand=h_sb.set, yscrollcommand=v_sb.set,state=DISABLED)
        frame.pack(expand=1, fill=X, pady=10, padx=5)

    def help(self):
        """ Information about authors """
   
        tmp = '''
Arithmetic Root Systems
=======================
Authors:
========
    Matías Graña <matiasg@dm.uba.ar>
    István Heckenberger <Istvan.Heckenberger@math.uni-leipzig.de>
    Leandro Vendramin <lvendramin@dm.uba.ar>
'''
        top = Toplevel()
        text=Text(top, wrap=NONE, height=10, width=65)
        text.insert(END, tmp) 
        text.pack(side=LEFT)
        text.configure(state=DISABLED)

###################
    
def main(filename=None):
    myapp = GUIApp(filename)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        filename = None
    else:
        filename = sys.argv[1]
    main(filename)

# vim:ts=4:sw=4:expandtab:
