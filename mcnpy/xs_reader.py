import h5py as h5
import numpy as np

xsdir = open('xsdir_mcnp6.2', 'r')
xslist = h5.File('xslist.h5', 'w')
grp = xslist.create_group('ZAID')
#xslist = open('xslist', 'w')

lines = xsdir.readlines()
lines_new = []

index = None
found = -1

# Extract the portion of the xsdir file with the isotopes by lib.
for i in range(len(lines)):
    if (found == -1):
        found = lines[i].find('directory')
    else:
        index = i
        break

lines_new = lines[index:]

zaids = dict()

# Extract only the zaids with library extensions.
# This should be the full list of all possible nuclides.
for i in range(len(lines_new)):
    zaid_lib = lines_new[i].split()[0]
    # Checks that the line has a ZAID and not SaB or just text.
    try:
        a = int(zaid_lib[0])
        zaid = zaid_lib.split('.')[0]
        lib = zaid_lib.split('.')[1]
        if (zaid in zaids):
            zaids[zaid].append(lib)
        else:
            zaids[zaid] = [lib]
    except:
        a = None

for k in zaids:
    grp.create_dataset(name=k, data=np.asarray(zaids[k], dtype='S'))

xslist.close()
xsdir.close()
