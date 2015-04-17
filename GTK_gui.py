#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')

import gtk
import gobject 

import pydot

(COLUMN_DEGREE, COLUMN_DIMENSION) = range(2)
(COLUMN_ROOT, COLUMN_QFF, COLUMN_ORDER) = range(3)

from mainapp import *
from sys import argv

DESCRIPTION = ('Arithmetic Root system')

AUTHORS = [ "MatÃ­as GraÃ±a <matiasg@dm.uba.ar>", \
            "IstvÃ¡n Heckenberger <Istvan.Heckenberger@math.uni-leipzig.de>", \
            "Leandro Vendramin <lvendramin@dm.uba.ar>"]

LICENSE = '''
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by 
the Free Software Foundation; either version 2 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program; if not, write to the Free Software Foundation, Inc., 
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
''' 

class GTKApplication:
    ui = '''<ui>
    <menubar name="MenuBar">
        <menu action="File">
            <menuitem action="New"/>
            <menuitem action="Open"/>
            <separator/>
            <menuitem action="Quit"/>
        </menu>

        <menu action="Gnuplot">
            <menuitem action="Show simple roots"/>
            <menuitem action="Show arrows"/>
            <separator/>
            <menuitem action="Redraw"/>
            <menuitem action="Save Gnuplot file"/>
            <menuitem action="Enter Gnuplot command"/>
        </menu>

        <menu action="Ars">
            <menuitem action="View braid"/>
            <separator/>
            <menuitem action="Change current basis"/>
            <menuitem action="Reflect on a simple root"/>
            <menuitem action="Show roots"/>
            <menuitem action="Show roots f and qff"/>
            <menuitem action="Show Dynkin diagram"/>
            <separator/>
        </menu>

        <menu action="Nichols algebra">
            <menuitem action="Dimension"/>
            <menuitem action="Dimension table"/>
            <menuitem action="GK dimension"/>
            <separator/>
            <menuitem action="Hilbert series"/>
            <separator/>
            <menuitem action="Truncate degree"/>
        </menu>

        <menu action="Help">
            <menuitem action="About"/>
        </menu>

    </menubar>
    </ui>'''

    def __init__(self):
        """ Create the toplevel window """

        window = gtk.Window()
        window.set_title('Arithmetic Root Systems')
        window.connect('destroy', lambda w: gtk.main_quit())
        window.set_size_request(500, -1)
        window.set_resizable(False)

        vbox = gtk.VBox()
        window.add(vbox)
        
        # Globals 
        self.filename = None
        self.about_dialog = None
        self.command_dialog = None
        self.truncate = 0

        # Create a UIManager instance
        uimanager = gtk.UIManager()
        uimanager.set_add_tearoffs(True)
        
        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        window.add_accel_group(accelgroup)

        # Create an ActionGroup
        actiongroup = gtk.ActionGroup('UIManageExample')
        self.actiongroup = actiongroup

        # Create a ToggleAction, etc.
        actiongroup.add_toggle_actions([\
                ('Show simple roots', None, '_Show simple roots', '<Control>s', 'Show simple roots', self.toggle_gnuplot_showsimples, True),
                ('Show arrows', None, 'Show _arrows', '<Control>a', None, self.toggle_gnuplot_showarrows)]) 
        #        ('Open Gnuplot window', None, '_Open Gnuplot window', '<Control>o', None, self.toggle_gnuplotwindow, False)])

        # Create actions
        actiongroup.add_actions([('File', None, '_File'),
                                ('New', gtk.STOCK_NEW, '_New'),
                                ('Open', gtk.STOCK_OPEN, '_Open', '<Control>O', None, self.openfile),
                                ('Quit', gtk.STOCK_QUIT, '_Quit me!', '<Control>Q', None, self.quit_cb),

                                ('Gnuplot', None, '_Gnuplot'),
                                ('Redraw', None, '_Redraw', None, None),
                                ('Save Gnuplot file', None, '_Save Gnuplot file'),
                                ('Enter Gnuplot command', None, 'Enter Gnuplot _command', None, None, self.enter_command),

                                ('Ars', None, '_Ars'),
                                ('View braid', None, '_View braid', None, None, self.view_braid),
                                ('Change current basis', None, 'Change current _basis', None, None, self.change_basis),
                                ('Reflect on a simple root', None, 'Reflect on a s_imple root', None, None, self.reflect_simple),
                                ('Show roots', None, 'Show _roots', None, None, self.view_roots),
                                ('Show roots f and qff', None, 'Show roots _f and qff', None, None, self.view_roots_f),
                                ('Show Dynkin diagram', None, 'Show _Dynkin diagram', None, None, self.view_dynkin_diagram),
                                
                                ('Nichols algebra', None, '_Nichols algebra'),
                                ('Dimension', None, '_Dimension', None, None, self.view_dimension),
                                ('Dimension table', None, 'Dimension _table', None, None, self.view_dimension_table),
                                ('GK dimension', None, '_GK dimension', None, None, self.view_GK_dimension),
                                ('Hilbert series', None, '_Hibert series', None, None, self.view_hilbert_series),
                                ('Truncate degree', None, '_Truncate degree', None, None, self.change_truncate_degree),
                                
                                ('Help', None, '_Help'),
                                ('About', gtk.STOCK_ABOUT, '_About', None, None, self.about)
                                
                                ])

        uimanager.insert_action_group(actiongroup, 0)

        # Add a UI description
        uimanager.add_ui_from_string(self.ui)

        # Create a MenuBar
        menubar = uimanager.get_widget('/MenuBar')
        vbox.pack_start(menubar, False)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, expand=False)

        # Create the expander
        expander = gtk.Expander("Details")
        vbox.pack_start(expander, False, False, 0)

        # Open file if called with a file name
        if len(argv) > 1:
            try:
                ffdummy = open(argv[1], 'r');
                ffdummy.close()
                self.filename = argv[1]
                label = gtk.Label(self.filename)
            except:
                print 'File error: can\'t open file',argv[1];
                label = gtk.Label('No file loaded!')
        else:
            label = gtk.Label('No file loaded!')

        expander.add(label)
        #expander.connect('notify::expanded',self.__update_expander)

        #vbox.pack_start(label)
        self.filelabel = label

        separator = gtk.HSeparator()
        vbox.pack_start(separator, expand=False)
        #buttonbox = gtk.HButtonBox()
        gnuplotwindow = gtk.CheckButton('Gnuplot Window')
        self.gpcheckb = gnuplotwindow
        gnuplotwindow.set_active(False)
        self.gpid = None
        #buttonbox.pack_start(gnuplotwindow, False)
        vbox.pack_start(gnuplotwindow)

        # again, we set the filename
        if self.filename <> None:
            self.__aftersettingfilename(mustupdate=False)

        # No braid file, no menu
        self.actiongroup.get_action('Gnuplot').set_sensitive(self.filename<>None)
        self.actiongroup.get_action('Ars').set_sensitive(self.filename<>None)
        self.actiongroup.get_action('Nichols algebra').set_sensitive(self.filename<>None)

        window.show_all()
        return

    def enter_command(self, action):
        """ Enter a gnuplot command """

        if self.command_dialog:
            self.command_dialog.present()
            return

        dialog = gtk.Window(gtk.WINDOW_TOPLEVEL)
        dialog.set_size_request(300, 50)
        dialog.set_title("Gnuplot command")
        dialog.connect("delete_event", self.__command_response)

        vbox = gtk.VBox(False, 0)
        dialog.add(vbox)
        vbox.show()

        entry = gtk.Entry()
        entry.set_max_length(50)
        entry.connect("activate", self.__command_entercallback, entry)
        entry.set_text("enter your command here")
        entry.select_region(0, len(entry.get_text()))
        vbox.pack_start(entry, True, True, 0)
        entry.show()

        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()

        check = gtk.CheckButton("Redraw")
        hbox.pack_start(check, False)
        check.connect("toggled", self.__command_redraw, entry)
        check.set_active(True)
        check.show()
        
        dialog.show()
        self.command_dialog = dialog
 
    def __command_response(self, dialog, response):
        self.command_dialog.destroy()
        self.command_dialog = None

    def __command_redraw(self, checkbutton, entry):
        """ for redraw """
        if checkbutton.get_active():
            print 'on!';

    def __command_entercallback(self, widget, entry):
        """ for enter gnuplot command """
        not_valid = ['quit', 'reset']
        if entry.get_text() not in not_valid:
            self.__app.GnuplotWindow(entry.get_text())
            self.__app.draw()

    def openfile(self, action):
        """ GTK open file dialog """
        
        dialog = gtk.FileChooserDialog(title="Open ARS file")
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("ARS files (*.ars)")
        filter.add_pattern("*.ars")
        dialog.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name('All Files')
        filter.add_pattern('*')
        dialog.add_filter(filter)
        result = dialog.run()
        dialog.hide()
        if result == gtk.RESPONSE_OK:
            self.filename = dialog.get_filename()
            print self.filename
            self.__aftersettingfilename()
            
        dialog.destroy()

    def __aftersettingfilename(self, mustupdate=True):
        self.__app = MainApp(self.filename, True)
        if mustupdate:
            self.__update_information()
        if self.__app.Groupoid.Rank==2 or self.__app.Groupoid.Rank==3:
            self.actiongroup.get_action('Gnuplot').set_sensitive(True)
            self.gpcheckb.set_active(True)
            self.gpid = self.gpcheckb.connect('toggled', self.toggle_gnuplotwindow)
            self.__app.draw()
        else:
            self.actiongroup.get_action('Gnuplot').set_sensitive(False)
            self.gpcheckb.set_active(False)
            if not self.gpid == None:
                self.gpcheckb.disconnect(self.gpid)
                self.gpid = None
        self.actiongroup.get_action('Ars').set_sensitive(True)
        self.actiongroup.get_action('Nichols algebra').set_sensitive(True)

    def view_GK_dimension(self, action):
        """ GK dimension """

        i = self.__app.Nichols.GKdim()

        dialog = gtk.MessageDialog(None,\
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,\
                gtk.MESSAGE_INFO, gtk.BUTTONS_OK,\
                "The GK-dimension of the Nichols algebra is %s" % i)
        dialog.run()
        dialog.destroy()

    def view_dimension(self, action):
        """ The dimension of the Nichols algebra """

        i = self.__app.Nichols.dimension()
        if i == 0:
            i = 'infinite'
        else:
            i = str(i)

        dialog = gtk.MessageDialog(None,\
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,\
                gtk.MESSAGE_INFO, gtk.BUTTONS_OK,\
                "The dimension of the Nichols algebra is %s" % i)

        dialog.run()
        dialog.destroy()

    def view_dynkin_diagram(self, action):
        """
        Draw the generalized Dynkin diagram associated to the current basis
        """

#        TODO: 
#        1) dialog to save jpeg file 
#        2) better managment of temporary file

        nq = self.__app.Groupoid.braid_for_basis(self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis])
        nq = triang(self.__app.Groupoid.NumberOfParameters,nq,self.__app.Groupoid.Order)
        edges = []
        for i in xrange(self.__app.Groupoid.Rank):
            edges.append((i+1,i+1))
            for j in xrange(i+1,self.__app.Groupoid.Rank):
                if notone(self.__app.Groupoid.NumberOfParameters, nq[i][j], self.__app.Groupoid.Order):
                    edges.append((i+1,j+1))
        jpeg=pydot.graph_from_edges(edges)
        for i in xrange(self.__app.Groupoid.Rank):
            ei = jpeg.get_edge(str(i+1),str(i+1))
            ei.set('headlabel',nq[i][i])
            ei.set('color','transparent')
            for j in xrange(i+1,self.__app.Groupoid.Rank):
                try:
                    eij = jpeg.get_edge(str(i+1),str(j+1))
                    eij.set_label(nq[i][j])
                except:
                    pass
        nl = jpeg.get_node_list()
        for n in nl:
            n.set('style','filled')
            n.set('fillcolor','red')
            n.set('shape','circle')
            n.set('fixedsize','true')
            n.set('width',.3)

        jpeg.write_jpeg('dynkin.jpg', prog='neato')

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Dynkin diagram')
        window.set_resizable(False)
        window.set_border_width(10)
        
        vbox = gtk.VBox(False, 0)
        window.add(vbox)
        vbox.show()

        image = gtk.Image()
        image.set_from_file("dynkin.jpg")
        image.show()
        
        vbox.pack_end(image, True, True, 2)
        window.show()

    def view_dimension_table(self, action):
        """ Open a dialog with the dimension table """

        print self.truncate
        i = self.__app.Nichols.dimension()
        if (i > 0) or (self.truncate > 0):
            dt = self.__app.Nichols.hilberttable(self.truncate)
            data = []
            if (len(dt) > 0):
                for j in xrange(len(dt)):
                    data.append([j,dt[j]])
            else:
                return

        dialog = gtk.Window(gtk.WINDOW_TOPLEVEL)
        dialog.set_resizable(True)
        dialog.set_title('Dimension table')
        dialog.set_default_size(300,200)
        dialog.set_border_width(8)

        vbox = gtk.VBox(False, 8)
        dialog.add(vbox)

        if i == 0:
            i = 'infinite'
        else:
            i = str(i)

        label = gtk.Label('The dimension of the Nichols algebra is %s'%i)
        vbox.pack_start(label, False, False)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        # Create the model
        model = gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_UINT)
        for item in data:
            iter = model.append()
            model.set(iter, COLUMN_DEGREE, item[COLUMN_DEGREE], COLUMN_DIMENSION, item[COLUMN_DIMENSION])

        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)
        sw.add(treeview)

        # For the rank
        column = gtk.TreeViewColumn('Degree', gtk.CellRendererText(), text=COLUMN_DEGREE)
        column.set_sort_column_id(COLUMN_DEGREE)
        treeview.append_column(column)

        # For the dimension
        column = gtk.TreeViewColumn('Dimension', gtk.CellRendererText(), text=COLUMN_DIMENSION)
        column.set_sort_column_id(COLUMN_DIMENSION)
        treeview.append_column(column)

        statusbar = gtk.Statusbar()
        vbox.pack_start(statusbar, False, False, 0)
        statusbar.push(0, 'Top degree: %d'%(len(dt)-1))
        statusbar.show()

        dialog.show_all()

    def change_basis(self, action):
        """ Dialog to change the current basis """

        dialog = gtk.Window()
        dialog.set_title('Change the current basis')
        dialog.set_resizable(False)

        dialog.set_border_width(8)

        vbox = gtk.VBox(False, 8)
        dialog.add(vbox)

        label = gtk.Label('There are %d bases'%len(self.__app.Groupoid.Bases))
        vbox.pack_start(label, False, False)

        combobox = gtk.ComboBox()
        liststore = gtk.ListStore(str)
        cell = gtk.CellRendererText()

        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)

        vbox.add(combobox)

        combobox.set_wrap_width(4)
        for n in xrange(len(self.__app.Groupoid.Bases)):
            liststore.append(['%s'%self.__app.Groupoid.Bases[n]])
        combobox.set_model(liststore)
        combobox.connect('changed', self.__changed)
        combobox.set_active(0)
        dialog.show_all()

    def __changed(self, combobox):
        """ When a basis is selected we have to recalculate all the roots """
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            self.__app.Groupoid.change_basis(index)
            self.__update_information()
            self.__app.draw()

    def __changed_trun(self, combobox):
        """ change degree truncation, poor man option """
        index = combobox.get_active()
        self.truncate = index

    def __reflect(self, combobox,dialog):
        """ After reflection on a root we have to recalculate all the roots """
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            self.__app.Groupoid.apply_reflection(index)
            self.__update_information()
            self.__app.draw()
            dialog.destroy()

    def reflect_simple(self, action):
        """ Dialog to reflect on a simple root """

        dialog = gtk.Window(gtk.WINDOW_TOPLEVEL)
        dialog.set_title('Choose!')
        dialog.set_resizable(False)

        dialog.set_border_width(8)

        vbox = gtk.VBox(False, 8)
        dialog.add(vbox)

        label = gtk.Label('There are %d simple roots.'%self.__app.Groupoid.Rank)
        vbox.pack_start(label, False, False, 0)

        combobox = gtk.ComboBox()
        liststore = gtk.ListStore(str)
        cell = gtk.CellRendererText()

        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)

        vbox.add(combobox)

#        combobox.set_wrap_width(4)
        for n in range(self.__app.Groupoid.Rank):
            liststore.append(str(n+1))
        combobox.set_model(liststore)
        combobox.connect('changed', self.__reflect,dialog)
        combobox.set_active(-1)
        dialog.show_all()

    def view_hilbert_series(self, action):
        """ Open a dialog with the Hilbert series """

        tmp = ""
        hs = self.__app.Nichols.hilbertseries(True); 
        for i in xrange(len(hs)-1):
            tmp = tmp + hs[i]

        self.__view_text('Hilbert series', tmp)

    def change_truncate_degree(self, action):
        """ Open a window to set degree truncation """
        dialog = gtk.Window()
        dialog.set_title('Change degree truncation')
        dialog.set_resizable(False)

        dialog.set_border_width(8)

        vbox = gtk.VBox(False, 8)
        dialog.add(vbox)

        label = gtk.Label('Change it!')
        vbox.pack_start(label, False, False)

        combobox = gtk.ComboBox()
        liststore = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)
        vbox.add(combobox)
        combobox.set_wrap_width(4)
        for n in xrange(18):
            liststore.append(['%s'%n])
        combobox.set_model(liststore)
        combobox.connect('changed', self.__changed_trun)
        combobox.set_active(0)
        dialog.show_all()

    def view_roots(self, action):
        """ Open a dialog with positive and negative roots of the Weyl groupoid """

        tmp = 'Current basis:\n'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis]
        tmp = tmp + 'Positive Roots:\n'

        for v in self.__app.Groupoid.PosRoots:
            tmp = tmp + '%s\n'%v
        tmp = tmp + '\nNegative Roots:\n'
        for v in self.__app.Groupoid.NegRoots:
            tmp = tmp + '%s\n'%v

        self.__view_text('Roots', tmp, 'Current basis: %s'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis])

    def view_roots_f(self, action):
        """ Open a dialog with positive roots f and braiding q_ff of the Weyl groupoid """

        data = self.__app.Nichols.roots_coefs()
        #data = [['root','q_ff','order']] + rtsqs
        #tmp = '%16s %10s %5s\n' % ('root','q_ff','order') + '='*33 
        #for i in rtsqs:
        #    tmp = tmp + '\n%16s %10s %5d' % (i[0],i[1],i[2])
        #self.__view_text('Roots', tmp, 'Current basis: %s'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis])

        dialog = gtk.Window(gtk.WINDOW_TOPLEVEL)
        dialog.set_resizable(True)
        dialog.set_title('Roots and orders')
        dialog.set_default_size(300,200)
        dialog.set_border_width(8)
        vbox = gtk.VBox(False, 8)
        dialog.add(vbox)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        # Create the model
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT)
        for item in data:
            iter = model.append()
            model.set(iter, COLUMN_ROOT, item[COLUMN_ROOT], COLUMN_QFF, item[COLUMN_QFF], COLUMN_ORDER, item[COLUMN_ORDER])

        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)
        sw.add(treeview)

        # For the roots
        column = gtk.TreeViewColumn('root', gtk.CellRendererText(), text=COLUMN_ROOT)
        column.set_sort_column_id(COLUMN_ROOT)
        treeview.append_column(column)

        # For the braid
        column = gtk.TreeViewColumn('q_ff', gtk.CellRendererText(), text=COLUMN_QFF)
        column.set_sort_column_id(COLUMN_QFF)
        treeview.append_column(column)

        # For the order
        column = gtk.TreeViewColumn('order', gtk.CellRendererText(), text=COLUMN_ORDER)
        column.set_sort_column_id(COLUMN_ORDER)
        treeview.append_column(column)

        statusbar = gtk.Statusbar()
        vbox.pack_start(statusbar, False, False, 0)
        statusbar.push(0, 'Current basis:')
        statusbar.push(1, '%s'%self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis])
        statusbar.show()

        dialog.show_all()

    def view_braid(self, action):
        """ Open a dialog with the braid data """

        self.__view_text('Braid', self.__app.FileData, 'File: %s'%self.filename)

    def about(self, action):
        """ The about dialog """

        if self.about_dialog:
            self.about_dialog.present()
            return

        about = gtk.AboutDialog()
        about.set_name("Arithmetic Root Systems")
        #about.set_copyright("copyright")
        about.set_authors(AUTHORS)
        about.set_license(LICENSE)
        about.set_comments('Weyl Groupoids and Nichols Algebras')
        about.set_website("http://buggies.dm.uba.ar/ars/")
        about.connect ("response", self.about_response)
        about.show()

        self.about_dialog = about

    def about_response(self, dialog, response):
        self.about_dialog.destroy()
        self.about_dialog = None

    def toggle_gnuplot_showarrows(self, action):
        """ To toggle ShowArrows (show arrows) """

        self.__app.change_option('ShowArrows')
        self.__app.draw()

    def toggle_gnuplot_showsimples(self, action):
        """ To toggle ShowSimples (show simple roots) """
        self.__app.change_option('ShowSimples')
        self.__app.draw()

    def toggle_gnuplotwindow(self, action):
        """ To toggle OpenGnuplotWindow (open a gnuplot window?) """

        self.__app.change_option('OpenGnuplotWindow')
        if not self.__app.Options['OpenGnuplotWindow']:
            self.actiongroup.get_action('Gnuplot').set_sensitive(False)
            self.__app.GnuplotWindow('quit')
            self.__app.GnuplotWindow = Gnuplot()
        else:
            self.actiongroup.get_action('Gnuplot').set_sensitive(True)
            self.__app.draw()

    def __view_text(self, title, buffer, sb=None):
        """ To show text in a dialog box """

        dialog = gtk.Window(gtk.WINDOW_TOPLEVEL)
        dialog.set_resizable(True)
        dialog.set_title(title)
        dialog.set_default_size(200,200)

        box1 = gtk.VBox(False, 10)
        dialog.add(box1)
        box1.show()

        box2 = gtk.VBox(False, 10)
        box2.set_border_width(0)
        box1.pack_start(box2, True, True, 0)
        box2.show()

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()

        textview.set_editable(False)
        textview.set_cursor_visible(False)

        textbuffer = textview.get_buffer()
        sw.add(textview)
        sw.show()
        textview.show()

        box2.pack_start(sw)
        textbuffer.set_text(buffer)

        if sb is not None:
            statusbar = gtk.Statusbar()
            box1.pack_start(statusbar, False, False, 0)
            statusbar.push(0, sb)
            statusbar.show()

        dialog.show()

#    def __update_expander(self,expander,params):
#        self.__update_information()
#        return

    def __update_information(self):
        """ The information of the expander box """
        if self.filename == None:
            label = gtk.Label('No braid file loaded')
        else:
            txt = 'Braid file: ' + self.filename + '\n'
            txt += 'Rank: ' + str(self.__app.Groupoid.Rank) + '\n'
            txt += 'Current Basis: ' + str(self.__app.Groupoid.Bases[self.__app.Groupoid.CurrentBasis])
            self.filelabel.set_text(txt)
        return

    def quit_cb(self, b):
        print 'Quitting program'
        gtk.main_quit()

if __name__ == '__main__':
    ba = GTKApplication() 
    gtk.main()

# vim:ts=4:sw=4:fenc=UTF-8:
