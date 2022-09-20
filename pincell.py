import mcnpy as mp
from mcnpy.elements import *

deck = mp.Deck()

# Materials
enr = 3
u_enr = U[238]%(100-enr) + U[235]%enr
fuel = mp.Material(u_enr + O[16]@2)
# Include S(a,B). Normally added as a separate card in MCNP.
fuel.s_alpha_beta = ['o_in_uo2', 'u238_in_uo2']

mod = mp.Material(H[1]@2 + O)
mod.s_alpha_beta = 'lwtr'

solutes = {SN: 1.5, FE: 0.2, CR: 0.1}
zirc4 = ZR%(100-sum(solutes.values()))
for sol in solutes:
    zirc4 += sol%solutes[sol]
clad = mp.Material(zirc4)

gap = mp.Material(H[1]@0.5 + HE[4]@0.5)

deck += [fuel, mod, clad, gap]

fuel_outer_radius = mp.ZCylinder(name=1, x0=0, y0=0, r=0.39)
clad_inner_radius = mp.ZCylinder(name=2, x0=0, y0=0, r=0.40)
clad_outer_radius = mp.ZCylinder(name=3, x0=0, y0=0, r=0.46)
pitch = 1.26
bounding_box = mp.RectangularPrism(x0=-pitch/2, x1=pitch/2, y0=-pitch/2, 
                                   y1=pitch/2, z0=-pitch/2, z1=pitch/2, 
                                   boundary_type='reflective', name=4)
deck += [fuel_outer_radius, clad_inner_radius, clad_outer_radius, 
         bounding_box]

fuel_region = -fuel_outer_radius & -bounding_box
gap_region = +fuel_outer_radius & -clad_inner_radius & -bounding_box
clad_region = +clad_inner_radius & -clad_outer_radius & -bounding_box
mod_region = +clad_outer_radius & -bounding_box
outside_region = +bounding_box

fuel_cell = mp.Cell(1, fuel_region, fuel*10.0)
clad_cell = mp.Cell(2, clad_region, clad*6.6)
mod_cell = mp.Cell(3, mod_region, mod*1.0)
gap_cell = mp.Cell(4, gap_region, gap*1.78e-4)
void_cell = mp.Cell(5, outside_region, None)
deck += [fuel_cell, clad_cell, mod_cell, gap_cell, void_cell]

for cell in deck.cells.values():
    if cell.material is None:
        cell.importances = {'n' : 0.0}
    else:
        cell.importances = {'n' : 1.0}

deck += mp.CriticalitySource(histories=1e2, keff_guess=1.0, skip_cycles=100, 
                             cycles=300)
deck += mp.CriticalitySourcePoints([(0,0,0), (0,0,0.5), (0,0,-0.5)])

# Print MCTAL file
deck += mp.PrintDump(print_mctal=1)

print(deck)

# Write to file
deck.write('my_pincell.mcnp')

mp.run_mcnp('my_pincell.mcnp')