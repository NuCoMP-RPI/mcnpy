def make_deck(h:float):
    """Create RCF model with at rod height `h`.
    """
    name = 'rcf_rods_' + str(h) + '.mcnp'
    rcf = mp.RCF(name, 68, h)
    rcf.deck += mp.PrintDump(print_mctal=1)

    # Write the deck to file
    filename = 'optimization/' + name
    rcf.deck.write(filename)

    # Return name of deck file
    return filename

def get_keff(file:str):
    """Get final keff from an MCTAL file.
    """
    m = Mctal(file)
    kc = m.GetKcode()
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
    filename = make_deck(float(guess))

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
    from mcnptools import Mctal, MctalKcode
    from subprocess import Popen, PIPE, CalledProcessError

    #crit_radius, guesses, keffs = search_for_keff(make_deck, initial_guess=float(sys.argv[1]), tol=float(sys.argv[2]), print_iterations=True)
    crit_height, guesses, keffs = search_for_keff(make_deck, bracket=[float(sys.argv[1]), float(sys.argv[2])], tol=float(sys.argv[3]), print_iterations=True, bracketed_method='brentq')

    output = open('optimization/crit_search_ref_rods.tex', 'w')
    text = 'CRITICAL HEIGHT: ' + str(crit_height) + '\n'
    text = (r'\begin{table}[h]' 
            + '\n  ' + r'\centering' 
            + '\n  ' + r'\caption{\bf RCF Control Rod Critical Bank Height.}' 
            + '\n  ' + r'\label{tabel:rcf_bank_height}' 
            + '\n  ' + r'\begin{tabular}{|c|c|c|c|c|c|}  \hline '
            + '\n  ' + r'Iteration & Height (in) & $k_{\text{eff}}$ & $k_{\text{eff}}$-1 (pcm) & $\sigma_{keff}$ (pcm)  \\ \hline')
    for i in range(len(keffs)):
        height = round(guesses[i], 3)
        k = round(keffs[i][0], 5)
        k_1 = round((keffs[i][0]-1) * 1e5, 1)
        k_sig = round(keffs[i][1] * 1e5, 1)
        text += '\n  ' + str(i+1) + ' & ' + str(height) + ' & ' + str(k) + ' & ' + str(k_1) + '+/-' + str(k_sig) + r'  \\ \hline'
    text += '\n  ' + r'\end{tabular}' + '\n' + r'\end{table}'
    output.write(text)
    output.close()

