def make_deck(h:float, **kwargs):
    """Create RCF model with at rod height `h`.

    Parameters
    ----------
    h : float
        RCF control rod bank height.
    **kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    filename : str
        Name of the serialized MCNP deck.

    """
    
    name = 'rcf_rods_' + str(h) + '.mcnp'
    rcf = mp.RCF(name, 68, h)
    rcf.deck += mp.PrintDump(print_mctal=1)

    # Write the deck to file
    filename = 'optimization/' + name
    rcf.deck.write(filename)

    # Return name of deck file
    return filename

def run_mcnp(file:str):
    """Run MCNP from script.
    """
    script = r'/home/peter/MCNP620/scripts/execute.sh'
    exe = 'bash'
    mp.run_script(script, exe, file, lineout=False)

if __name__ == '__main__':
    import sys
    import mcnpy as mp
    from mcnpy.search import search_for_keff, get_keff

    crit_height, guesses, keffs = search_for_keff(make_deck, run_mcnp, get_keff, 
                                                  bracket=[float(sys.argv[1]), 
                                                           float(sys.argv[2])], 
                                                  tol=float(sys.argv[3]), 
                                                  print_iterations=True, 
                                                  bracketed_method='brentq')

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

