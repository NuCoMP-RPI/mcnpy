import time
import scipy.optimize as sopt

def get_keff(file:str):
    """Get final keff from an MCTAL file.

    Parameters
    ----------
    file : str
        Name of MCTAL file with keff outputs.

    Returns
    -------
    keff_value : float
        Final keff value.
    keff_std : float
        Final keff standard deviation.
    """

    from mcnptools import Mctal, MctalKcode

    m = Mctal(file+'m')
    kc = m.GetKcode()
    keff = MctalKcode.AVG_COMBINED_KEFF
    keff_std = MctalKcode.AVG_COMBINED_KEFF_STD

    return (kc.GetValue(keff, kc.GetCycles()-1), 
            kc.GetValue(keff_std, kc.GetCycles()-1))

def _search_keff(guess, target, make_deck, run_mcnp, get_keff, deck_args, 
                 print_iterations, guesses, results):
    """Function which will actually create our deck, run the calculation, and
    obtain the result. This function will be passed to the root finding
    algorithm.

    Parameters
    ----------
    guess : float
        Current guess for the parameter to be searched in `make_deck`.
    target_keff : float
        Value to search for
    make_deck : collections.Callable
        Callable function which builds a deck according to a passed
        parameter. This function must return the name of an on-disk MCNP deck.
        Can be helpful to generate a unique name for each deck, like 
        `my_deck.iteration#.mcnp`.
    run_mcnp : collections.Callable
        Callable function which executes an MCNP simulation. Must accept the name
        of an on-disk MCNP file. Recommended to run MCNP with the `N=input_name`
        convention to create outputs with recognizable names.
    get_keff : collections.Callable
        Callable function which retrieves a keff value. Must accept the name
        of an on-disk MCNP file. Recommended to run MCNP with the `N=input_name`
        convention to create outputs with recognizable names. Also recommended to
        generate an MCTAL file and use MCNPTools to extract keff values.
    deck_args : dict
        Keyword-based arguments to pass to the `make_deck` method.
    print_iterations : bool
        Whether or not to print the guess and the resultant keff during the
        iteration process.
    guesses : Iterable of float
        Running list of guesses thus far, to be updated during the execution of
        this function.
    results : Iterable of float
        Running list of results thus far, to be updated during the execution of
        this function.

    Returns
    -------
    float
        Value of the model for the current guess compared to the target value.

    """

    # Build the model
    print('Building the MCNP Deck...')
    filename = make_deck(float(guess), **deck_args)

    # Run the model and obtain keff
    print('Initiating MCNP Simulation...')
    start = time.time()
    run_mcnp(filename)
    run_time = (time.time()-start) / 60
    keff = get_keff(filename)

    # Record the history
    guesses.append(guess)
    results.append(keff)

    if print_iterations:
        text = 'Iteration: {}; Guess of {:.5e} produced a keff of ' + \
            '{:1.5f} +/- {:1.5f} in {:1.2f} minutes'
        print(text.format(len(guesses), guess, keff[0], keff[1], run_time))

    return keff[0] - target


def search_for_keff(make_deck, run_mcnp, get_keff=get_keff, deck_args={}, 
                    initial_guess=None, target=1.0,
                    bracket=None, tol=None,
                    bracketed_method='bisect', print_iterations=False):

    """
    Keff optimization search function.

    Parameters
    ----------
    make_deck : collections.Callable
        Callable function which builds a deck according to a passed
        parameter. This function must return the name of an on-disk MCNP deck.
        Can be helpful to generate a unique name for each deck, like 
        `my_deck.iteration#.mcnp`.
    run_mcnp : collections.Callable
        Callable function which executes an MCNP simulation. Must accept the name
        of an on-disk MCNP file. Recommended to run MCNP with the `N=input_name`
        convention to create outputs with recognizable names.
    get_keff : collections.Callable
        Callable function which retrieves a keff value. Must accept the name
        of an on-disk MCNP file. Recommended to run MCNP with the `N=input_name`
        convention to create outputs with recognizable names. Also recommended to
        generate an MCTAL file and use MCNPTools to extract keff values.
    deck_args : dict
        Keyword-based arguments to pass to the `make_deck` method.
    initial_guess : float
        Initial guess for keff.
    target : float
        Target value for keff.
    bracket : Iterable of float
        Lower and upper limits for bracketed search method.
    tol : float
        Absolute tolerance.
    bracketed_method : str
        Choice of bracketed methods. Valid option are `bisect`, `brentq`, 
        `brenth`, and `ridder`. Names correspond to their SciPy functions.
    print_iterations : bool
        Whether to print information for each iteration.

    Returns
    -------
    zero_value : float
        Value of the optimized parameter.
    guesses : list
        List of parameter guesses at each iteration.
    results : list
        List of keff result at each iteration.

    """

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
    args['args'] = (target, make_deck, run_mcnp, get_keff, deck_args, 
                    print_iterations, guesses, results)

    # Perform the search
    zero_value = root_finder(**args)

    return zero_value, guesses, results
