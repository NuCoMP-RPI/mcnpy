from re import search, compile, finditer, findall, IGNORECASE

def line_wrap(before_comment, comment, line_limit):
    if (len(before_comment) > line_limit):
        line = ''
        ws_index = 0
        while (len(before_comment) > line_limit):
            for i in range(len(before_comment)):
                if (before_comment[i] == ' '):
                    ws_index = i
                if (i >= line_limit-1):
                    if (before_comment[ws_index:].lstrip() != ''):
                        line = line + before_comment[:ws_index]
                        before_comment = '\n     ' + before_comment[ws_index:].lstrip()
                        ws_index = 5
                    else:
                        line = line + before_comment[:ws_index]
                        before_comment = ''
                    break
        line = line + before_comment + comment
    else:
        line = before_comment + comment

    return line

def print_lattice(line, p, line_limit, comment):
        dims = []
        indicies = []
        end = len(line)
        iters = finditer(p, line)
        q = 0
        index = 0
        for m in iters:
            q = q+1
            if (q > 3):
                break
            nums = line[m.start():m.end()].replace(':', ' ').split()
            dims.append(1+int(nums[1])-int(nums[0]))
            indicies.append(int(nums[0]))
            end = m.end()

        line_start = line_wrap(line[:end+1], comment, line_limit)
        line_new = line[end+1:len(line)]
        lat = line_new.split()

        if (dims[2] > 1):
            lattice = '\nC    k = ' + str(indicies[2]) + ' (Bottom)\n     '
        else:
            lattice = '\n     '
        for k in range(dims[2]):
            for j in range(dims[1]):
                lat_line = ''
                for i in range(dims[0]):
                    index = i + j*dims[0] + k*dims[0]*dims[1]
                    lat_line = lat_line + lat[index] + ' '
                comment = ('$ i = (' + str(indicies[0]) + ' to ' 
                    + str(indicies[0]+i) + '), j = ' + str(indicies[1]+j))
                lattice = lattice + line_wrap(lat_line, comment, line_limit-5)
                if (j < dims[1]-1):
                    lattice = lattice + '\n     '
            if (k < dims[2]-1):
                    lattice = lattice + '\nC    k = ' + str(indicies[2]+k+1) + '\n     '
        if (len(lat) > index):
            line_end = '\n     ' + line_wrap(' '.join(lat[index+1:]), '', line_limit-5)
            if line_end.strip() == '':
                line_end = ''
            #line_end = line_wrap(line_end, '', line_limit)
        else:
            line_end = ''
        return line_start + lattice + line_end

def print_material(line, p, line_limit, comment):
    iters = finditer(p, line)
    q = 0
    end = len(line)
    line_new = ''
    for m in iters:
        q = q+1
        if (q == 1):
            end = m.start()
        line_new = line_new + line[m.start():m.end()]
        if (line[m.end():].lstrip() != ''):
            line_new = line_new + '\n     '
            
    line_start = line_wrap(line[:end], comment, line_limit)

    if (line_new == ''):
        return line_start
    else:
        return line_start + '\n     ' + line_new

def preprocessor(filename):
    """Removes specific syntax features which parse correctly, but later serialize problematicly.
    """
    #pos_hs = compile(' \+[0-9]')
    sl_comment = compile('[$]')
    #ml_comment = compile('^[C ].*', IGNORECASE)
    ml_comment = compile('^C ', IGNORECASE)
    
    with open(filename, 'r') as input, open('modified_'+filename, 'w') as output:
        deck = input.read().splitlines()
        #end = False
        string = ''
        for line in deck:
            if search(ml_comment, line):
                line = ''
            else:
                if search(sl_comment, line):
                    index = search(sl_comment, line).span()[0]
                    if index != 0:
                        line = line[:index]
                string = string + line + '\n'
        output.write(string)
        
    return 'modified_'+filename


"""8800 60  2.00000E-15      ((-8835  +8602  -8625)                 
                   :(-8817  +8604  +8625  -8630)          
c                   :(-8817  +8630  -8845  +8622  +8624)   
                   :(-8810  +8845  -8846  +8622  +8624)   
                   :(-8803  +8846  -8901  +8622  +8624))  
                   #(8604 -86254 86252 -86253)                     imp:n=1                              
cmesh
c4 """

def deck_cleanup(inp):
    p_cell = compile('\s*\d+\s+\d+')
    p_cont = compile('\s*continue', IGNORECASE)
    p_exp = compile('\d[-\+]\d')
    p_dexp = compile('\dd[-\+]?\d', IGNORECASE)
    new_text = ''
    # Open the file and start the cleanup.
    with open(inp, 'r') as f:
        lines = f.readlines()
        start = False
        # Need to add the $ title.
        if lines[0].startswith('$') is False:
            if lines[0].lower().startswith('continue'):
                new_text += '$ \n' + lines[0]
            else:
                new_text += '$ ' + lines[0]
        else:
            new_text += lines[0]
        
        # A lot of files have extra text after the end of the input.
        # MCNP doesn't care, but the parser sure does.
        # So we delete extraneous blank lines and other 'end' 
        # statements. Comments should be left alone.
        for i in range(len(lines)-1, 1, -1):
            line = lines[i].strip()
            if line == '' or line == 'end of input' or line == 'end':
                lines.pop(i)
            elif line.lower().startswith('c '):
                pass
            else:
                break
        
        # Exponents must have the 'E'.
        for i in range(1, len(lines)):
            exp = findall(p_exp, lines[i])
            dexp = findall(p_dexp, lines[i])
            if (lines[i].lower().startswith('c ') is False 
                and lines[i].startswith('$') is False):
                # Fixes exponents without the 'E'.
                for e in exp:
                    sign = 'E' + e[1]
                    lines[i] = lines[i].replace(e, e[:1]+sign+e[-1])
                # Fixes exponents using 'D' instead of 'E'.
                for d in dexp:
                    lines[i] = lines[i].replace(d, d[0]+'E' +d[2:])
            
            # Some files have title sections that can't be validated.
            # Comment out everything before a cell or continue card.
            # Should fix most files.
            if start is False:
                cell = search(p_cell, lines[i])
                cont = search(p_cont, lines[i])
                if cell is not None or cont is not None:
                    start = True
                    new_text += lines[i]
                elif lines[i].lower().startswith('c '):
                    new_text += lines[i]
                else:
                    new_text += 'C ' + lines[i]
            elif (lines[i].lower().strip().startswith('#ifdef') 
                    or lines[i].lower().strip().startswith('#else')
                    or lines[i].lower().strip().startswith('#endif')):
                    new_text += 'C ' + lines[i]
            else:
                new_text += lines[i]
        
        # Make sure there's at least one blank line at the end.
        if new_text.endswith('\n') is False:
            new_text += '\n'
                
    # Rename with '.mcnp' extension.
    """if inp.endswith('.mcnp') is False:
        new_name = 'cleaned_' + inp + '.mcnp'
    else:
        new_name = 'cleaned_' + inp"""
    new_name = inp + '_cleaned.mcnp'
    
    with open(new_name, 'w') as f:
        f.write(new_text)

    return new_name

def formatter(deck, title=None):
    """Used to serialize the deck as a string. There are currently some spacing issues when making new deck objects.
    Some ad-hoc corrections are made. Will address this later.
    """
    line_limit = 120
    # +/- int, a colon, and another +/- int
    p_lat = compile('-?\d+:-?\d+')
    # A 4-6 digit ZAID, WS, a +/- number with optional exponents
    #p_mat = re.compile('(\d\d\d\d\d?\d?)(\.\d\d\D?)?(\W+)((\+|-)?\d*\.?\d+(e(\+|-)?\d+\.?\d*)?)', re.IGNORECASE)
    p_fill = compile('fill', IGNORECASE)

    # List of characters that should be un-spaced or otherwise changed at every occurance.
    chars = {}
    chars['##'] = ''
    #TODO: Fix TMESH spacing directly in serializer
    tmesh = {}
    tmesh[' CORA '] = '\nCORA'
    tmesh[' CORB '] = '\nCORB'
    tmesh[' CORC '] = '\nCORC'
    tmesh[' RMESH '] = '\nRMESH'
    tmesh[' CMESH '] = '\nCMESH'
    tmesh[' SMESH '] = '\nSMESH'
    tmesh[' ERGSH '] = '\nERGSH'
    tmesh[' MSHMF '] = '\nMSHMF'
    tmesh[' FM '] = '\nFM'
    tmesh[' +FM '] = '\n+FM'

    d = deck.splitlines()
    
    if (d[0].startswith('$') == False):
        if title is None:
            string = '$ This file was written with mcnpy\n'
        elif title.startswith('$'):
            string = title + '\n'
        else:
            string = '$ ' + title + '\n'

    else:
        string = ''
    for line in d:
        tmesh_block = False
        # Removes leading space.
        if (line.startswith('     ') == False):
            line = line.lstrip()
        # Check for $ comment to avoid changing comments.
        index = line.find('$')
        if (index > -1):
            before_comment = line[:index]
            comment = line[index:]
        else:
            before_comment = line
            comment = ''

        # Don't do anything for C comment lines.
        if (before_comment.upper().startswith('C ') == False):# and line.upper().startswith('MODE') == False):
            if before_comment.upper().startswith('TMESH'):
                tmesh_block = True
            # Only replacing '##' right now.
            for k in chars:
                before_comment = before_comment.upper().replace(k, chars[k])
            # Because the serializer epic fails with TMESH...
            if tmesh_block is True:
                for k in tmesh:
                    before_comment = before_comment.upper().replace(k, tmesh[k])
                
            if search(p_fill, before_comment):
                try:
                    line = print_lattice(before_comment, p_lat, line_limit, comment)
                except:
                    line = line_wrap(before_comment, comment, line_limit)
            else:
                line = line_wrap(before_comment, comment, line_limit)
            if tmesh_block is True and 'ENDMD' in before_comment.upper():
                tmesh_block = False

        string = string + line + '\n'
    return string
