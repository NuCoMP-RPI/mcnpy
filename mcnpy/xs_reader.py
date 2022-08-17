import h5py as h5
import numpy as np

M_NEUTRON = 1.008664967 #amu

def make_mass_list(xsdir):
    with open(xsdir, 'r') as xs_mcnp:
        xslist = h5.File('masses.h5', 'w')
        grp = xslist.create_group('ZAID')

        lines = xs_mcnp.readlines()
        index = None
        found = -1

        for i in range(len(lines)):
            if found == -1:
                found = lines[i].find('atomic weight ratios')
            else:
                index = i
                break

        zaids = dict()

        for line in lines[index:]:
            # Values should be a ZAID and a mass ratio
            values = line.split()
            # Reached end of atomic weight block.
            if len(values) == 1:
                break
            for i in range(0, len(values), 2):
                zaids[values[i]] = values[i+1]

        for k in zaids:
            grp.create_dataset(name=k, data=np.asarray(zaids[k], dtype='S'))

        xslist.close()

def make_xs_list(xsdir):
    with open(xsdir, 'r') as xs_mcnp:
        xslist = h5.File('xslist.h5', 'w')
        grp = xslist.create_group('ZAID')

        lines = xs_mcnp.readlines()
        index = None
        found = -1

        # Extract the portion of the xsdir file with the isotopes by lib.
        for i in range(len(lines)):
            if (found == -1):
                found = lines[i].find('directory')
            else:
                index = i
                break

        zaids = dict()

        # Extract only the zaids with library extensions.
        # This should be the full list of all possible nuclides.
        for line in lines[index:]:
            zaid_lib = line.split()[0]
            # Checks that the line has a ZAID and not SaB or just text.
            try:
                int(zaid_lib[0])
                zaid = zaid_lib.split('.')[0]
                lib = zaid_lib.split('.')[1]
                if (zaid in zaids):
                    zaids[zaid].append(lib)
                else:
                    zaids[zaid] = [lib]
            except:
                pass

        for k in zaids:
            grp.create_dataset(name=k, data=np.asarray(zaids[k], dtype='S'))

        xslist.close()
