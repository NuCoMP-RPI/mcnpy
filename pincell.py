from mcnpy import MaterialNuclide as Nuclide
import mcnpy as mp

deck = mp.Deck()

# Materials
uo2 = [Nuclide('u235', 0.03), Nuclide('u238', 0.97), Nuclide('o16', 2.0)]
h2o = [Nuclide('h1', 2.00), Nuclide('8016', 1.0)]
zr = [Nuclide('zr0', 1.0)]
gas = [Nuclide('h1', 0.5), Nuclide('he4', 0.5)]

fuel = mp.Material('1', uo2)
mod = mp.Material('2', h2o)
clad = mp.Material('3', zr)
gap  = mp.Material('4', gas)
deck.add_all([fuel, mod, clad, gap])

# Surfaces
fuel_outer_radius = mp.ZCylinder(name='1', x0=0, y0=0, r=0.39)
clad_inner_radius = mp.ZCylinder(name='2', x0=0, y0=0, r=0.40)
clad_outer_radius = mp.ZCylinder(name='3', x0=0, y0=0, r=0.46)
pitch = 1.26
bounding_box = mp.RectangularPrism(x0=-pitch/2, x1=pitch/2, y0=-pitch/2, 
                                   y1=pitch/2, z0=-pitch/2, z1=pitch/2, 
                                   boundary_type='reflective', name='4')
deck.add_all([fuel_outer_radius, clad_inner_radius, clad_outer_radius, 
              bounding_box])

# Regions
fuel_region = -fuel_outer_radius & -bounding_box
gap_region = +fuel_outer_radius & -clad_inner_radius & -bounding_box
clad_region = +clad_inner_radius & -clad_outer_radius & -bounding_box
mod_region = +clad_outer_radius & -bounding_box
outside_region = +bounding_box

# Cells
fuel_cell = mp.Cell(name='1', region=fuel_region, density=10.0, material=fuel)
fuel_cell.density_unit = 'g_cm3'
clad_cell = mp.Cell(name='2', region=clad_region, density=-6.6, material=clad)
mod_cell = mp.Cell(name='3', region=mod_region, density=-1.0, material=mod)
gap_cell = mp.Cell(name='4', region=gap_region, density=-1.78e-4, material=gap)
void_cell = mp.Cell(name='5', region=outside_region, material=None)
deck.add_all([fuel_cell, clad_cell, mod_cell, gap_cell, void_cell])

# Cell Importances
particles = ['n']
for k in deck.cells:
    if deck.cells[k] == void_cell:
        deck.cells[k].importances = {0.0 : particles}
    else:
        deck.cells[k].importances = {1.0 : particles}

# Define criticality source
kcode = mp.CriticalitySource(histories=1e4, keff_guess=1.0, skip_cycles=200, 
                             cycles=1200)
src_points = [(0,0,0), (0,0,0.5), (0,0,-0.5)]
ksrc = mp.CriticalitySourcePoints(src_points)
deck.add_all([kcode, ksrc])

# Print MCTAL file
deck.add(mp.PrintDump(print_mctal=1))

print(deck)

# Write to file
deck.write('my_pincell.mcnp')