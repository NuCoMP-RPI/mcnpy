from subprocess import Popen, PIPE, CalledProcessError
from os.path import isfile, join
import os

class Run():
    """Initiate MCNP simulation. Also supports calling the plotter.

    Parameters
    ==========
    input : str
        Name of the MCNP textual input file.
    exe : str
        Name of the MCNP executable.
    exe_op : str
        MCNP executions options.
    inp : boolean
        Set to True to run with 'I=input'. False for 'N=input'.
    mcnp_path : str or None
        The path to the MCNP executable. 
    data_path : str or None
        The path to the MCNP XS directory file.
    ics_path : str or None
        The path to ISC data.
    options : iterable of str
        A list of other options that require no arguments.
    **kwargs : str
        Keyword arguments for MCNP.
    """

    def __init__(self, input, exe='mcnp6', exe_op='IXR', inp=True, 
                 mcnp_path=None, data_path=None, ics_path=None, options=[], 
                 **kwargs):
        """
        """
        self.cmd = []
        self.mcnp_path = mcnp_path
        self.data_path = data_path
        self.ics_path = ics_path

        if self.mcnp_path is None:
            self.mcnp_path = os.getenv('PATH')
        
        if self.data_path is None:
            self.data_path = os.getenv('DATAPATH')
            if self.data_path is None:
                raise Exception('MCNP datapath not found!')
        
        if self.ics_path is None:
            self.ics_path = os.getenv('ISCDATA')
            if self.data_path is None:
                raise Exception('MCNP ISC datapath not found!')

        # mcnp_path was supplied or PATH envvar exists.
        if self.mcnp_path is not None:
            paths = self.mcnp_path.split(':')
            # Check if exe exists on the path.
            for p in paths:
                find_exe = isfile(join(p, exe))
                if find_exe is True:
                    # Provide absolute exe path is not using PATH envvar.
                    if mcnp_path is not None:
                        exe = join(p, exe)
                    self.cmd.append(exe)
                    break
            if find_exe is False:
                raise Exception('MCNP executable not found!')
        else:
            raise Exception('No path to MCNP executable!')

        if exe_op.upper() != 'IXR':
            self.cmd.append(exe_op)

        # MCNP kwargs entered without an '='.
        kwargs_no_equals = ['c', 'cn', 'dbug', 'tasks']

        for k in kwargs:
            if k.lower() in kwargs_no_equals:
                mcnp_kwarg = k + ' ' + str(kwargs[k])
            else:
                mcnp_kwarg = k + '=' + str(kwargs[k])
            self.cmd.append(mcnp_kwarg)

        self.cmd += options

        if inp is True:
            self.cmd.append('I=' + input)
        else:
            self.cmd.append('N=' + input)

        #print(self.cmd)
        with Popen(self.cmd, stdin=PIPE, stdout=PIPE, bufsize=1, 
                   universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='') # process line here
            #print(p.returncode)
            """if p.returncode != 0:
                raise CalledProcessError(p.returncode, p.args)"""
        
        #self.proc = Popen(self.cmd)

class RunScript():
    """
    """

    def __init__(self, script, exe, *args, **kwargs):

        self.cmd = [exe, script, args]

        for k in kwargs:
            self.cmd.append(k + '=' + str(kwargs[k]))
        
        proc = Popen()