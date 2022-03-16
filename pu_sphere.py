def make_deck(r:float):
    """Create Pu sphere in MCNP with radius `r`.
    """
    deck = mp.InputDeck()

    # Materials
    pu = [Nuclide(name='pu239', fraction=0.046982),
          Nuclide(name='pu240', fraction=0.0025852),
          Nuclide(name='pu241', fraction=0.00014915)]
    """water = [Nuclide(name='h1', fraction=0.066766),
             Nuclide(name='o16', fraction=0.033383)]"""
    m_pu = mp.Material(name=1, nuclides=pu)
    #m_water = mp.Material(name=2, nuclides=water)
    """sab_water = mp.SabBase()
    sab_water.material = m_water
    lwtr = mp.SabLibraryBase()
    lwtr.nuclide = 'lwtr'
    sab_water.libraries = [lwtr]"""
    #deck.add_all([m_pu, m_water, sab_water])
    deck.add_all([m_pu])

    # Surfaces
    sphere_pu = Sphere(name=1, x0=0, y0=0, z0=0, r=r)
    #sphere_water = Sphere(name=2, x0=0, y0=0, z0=0, r=29.5217)
    #deck.add_all([sphere_pu, sphere_water])
    deck.add(sphere_pu)

    # Cells
    cell_pu = mp.Cell(name=1, material=m_pu, density=0.04971635, region=-sphere_pu)
    """cell_water = mp.Cell(name=2, material=m_water, density=0.100149, 
                         region=+sphere_pu & -sphere_water)"""
    cell_outside = mp.Cell(name=3, material=None, region=+sphere_pu)
    # Cell importances
    imp_n1 = mp.CellImportanceBase()
    imp_n1.particles = ['n']
    imp_n1.importance = 1
    imp_n0 = mp.CellImportanceBase()
    imp_n0.particles = ['n']
    imp_n0.importance = 0
    cell_pu.importances = [imp_n1]
    #cell_water.importances = [imp_n1]
    cell_outside.importances = [imp_n0]
    deck.add_all([cell_pu, cell_outside])

    # Kcode
    kcode = mp.CriticalitySourceBase()
    kcode.histories = 1e3
    kcode.keff_guess = 1.0
    kcode.skip_cycles = 10
    kcode.cycles = 210
    ksrc = mp.CriticalitySourcePointsBase()
    src_points = [mp.Point(0,0,0)]
    ksrc.points = src_points
    deck.add_all([kcode, ksrc])

    # Outputs
    #deck.add(mp.PrintBase())
    print_dump = mp.PrintDumpBase()
    print_dump.jump = ['j', 'j']
    print_dump.print_mctal = 1
    deck.add(print_dump)

    return deck.export(title='Pu Sphere')


def get_keff(file:str):
    """Get final keff from an MCTAL file.
    """
    m = Mctal(file)
    kc =m.GetKcode()
    keff = MctalKcode.AVG_COMBINED_KEFF
    keff_std = MctalKcode.AVG_COMBINED_KEFF_STD

    return (kc.GetValue(keff, kc.GetCycles()-1), kc.GetValue(keff_std, kc.GetCycles()-1))

def run_mcnp(file:str):
    """Run MCNP from script.
    """
    path = r'/home/peter/MCNP620/scripts/'

    with Popen(['bash', path + 'execute.sh', file], stdin=PIPE, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            """print(line, end='') # process line here"""

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)

def _search_keff(guess, target, make_deck, print_iterations,
                 guesses, results):
    """Function which will actually create our model, run the calculation, and
    obtain the result. This function will be passed to the root finding
    algorithm

    Parameters
    ----------
    guess : Real
        Current guess for the parameter to be searched in `model_builder`.
    target_keff : Real
        Value to search for
    model_builder : collections.Callable
        Callable function which builds a model according to a passed
        parameter. This function must return an openmc.model.Model object.
    model_args : dict
        Keyword-based arguments to pass to the `model_builder` method.
    print_iterations : bool
        Whether or not to print the guess and the resultant keff during the
        iteration process.
    print_output : bool
        Whether or not to print the OpenMC output during the iterations.
    guesses : Iterable of Real
        Running list of guesses thus far, to be updated during the execution of
        this function.
    results : Iterable of Real
        Running list of results thus far, to be updated during the execution of
        this function.

    Returns
    -------
    float
        Value of the model for the current guess compared to the target value.

    """

    # Build the model
    print('Building')
    filename = 'optimization/pu_sphere.mcnp'
    deck = open(filename, 'w')
    deck.write(make_deck(float(guess)))
    deck.close()

    # Run the model and obtain keff
    print('Running')
    start = time.time()
    run_mcnp(filename)
    run_time = (time.time()-start) / 60
    keff = get_keff(filename + 'm')

    # Record the history
    guesses.append(guess)
    results.append(keff)

    if print_iterations:
        text = 'Iteration: {}; Guess of {:.5e} produced a keff of ' + \
            '{:1.5f} +/- {:1.5f} in {:1.2f} minutes'
        print(text.format(len(guesses), guess, keff[0], keff[1], run_time))

    return keff[0] - target


def search_for_keff(make_deck, initial_guess=None, target=1.0,
                    bracket=None, tol=None,
                    bracketed_method='bisect', print_iterations=False):

    # Set the iteration data storage variables
    guesses = []
    results = []

    # Set the searching function (for easy replacement should a later
    # generic function be added.
    search_function = _search_keff

    if bracket is not None:
        # Generate our arguments
        args = {'f': search_function, 'a': bracket[0], 'b': bracket[1]}
        if tol is not None:
            args['xtol'] = tol

        # Set the root finding method
        if bracketed_method == 'brentq':
            root_finder = sopt.brentq
        elif bracketed_method == 'brenth':
            root_finder = sopt.brenth
        elif bracketed_method == 'ridder':
            root_finder = sopt.ridder
        elif bracketed_method == 'bisect':
            root_finder = sopt.bisect

    elif initial_guess is not None:

        # Generate our arguments
        args = {'func': search_function, 'x0': initial_guess}
        if tol is not None:
            args['tol'] = tol

        # Set the root finding method
        root_finder = sopt.newton

    else:
        raise ValueError("Either the 'bracket' or 'initial_guess' parameters "
                         "must be set")

    # Add information to be passed to the searching function
    args['args'] = (target, make_deck, print_iterations,
                    guesses, results)

    # Perform the search
    zero_value = root_finder(**args)

    return zero_value, guesses, results


if __name__ == '__main__':
    import sys, time
    import scipy.optimize as sopt
    import mcnpy as mp
    from mcnpy import MaterialNuclide as Nuclide
    from mcnpy.surfaces import Sphere
    from mcnptools import Mctal, MctalKcode
    from subprocess import Popen, PIPE, CalledProcessError

    #crit_radius, guesses, keffs = search_for_keff(make_deck, initial_guess=float(sys.argv[1]), tol=float(sys.argv[2]), print_iterations=True)
    crit_radius, guesses, keffs = search_for_keff(make_deck, bracket=[float(sys.argv[1]), float(sys.argv[2])], tol=float(sys.argv[3]), print_iterations=True, bracketed_method='brentq')

    output = open('optimization/crit_search.txt', 'w')
    text = 'CRITICAL RADIUS: ' + str(crit_radius) + '\n'
    for i in range(len(keffs)):
        text = text + ('Iteration: ' + str(i+1) + '; Guess of ' + str(guesses[i]) 
        + ' produced a keff of ' + str(keffs[i][0]) + '+/-' + str(keffs[i][1]) + '\n')
    output.write(text)
    output.close()

