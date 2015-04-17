
"""

Test of bidirectional interfacing with gnuplot.
Main feature:
  - get variables from (very recent CVS) gnuplot.
  - even allows to wait for a mouse-click and read
    the coordinates back to python
    (thanks to the recent change of gnuplot by Ethan the `pause mouse`
     can be used from a pipe as now - thanks!)

See the gnuplot help,
  - `help mouse` 
  -  help mouse variables`
for further details on the behaviour of `pause mouse`

No capture of stderr (using popen3 should allow this....)

This has only been tested under linux (debian, testing).
I have no idea about M$Windows or Mac.


Version 0.0.1, 31.07.2003, Arnd Baecker
Version 0.0.2, 04.10.2003, Arnd Baecker
Version 0.0.3, 07.01.2004, Arnd Baecker
Version 0.0.4, 12.01.2004, Arnd Baecker

"""

from os import popen2

class Gnuplot:
    """Interface to gnuplot."""

    def __init__(self):
        """Create a pipe to gnuplot"""
        self.gpwrite,self.gpout=popen2("gnuplot")

    def __call__(self, s):
        """Send string to gnuplot"""

        self.gpwrite.write(s+"\n")
        self.gpwrite.flush()
        
    def getvar(self,var):
        """Get a gnuplot variable

           In order to avoid locking we have to check
           if the variable is really defined.
           This only works with a recent CVS gnuplot
           (having the defined(var) function;
            this is enabled per default).

           FIXME: no real error checking done so far ....
           FIXME: we could try to convert the returned string
                  to a float or int (depending on
                  an optional parameter passed to getvar)

        """
        self(" set print \"-\"\n")      # print output to stdout
        self(" if (defined(%s)) print %s ; else print \"None\" \n" % (var,var))
        result=self.gpout.readline()
        self(" set print\n")            # print output to default stderr
        if result[0:4]=="None":
            return None
        return(result)


if __name__=="__main__":
    # simple test/example:
    import string
    
    gp=Gnuplot()
    gp("set mouse")
    gp("plot sin(x)")
    gp("a=10")
    print "string for `a` as recieved from gnuplot: ",gp.getvar("a")
    # This one has not been defined ...
    # ... and we get "None"
    # (maybe one should raise an error here ...)
    print "string for `b` as recieved from gnuplot: ",gp.getvar("b")

    # convert to variable usable in python
    a=string.atof(gp.getvar("a"))
    print "a as recieved from gnuplot, converted to float ",a

    # one more test:
    gp("c=11")
    gp("this_command_is_not_known_to_gnuplot_but_no_problem_to_recover_c")
    print "string for `c` as recieved from gnuplot: ",gp.getvar("c")

    # Even this works now !!!
    gp("set title 'click with the mouse'")
    gp("plot sin(x)")
    print "var=",gp.getvar("a")  
    print "Now get coordinates of a mouse-click:"
    gp("pause mouse 'click with mouse' ")

    print "MOUSE_BUTTON:",gp.getvar("MOUSE_BUTTON")
    print "MOUSE_SHIFT :",gp.getvar("MOUSE_SHIFT")
    print "MOUSE_ALT   :",gp.getvar("MOUSE_ALT")
    print "MOUSE_CTRL  :",gp.getvar("MOUSE_CTRL")

    
    mouse_x=string.atof(gp.getvar("MOUSE_X"))
    mouse_y=string.atof(gp.getvar("MOUSE_Y"))
    print "Clicked mouse coords: x,y= ",mouse_x,mouse_y

    mouse_x2=string.atof(gp.getvar("MOUSE_X2"))
    mouse_y2=string.atof(gp.getvar("MOUSE_Y2"))
    print "Clicked mouse coords: x2,y2= ",mouse_x2,mouse_y2

    gp("show xrange")
    gp("show yrange")
    raw_input("")
