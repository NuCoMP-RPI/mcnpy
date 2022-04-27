def make_deck(h:float):
    """Change control rod heights for HFIR.
    """
    deck = Deck()
    deck.read('hfir.mcnp', preprocess=True)

    # Change rod heights with TR cards.
    deck.transformations['100'].transformation.disp3 = -h
    deck.transformations['200'].transformation.disp3 = h

    # Use available material XS.
    for k in deck.materials:
        nuclides = deck.materials[k].nuclides
        for nuclide in nuclides:
            element = zaid_to_element(nuclide.name).lower()
            if element == 'mo0' or element == 'ca0':
                nuclide.library.library = '60'
            elif nuclide.library.library == '03':
                print('HERE')
                nuclide.library.library = '70'

    # Find and modify KCODE card.
    for card in deck.src_settings:
        if isinstance(card, CriticalitySource):
            card.histories = 1e5
            card.skip_cycles = 10
            card.cycles = 210

    # Print MCTAL file.
    deck.add(PrintDump(print_mctal=1))

    # Write the deck to file
    filename = 'optimization/hfir_crit_search.mcnp'
    deck.write(filename)

    # Return name of deck file
    return filename
    #return deck.direct_export()


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
    # Build the model
    print('Building')
    filename = 'optimization/hfir_crit_search.mcnp'
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
            args['rtol'] = tol

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
    from mcnpy import Deck
    from mcnpy.output import PrintDump
    from mcnpy.source import CriticalitySource
    from mcnpy.zaid_helper import zaid_to_element
    from mcnptools import Mctal, MctalKcode
    from subprocess import Popen, PIPE, CalledProcessError

    result, guesses, keffs = search_for_keff(make_deck, bracket=[float(sys.argv[1]), float(sys.argv[2])], tol=float(sys.argv[3]), print_iterations=True, bracketed_method='brentq')

    output = open('optimization/hfir_crit_search.txt', 'w')
    text = 'FINAL RESULT: ' + str(result) + '\n'
    for i in range(len(keffs)):
        text = text + ('Iteration: ' + str(i+1) + '; Guess of ' + str(guesses[i]) 
        + ' produced a keff of ' + str(keffs[i][0]) + '+/-' + str(keffs[i][1]) + '\n')
    output.write(text)
    output.close()

