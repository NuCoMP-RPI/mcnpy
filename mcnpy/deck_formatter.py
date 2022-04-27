from re import search, compile, finditer, IGNORECASE

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
    #p_m_id = re.compile('^m\d+', re.IGNORECASE)
    """p_surface_tally = re.compile('^f\d*(1|2)\ \:', re.IGNORECASE)
    p_facet = re.compile('\d*\ \.\d')
    p_f5_axis = re.compile('(f\d*5\s+x\ \:)|(f\d*5\s+y\ \:)|(f\d*5\s+z\ \:)', re.IGNORECASE)
    p_fip = re.compile('^fip\s+\d*5\ \:', re.IGNORECASE)
    p_fir = re.compile('^fir\s+\d*5\ \:', re.IGNORECASE)
    p_tir = re.compile('^tir\s+\d*5\ \:', re.IGNORECASE)
    p_pi = re.compile('^pi\s+\d*5\ \:', re.IGNORECASE)
    p_fic = re.compile('^fic\s+\d*5\ \:', re.IGNORECASE)
    p_tic = re.compile('^tic\s+\d*5\ \:', re.IGNORECASE)
    p_angle_bins = re.compile('^c\s+\d*(0|1|2|4|5|6|7|8)', re.IGNORECASE)
    p_seg_bins = re.compile('^fs\s+\d*(0|1|2|4|5|6|7|8)', re.IGNORECASE)
    p_e_bins = re.compile('^E\s+\d*(0|1|2|4|5|6|7|8)', re.IGNORECASE)
    p_fm = re.compile('^FM\s+\d*(0|1|2|4|5|6|7|8)', re.IGNORECASE)
    p_si = re.compile('^si\s+\d+', re.IGNORECASE)
    p_sp = re.compile('^sp\s+\d+', re.IGNORECASE)
    p_sb = re.compile('^sb\s+\d+', re.IGNORECASE)
    p_ds = re.compile('^ds\s+\d+', re.IGNORECASE)
    p_dist = re.compile('\sd\s\d+', re.IGNORECASE)
    # TODO: Work out why the weird formatting on IMP keywords occurs.
    # Probably need to list out the possible particles.
    p_imp = re.compile('imp:[^0-9.]+', re.IGNORECASE)
    p_imp2 = re.compile('imp : [^0-9.]+', re.IGNORECASE)
    p_r_paren = re.compile('[)]')
    p_l_paren = re.compile('[(]')"""
    #p_imp1 = re.compile('imp\s+\:\s+*{1}', re.IGNORECASE)
    #p_imp2 = re.compile('imp\:*{1}', re.IGNORECASE)

    # List of characters that should be un-spaced or otherwise changed at every occurance.
    old_char = []
    #old_char.append(' . 70   ') # For workaround regarding C lib entensions.
    """old_char.append(' = ')
    old_char.append('- ')
    old_char.append(' ,')
    old_char.append('+ ')
    old_char.append(' : ')
    old_char.append('# ')"""
    old_char.append('##')
    """old_char.append(' . ')
    old_char.append(' NC  ')
    old_char.append(' C  ')
    old_char.append(' D  ')
    old_char.append(' M  ')
    old_char.append(' P  ')
    old_char.append(' U  ')
    old_char.append(' Y  ')
    old_char.append(' E  ')
    old_char.append(' H  ')
    old_char.append(' O  ')
    old_char.append(' R  ')
    old_char.append(' S  ')
    old_char.append(' A  ')
    old_char.append('* TRCL')
    old_char.append('( ')
    old_char.append(' )')
    old_char.append(', ')
    old_char.append(' [')
    old_char.append('[ ')
    old_char.append(' ]')"""
    #old_char.append('] ')

    new_char = []
    #new_char.append('.70C  ') # For workaround regarding C lib entensions.
    """new_char.append('=')
    new_char.append('-')
    new_char.append(',')
    new_char.append('+')
    new_char.append(':')
    new_char.append('#')"""
    new_char.append('')
    """new_char.append('.')
    new_char.append('NC ')
    new_char.append('C ')
    new_char.append('D ')
    new_char.append('M ')
    new_char.append('P ')
    new_char.append('U ')
    new_char.append('Y ')
    new_char.append('E ')
    new_char.append('H ')
    new_char.append('O ')
    new_char.append('R ')
    new_char.append('S ')
    new_char.append('A ')
    new_char.append('*TRCL')
    new_char.append('(')
    new_char.append(')')
    new_char.append(',')
    new_char.append('[')
    new_char.append('[')
    new_char.append(']')"""
    #new_char.append(']')

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
        """if (re.search(p_angle_bins, before_comment)):
            before_comment = before_comment.upper().replace('C ', 'C', 1)
        if (re.search(p_seg_bins, before_comment)):
            before_comment = before_comment.upper().replace('FS ', 'FS', 1)
        if (re.search(p_e_bins, before_comment)):
            before_comment = before_comment.upper().replace('E ', 'E', 1)
        if (re.search(p_fm, before_comment)):
            before_comment = before_comment.upper().replace('FM ', 'FM', 1)
        if (re.search(p_si, before_comment)):
            before_comment = before_comment.upper().replace('SI ', 'SI', 1)
        if (re.search(p_sp, before_comment)):
            before_comment = before_comment.upper().replace('SP ', 'SP', 1)
        if (re.search(p_sb, before_comment)):
            before_comment = before_comment.upper().replace('SB ', 'SB', 1)
        if (re.search(p_ds, before_comment)):
            before_comment = before_comment.upper().replace('DS ', 'DS', 1)
        if (re.search(p_dist, before_comment)):
            before_comment = before_comment.upper().replace('D ', 'D')"""
        # Don't do anything for C comment lines.
        if (before_comment.upper().startswith('C ') == False):# and line.upper().startswith('MODE') == False):
            """# Removes space between M and material ID.
            if (before_comment.upper().startswith('M ')):
                before_comment = before_comment.upper().replace('M ', 'M', 1)
            # Removes space between * and surface ID.
            if (before_comment.startswith('* ')):
                before_comment = before_comment.replace('* ', '*',1)
            # Removes space between F and tally ID.
            if (before_comment.upper().startswith('F ')):
                before_comment = before_comment.upper().replace('F ', 'F', 1)
            if (before_comment.upper().startswith('+ F ')):
                before_comment = before_comment.upper().replace('+ F ', '+F', 1)
            if (before_comment.upper().startswith('+F ')):
                before_comment = before_comment.upper().replace('*F ', '*F', 1)
            if (re.search(p_surface_tally, before_comment)):
                matches = re.findall(p_facet, before_comment)
                #print(matches)
                for m in matches:
                    before_comment = re.sub(m, re.sub(' ', '', m), before_comment)
            if (re.search(p_f5_axis, before_comment)):
                #print('HERE', before_comment, '\n')
                before_comment = before_comment.upper().replace('5 X', '5X', 1).replace('5 Y', '5Y', 1).replace('5 Z', '5Z', 1)
            if (re.search(p_fip, before_comment)):
                before_comment = before_comment.upper().replace('P ', 'P', 1)
            if (re.search(p_pi, before_comment)):
                before_comment = before_comment.upper().replace('PI ', 'FIP', 1)
            if (re.search(p_fir, before_comment) or re.search(p_tir, before_comment)):
                before_comment = before_comment.upper().replace('R ', 'R', 1).replace('T', 'F', 1)
            if (re.search(p_fic, before_comment) or re.search(p_tic, before_comment)):
                before_comment = before_comment.upper().replace('C ', 'C', 1).replace('T', 'F', 1)
            # Will need to update this one for supporting comments
            if (before_comment.upper().startswith('MT ')):
                before_comment = before_comment.upper().replace('MT ', 'MT', 1).replace('U-O2', ' U/O2', 1).replace('O2-U', ' O2/U', 1).replace(' T ', 'T ')
            if (line.upper().startswith('TR ') or before_comment.upper().startswith('*TR ')):
                before_comment = before_comment.upper().replace('TR ', 'TR', 1).replace('(', '').replace(')', '')"""

            # Only replacing '##' right now.
            for j in range(len(old_char)):
                before_comment = before_comment.upper().replace(old_char[j], new_char[j])
            # Fix IMP keywords.
            """if (re.search(p_imp, before_comment)):
                match = re.search(p_imp, before_comment).group()
                before_comment = before_comment.upper().replace(match, match+' ')
            if (re.search(p_imp2, before_comment)):
                match = re.search(p_imp2, before_comment).group()
                before_comment = before_comment.upper().replace(match, match+' ')
            if (re.search(p_r_paren, before_comment) is True and re.search(p_l_paren, before_comment) is False):
                match = re.search(p_r_paren, before_comment).group()
                before_comment = before_comment.upper().replace(match, match+' ')"""
                
            if search(p_fill, before_comment):
                try:
                    line = print_lattice(before_comment, p_lat, line_limit, comment)
                except:
                    line = line_wrap(before_comment, comment, line_limit)
            else:
                line = line_wrap(before_comment, comment, line_limit)
            """elif re.search(p_m_id, before_comment):
                try:
                    line = print_material(before_comment, p_mat, line_limit, comment)
                except:
                    line = line_wrap(before_comment, comment, line_limit)
            else:
                line = line_wrap(before_comment, comment, line_limit)"""
        string = string + line + '\n'
    return string
