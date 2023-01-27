class Pincell():
    """A simple pin-cell model

    Parameters
    ----------
    filename : str, optional
        Name of file to be written.

    Attributes
    ----------
    filename : str
        Name of file to be written.
    deck : mcnp.Deck
        The MCNP model object.
    """

    def __init__(self, filename='pincell.mcnp'):
        """A simple pin-cell model"""

        import mcnpy as mp
        from mcnpy.elements import U, O, H, SN, FE, CR, ZR, HE

        self.filename = filename
        self.title = 'Pin-Cell example from MCNPy'
        self.deck = mp.Deck()

        # Materials
        enr = 3
        u_enr = U[238]%(100-enr) + U[235]%enr
        fuel = mp.Material(u_enr + O[16]@2)
        # Include S(a,B). Normally added as a separate card in MCNP.
        fuel.s_alpha_beta = ['o_in_uo2', 'u238_in_uo2']

        mod = mp.Material(H[1]@2 + O[16])
        mod.s_alpha_beta = 'lwtr'

        solutes = {SN: 1.5, FE: 0.2, CR: 0.1}
        zirc4 = ZR%(100-sum(solutes.values()))
        for sol in solutes:
            zirc4 += sol%solutes[sol]
        clad = mp.Material(zirc4)

        gap = mp.Material(H[1]@0.5 + HE[4]@0.5)

        self.deck += [fuel, mod, clad, gap]

        # Surfaces
        fuel_outer_radius = mp.ZCylinder(name=1, x0=0, y0=0, r=0.39)
        clad_inner_radius = mp.ZCylinder(name=2, x0=0, y0=0, r=0.40)
        clad_outer_radius = mp.ZCylinder(name=3, x0=0, y0=0, r=0.46)
        pitch = 1.26
        bounding_box = mp.RectangularPrism(x0=-pitch/2, x1=pitch/2, y0=-pitch/2, 
                                        y1=pitch/2, z0=-pitch/2, z1=pitch/2, 
                                        boundary_type='reflective', name=4)
        self.deck += [fuel_outer_radius, clad_inner_radius, clad_outer_radius, 
                     bounding_box]

        # Regions
        fuel_region = -fuel_outer_radius & -bounding_box
        gap_region = +fuel_outer_radius & -clad_inner_radius & -bounding_box
        clad_region = +clad_inner_radius & -clad_outer_radius & -bounding_box
        mod_region = +clad_outer_radius & -bounding_box
        outside_region = +bounding_box

        # Cells
        fuel_cell = mp.Cell(1, fuel_region, fuel*10.0)
        clad_cell = mp.Cell(2, clad_region, clad*6.6)
        mod_cell = mp.Cell(3, mod_region, mod*1.0)
        gap_cell = mp.Cell(4, gap_region, gap*1.78e-4)
        void_cell = mp.Cell(5, outside_region, None)
        self.deck += [fuel_cell, clad_cell, mod_cell, gap_cell, void_cell]

        for cell in self.deck.cells.values():
            if cell.material is None:
                cell.importances = {mp.Particle.NEUTRON : 0.0}
            else:
                cell.importances = {mp.Particle.NEUTRON : 1.0}

        # Source
        self.deck += mp.CriticalitySource(histories=1e4, keff_guess=1.0, 
                                          skip_cycles=100, cycles=300)
        self.deck += mp.CriticalitySourcePoints([(0,0,0), (0,0,0.5), (0,0,-0.5)])

        # Print MCTAL file
        self.deck += mp.PrintDump(print_mctal=1)

    def write(self):
        """Write the model to file.
        """
        self.deck.write(self.filename, self.title)

class RCF():
    """A full core model of RPI's Reactor Critical Facility. A very critical reactor that will live on in the virtual world no matter what Shirley and the RPI administration does. This example will generate a new MCNP deck, build the RCF, and write the model to file.`water` sets the height of the water in the reactor in inches (default is `68.0in`). `bank` sets the control rod bank height in inches (default is rods fully bottomed at `0.0in`). `sporty` when set to `True` removes the center fuel pin which puts the RCF in sport mode. `filename` specifies the name of the new MCNP input (default is `./rcf_full_api.mcnp`). The model can be accessed with the `deck` attribute.

    Parameters
    ----------
    filename : str, optional
        Name of file to be written.
    water : float, optional
        RCF water height in inches.
    bank : float, optional
        RCF control rod bank height in inches.
    sporty: boolean, optional
        Whether or not sport mode is engaged.

    Attributes
    ----------
    filename : str
        Name of file to be written.
    water : float
        RCF water height in inches.
    bank : float
        RCF control rod bank height in inches.
    sporty: boolean
        Whether or not sport mode is engaged.
    deck : mcnp.Deck
        The MCNP model object.
    """
    def __init__(self, filename='rcf_full_api.mcnp', 
                 water=68.0, bank=0.0, sporty=False):
        """A full core model of RPI's Reactor Critical Facility. A very 
        critical reactor that will live on in the virtual world no matter what 
        Shirley and the RPI administration does. This example will generate a 
        new MCNP deck, build the RCF, and write the model to file.`water` sets 
        the height of the water in the reactor in inches (default is `68.0in`).
        `bank` sets the control rod bank height in inches (default is rods 
        fully bottomed at `0.0in`). `sporty` when set to `True` removes the 
        center fuel pin which puts the RCF in sport mode. `filename` specifies 
        the name of the new MCNP input (default is 
        `./rcf_full_api.mcnp`). The model can be accessed with the 
        `deck` attribute.
        """
        import numpy as np
        from mcnpy import Cell, Deck, Lattice, Point, UniverseList
        from mcnpy import Transform, Transformation
        from mcnpy import Material
        from mcnpy import CriticalitySource, CriticalitySourcePoints
        from mcnpy import CircularCylinder as RCC
        from mcnpy import RectangularPrism as RPP
        from mcnpy import Plane, PPoints
        from mcnpy.elements import U, O, FE, CR, NI, MN, AL, H, HE, C, N, AR, MO, CU, CO, B

        """
        A. Pin Anatomy (bottom to top):
            1. Bottom of pin (small extrusion sticking into bottom plate)
            2. Bottom plug
            3. Bottom spacer
            4. Fuel
            5. Insulator
            6. Top spacer
            7. Spring
            8. Top plug
            9. Top of pin (part you hook to remove pin)
            10. Cladding extends between the top and bottom plugs
        B. Other Pin Cell Features:
            1. Support plate (below entire pin)
            2. Top plate (upper plate with holes)
            3. Moderator (everywhere a pin or plate is not)
        """

        """These 2 values allow you to control the water height and to raise 
        rods as a bank. The real world RCF limits are 36in rod height and 
        68in water height. For the model, any positive rod height should work. 
        Water height should not be above the top of the tank.
        """
        self.filename=filename
        self.water = water
        self.bank = bank
        self.sporty = sporty
        # This is the number read from the control panel.
        # Change this to adjust rod position.
        bank_height = bank*2.54
        # Set to max 68in height.
        water_height = water*2.54
        # Activate 'sport mode' by removing the center pin.

        # Dimensions
        # Lattice is 21x21 elements.
        num_el = 21 
        el_height = 171.78
        # 1/2 0.64" square lattice pitch.
        el_width = 0.8128 
        lat_width = num_el*el_width
        sup_plate_width = 82.56
        lat_plate_width = 66.04

        sup_plate_bottom = 39.05
        sup_plate_top = 43.82
        sup_plate_hole_r = 0.3175
        pin_bottom_r = 0.3137
        pin_hole_h = 1.27
        bottom_plug_h = 0.91
        spacer_h = 0.32
        fuel_h = 91.44
        spring_h = 5.08
        top_plug_h = 1.9
        pin_top_h = 3.18
        clad_or = 0.59128
        clad_ir = 0.54102
        clad_h = 99.38
        fuel_or = 0.5334
        top_plate_hole_r = 0.635
        top_plate_bottom = 145.1
        pin_top_water_h = 2.19
        tank_h = 7.0*12.0*2.54
        tank_ir = 0.5*tank_h
        top_sup_plate_t = 3.18
        top_sup_plate_r = 46.6725 
        post_r = 3.01625
        post_pos = 29.69
        # A default moderator H2O desnity.
        density_mod = 0.998113 # g/cc
        # A default SS density.
        density_ss = 8.0 # g/cc
        # A default air density.
        density_air = 0.001205 # g/cc
        density_fill_gas = 1.78e-04 # g/cc
        density_spring = 1.0 # g/cc

        # Rounding to avoid floating point errors.
        # This is safe to do since max precision is known.
        top_plate_top = np.round(top_plate_bottom+pin_hole_h, 13)
        bottom_plug_base = np.round(sup_plate_top+pin_hole_h, 13)
        bottom_spacer_base = np.round(bottom_plug_base+bottom_plug_h, 13)
        fuel_base = np.round(bottom_spacer_base+spacer_h, 13)
        insulator_base = np.round(fuel_base+fuel_h, 13)
        top_spacer_base = np.round(insulator_base+spacer_h, 13)
        spring_base = np.round(top_spacer_base+spacer_h, 13)
        top_plug_base = np.round(spring_base+spring_h, 13)
        pin_top_base = np.round(top_plug_base+top_plug_h, 13)
        pin_top_top = np.round(pin_top_base+pin_top_h, 13)
        pin_top_water_base = np.round(pin_top_top-pin_top_water_h, 13)

        # Control rods.
        # Modeling with bottomed meaning the brake is inserted into sup plate.
        # The square section of the rod would appear flush with lattice plate.
        bottomed_h = bottom_plug_base
        rod_position = np.round(bottomed_h+bank_height, 13)
        brake_h = 13.5
        brake_r = 3.2
        guide_tube_r = 1.27
        abs_h = 52.8638
        boron1_bottom = np.round(rod_position+2.405, 13)
        boron1_top = np.round(boron1_bottom+abs_h, 13)
        boron2_bottom = np.round(boron1_top+3.81, 13)
        boron2_top = np.round(boron2_bottom+abs_h, 13)
        follower_pos = np.round(rod_position-brake_h, 13)
        rod_inner = 2.91846
        rod_outer = 3.54584
        abs_inner = 3.00228
        abs_outer = 3.23088
        channel_width = 3.75

        # Create a new deck object.
        inp = Deck()
        self.deck = inp

        # Boundary surfaces
        tank = RCC(comment='Tank - Inside',
                   base=Point(0,0,0),
                   axis=Point(0,0,tank_h),
                   r=tank_ir)
        tank_outside = RCC(comment='Tank - Outside',
                           base=Point(0,0,0),
                           axis=Point(0,0,tank_h),
                           r=tank_ir+1.0)
        tank_bottom = RCC(comment='Tank - Bottom',
                          base=Point(0,0,-1),
                          axis=Point(0,0,1),
                          r=tank_ir+1.0)
        fill_height = Plane(comment='Water Fill Height',
                            a=0, b=0, c=1, d=water_height)
        tank_top = Plane(comment='Tank - Top',
                         a=0, b=0, c=1, d=tank_h)
        bottom_plate = RPP(comment='Bottom Sup. Plate',
                          x0=-0.5*sup_plate_width, x1=0.5*sup_plate_width, 
                          y0=-0.5*sup_plate_width, y1=0.5*sup_plate_width, 
                          z0=sup_plate_bottom, z1=sup_plate_top)
        # Planes for making bottom plate an octagon.
        plate_plane1 = PPoints(comment='Bottom Sup. Plate',
                               points=[Point(25.4,41.28,0.0), 
                               Point(25.4,41.28,25.4),
                               Point(41.28,25.4,0.0)])
        plate_plane2 = PPoints(comment='Bottom Sup. Plate',
                               points=[Point(-25.4,41.28,0.0),
                               Point(-25.4,41.28,25.4),
                               Point(-41.28,25.4,0.0)])
        plate_plane3 = PPoints(comment='Bottom Sup. Plate',
                               points=[Point(-41.28,-25.4,0.0),
                              Point(-41.28,-25.4,25.4),
                              Point(-25.4,-41.28,0.0)])
        plate_plane4 = PPoints(comment='Bottom Sup. Plate',
                               points=[Point(25.4,-41.28,0.0),
                               Point(25.4,-41.28,25.4),
                               Point(41.28,-25.4,0.0)])
        # Cutouts and top support plate surfaces.
        top_sup_plate1 = RPP(comment='Top Sup. Plate',
                             x0=-33.8, x1=33.8,
                             y0=-11.4, y1=11.4,
                             z0=top_plate_bottom-top_sup_plate_t, 
                             z1=top_plate_bottom)
        top_sup_plate2 = RPP(comment='Top Sup. Plate',
                             x0=-26.4, x1=26.4,
                             y0=-26.4, y1=26.4,
                             z0=top_plate_bottom-top_sup_plate_t, 
                             z1=top_plate_bottom)
        top_sup_plate3 = RPP(comment='Top Sup. Plate',
                             x0=-11.4, x1=11.4,
                             y0=-33.8, y1=33.8,
                             z0=top_plate_bottom-top_sup_plate_t, 
                             z1=top_plate_bottom)
        top_sup_plate4 = RCC(comment='Top Sup. Plate',
                             base=Point(0,0,top_plate_bottom-top_sup_plate_t),
                             axis=Point(0,0,top_sup_plate_t),
                             r=top_sup_plate_r)
        # Mid support plate
        mid_sup_plate1 = RPP(comment='Mid Sup. Plate',
                             x0=-33.02, x1=33.02,
                             y0=-33.02, y1=33.02,
                             z0=96.84, z1=96.84+1.27)
        mid_sup_plate2 = RPP(comment='Mid Sup. Plate',
                             x0=-26.67, x1=26.67,
                             y0=-26.67, y1=26.67,
                             z0=96.84, z1=96.84+1.27)
        # Support posts.
        post1 = RCC(comment='Sup. Post',
                    base=Point(post_pos,post_pos,0),
                    axis=Point(0,0,top_plate_bottom-top_sup_plate_t),
                    r=post_r)
        post2 = RCC(comment='Sup. Post',
                    base=Point(-post_pos,post_pos,0),
                    axis=Point(0,0,top_plate_bottom-top_sup_plate_t),
                    r=post_r)
        post3 = RCC(comment='Sup. Post',
                    base=Point(-post_pos,-post_pos,0),
                    axis=Point(0,0,top_plate_bottom-top_sup_plate_t),
                    r=post_r)
        post4 = RCC(comment='Sup. Post',
                    base=Point(post_pos,-post_pos,0),
                    axis=Point(0,0,top_plate_bottom-top_sup_plate_t),
                    r=post_r)
        # Air region extending 20cm beyond top and sides of tank.
        outside = RCC(comment='Outside Air',
                      base=Point(0,0,-1),
                      axis=Point(0,0,tank_h+1.0+20.0),
                      r=tank_ir+1.0+20.0)

        lat_container = RPP(comment='Lattice Container',
                            x0=-lat_width, x1=lat_width, 
                            y0=-lat_width, y1=lat_width, 
                            z0=0.00, z1=el_height)
        lat_element = RPP(comment='Lattice Element',
                          x0=-el_width, x1=el_width, 
                          y0=-el_width, y1=el_width, 
                          z0=0.00, z1=el_height)
        pin_fill = RPP(comment='Pincell Fill',
                       x0=-1, x1=1, 
                       y0=-1, y1=1, 
                       z0=-1, z1=175)

        # Control Rod Surfaces.
        rod_clad_inner = RPP(comment='Control Rod - Cladding',
                             x0=-rod_inner, x1=rod_inner, 
                             y0=-rod_inner, y1=rod_inner, 
                             z0=rod_position, z1=boron2_top)
        rod_clad_outer = RPP(comment='Control Rod - Cladding',
                             x0=-rod_outer, x1=rod_outer, 
                             y0=-rod_outer, y1=rod_outer, 
                             z0=rod_position, z1=boron2_top+2.0)
        abs1_inner = RPP(comment='Control Rod - Lower Absorber',
                         x0=-abs_inner, x1=abs_inner, 
                         y0=-abs_inner, y1=abs_inner, 
                         z0=boron1_bottom, z1=boron1_top)
        abs2_inner = RPP(comment='Control Rod - Upper Absorber',
                         x0=-abs_inner, x1=abs_inner, 
                         y0=-abs_inner, y1=abs_inner, 
                         z0=boron2_bottom, z1=boron2_top)
        abs1_outer = RPP(comment='Control Rod - Lower Absorber',
                         x0=-abs_outer, x1=abs_outer, 
                         y0=-abs_outer, y1=abs_outer, 
                         z0=boron1_bottom, z1=boron1_top)
        abs2_outer = RPP(comment='Control Rod - Upper Absorber',
                         x0=-abs_outer, x1=abs_outer, 
                         y0=-abs_outer, y1=abs_outer, 
                         z0=boron2_bottom, z1=boron2_top)
        # Brake is fully in water or air.
        if brake_h+follower_pos < water_height or follower_pos > water_height:
            brake = RCC(comment='Control Rod - Brake',
                        base=Point(0,0,follower_pos),
                        axis=Point(0,0,brake_h),
                        r=brake_r)
            inp += brake
        # Brake is partially submerged, two cells required.
        else:
            brake1 = RCC(comment='Control Rod - Brake in water',
                         base=Point(0,0,follower_pos),
                         axis=Point(0,0,water_height-follower_pos),
                         r=brake_r)
            brake2 = RCC(comment='Control Rod - Brake in air',
                         base=Point(0,0,water_height),
                         axis=Point(0,0,brake_h-(water_height-follower_pos)),
                         r=brake_r)
            inp += [brake1, brake2]
        
        # Extends from the brake to bottom of tank.
        follower = RCC(comment='Control Rod - Follower',
                     base=Point(0,0,follower_pos),
                     axis=Point(0,0,-follower_pos),
                     r=guide_tube_r)
        # Extends through all structures.
        channel1 = RPP(comment='Control Rod 7 - Channel',
                       x0=-channel_width+22.38, x1=channel_width+22.38,
                       y0=-channel_width, y1=channel_width,
                       z0=0, z1=tank_h)
        channel2 = RPP(comment='Control Rod 4 - Channel',
                       x0=-channel_width-22.38, x1=channel_width-22.38,
                       y0=-channel_width, y1=channel_width,
                       z0=0, z1=tank_h) 
        channel3 = RPP(comment='Control Rod 5 - Channel',
                       x0=-channel_width, x1=channel_width,
                       y0=-channel_width+22.38, y1=channel_width+22.38,
                       z0=0, z1=tank_h) 
        channel4 = RPP(comment='Control Rod 3 - Channel',
                       x0=-channel_width, x1=channel_width,
                       y0=-channel_width-22.38, y1=channel_width-22.38,
                       z0=0, z1=tank_h) 
        channel = RPP(comment='Control Rod - Channel Fill',
                      x0=-2*tank_ir, x1=2*tank_ir,
                      y0=-2*tank_ir, y1=2*tank_ir,
                      z0=-1, z1=tank_h+1) 

        inp += [rod_clad_inner, rod_clad_outer, abs1_inner, abs1_outer,   
                abs2_inner, abs2_outer, follower, channel1, 
                channel2, channel3, channel4, channel]

        # Lattice element surfaces
        #if sup_plate_bottom > water_height or water_height > sup_plate_top:
        sup_plate = RPP(comment='No Pin - Lower Sup. Plate',
                        x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                        y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                        z0=sup_plate_bottom, z1=sup_plate_top)
        inp += sup_plate
        if sup_plate_bottom < water_height and water_height < sup_plate_top:
            sup_plate_a = RPP(comment='No Pin - Lower Sup. Plate, water',
                              x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                              y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                              z0=sup_plate_bottom, z1=water_height)
            sup_plate_b = RPP(comment='No Pin - Lower Sup. Plate, air',
                              x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                              y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                              z0=water_height, z1=sup_plate_top)
            inp += [sup_plate_a, sup_plate_b]
        sup_plate2 = RPP(comment='No Pin - Lower Lat. Plate',
                         x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                         y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                         z0=sup_plate_top, z1=bottom_plug_base)
        pin_bottom = RCC(comment='Pin - Bottom',
                         base=Point(0,0,sup_plate_top), 
                         axis=Point(0,0,pin_hole_h), 
                         r=pin_bottom_r)
        pin_bottom_hole = RCC(comment='Pin - Bottom Hole',
                              base=Point(0,0,sup_plate_top), 
                              axis=Point(0,0,pin_hole_h), 
                              r=sup_plate_hole_r)
        bottom_plug = RCC(comment='Pin - Bottom Plug',
                          base=Point(0,0,bottom_plug_base), 
                          axis=Point(0,0,bottom_plug_h), 
                          r=clad_or)
        bottom_spacer = RCC(comment='Pin - Bottom Spacer',
                            base=Point(0,0,bottom_spacer_base), 
                            axis=Point(0,0,spacer_h), 
                            r=clad_ir)
        fuel = RCC(comment='Pin - Fuel',
                   base=Point(0,0,fuel_base), 
                   axis=Point(0,0,fuel_h), 
                   r=fuel_or)
        insulator = RCC(comment='Pin - Insulator',
                        base=Point(0,0,insulator_base), 
                        axis=Point(0,0,spacer_h), 
                        r=clad_ir)
        top_spacer = RCC(comment='Pin - Top Spacer',
                         base=Point(0,0,top_spacer_base), 
                         axis=Point(0,0,spacer_h), 
                         r=clad_ir)
        spring = RCC(comment='Pin - Spring',
                     base=Point(0,0,spring_base), 
                     axis=Point(0,0,spring_h), 
                     r=clad_ir)
        top_plug = RCC(comment='Pin - Top Plug',
                       base=Point(0,0,top_plug_base), 
                       axis=Point(0,0,top_plug_h), 
                       r=clad_ir)
        if pin_top_base > water_height or water_height > pin_top_base+pin_top_h:
            pin_top = RCC(comment='Pin - Top',
                        base=Point(0,0,pin_top_base), 
                        axis=Point(0,0,pin_top_h), 
                        r=clad_or)
            inp += pin_top
        else:
            pin_top1 = RCC(comment='Pin - Top',
                        base=Point(0,0,pin_top_base), 
                        axis=Point(0,0,water_height-pin_top_base), 
                        r=clad_or)
            pin_top2 = RCC(comment='Pin - Top',
                        base=Point(0,0,water_height), 
                        axis=Point(0,0,pin_top_h+pin_top_base-water_height), 
                        r=clad_or)
            inp += [pin_top1, pin_top2]
        clad_inner = RCC(comment='Pin - Cladding',
                         base=Point(0,0,bottom_spacer_base), 
                         axis=Point(0,0,clad_h), 
                         r=clad_ir)
        clad_outer = RCC(comment='Pin - Cladding',
                         base=Point(0,0,bottom_spacer_base), 
                         axis=Point(0,0,clad_h), 
                         r=clad_or)
        gap = RCC(comment='Pin - Gap',
                  base=Point(0,0,fuel_base), 
                  axis=Point(0,0,fuel_h), 
                  r=clad_ir)
        top_plate = RPP(comment='Pin - Top Lat. Plate',
                        x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                        y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                        z0=top_plate_bottom, z1=top_plate_top)
        top_plate_hole = RCC(comment='Pin - Top Lat. Plate Hole',
                             base=Point(0,0,top_plate_bottom), 
                             axis=Point(0,0,pin_hole_h), 
                             r=top_plate_hole_r)
        pin_top_water = RCC(comment='Pin - Top Water',
                            base=Point(0,0,pin_top_water_base), 
                            axis=Point(0,0,pin_top_water_h), 
                            r=clad_or)
        top_plate_hole_water = RCC(comment='Pin - Top Hole Water',
                                   base=Point(0,0,top_plate_bottom), 
                                   axis=Point(0,0,pin_hole_h), 
                                   r=clad_or)

        # Add surfaces to deck.
        inp += [outside, tank, tank_bottom, tank_outside, fill_height, 
                bottom_plate, pin_fill, tank_top, lat_container,
                lat_element, sup_plate2, pin_bottom,
                pin_bottom_hole, bottom_plug, bottom_spacer, spring, 
                top_plug, clad_inner, clad_outer, gap, top_plate, 
                top_plate_hole, pin_top_water, top_plate_hole_water, fuel, 
                insulator, top_spacer, plate_plane1, plate_plane2, 
                plate_plane3, plate_plane4, top_sup_plate1, top_sup_plate2,
                top_sup_plate3, top_sup_plate4, mid_sup_plate1,
                mid_sup_plate2, post1, post2, post3, post4]

        # Create materials.
        h2o = H[1]@2 + O[16]@1
        mod = Material(h2o)
        mod.comment = 'Light Water Moderator'
        mod.s_alpha_beta = 'lwtr'

        uo2 = Material(U[233]*0.0000035168 + U[234]*0.000222438 
                       + U[235]*0.042263144 + U[236]*0.000411466 
                       + U[238]*0.836299436 + O[16]*0.1208)
        uo2.comment = 'UO2 Fuel'
        uo2.s_alpha_beta = ['o_in_uo2', 'u238_in_uo2']
        
        stainless_steel = FE[56]@0.965 + CR[52]@0.19 + NI[58]@0.095 + MN[55]@0.02
        ss = Material(stainless_steel)
        ss.comment = 'Stainless Steel'

        al203 = Material(AL[27]@0.4 + O[16]@0.6)
        al203.comment = 'Al203 Spacers'

        fill_gas = H[1]@0.5 + HE[4]@0.5
        gas = Material(fill_gas)
        gas.comment = 'Gas Plenum'

        air_mix = C%0.0124 + N[14]%75.5268 + O[16]%23.1781 + AR%1.2827
        air = Material(air_mix)
        air.comment = 'Air'



        # ~0.84 SS
        #TODO: Not 100% clear on why this section has always been homogenized.
        frac_ss = 0.84
        frac_other = 1 - frac_ss
        if sup_plate_bottom > water_height or water_height > sup_plate_top:
            # Submerged
            if sup_plate_bottom > water_height:
                density_bottom_plate = (frac_other*density_mod 
                                        + frac_ss*density_ss)
                ss_bottom_plate = Material(stainless_steel@frac_ss 
                                           + h2o@frac_other)
                # If there's water, then we can add S(a,B)
                ss_bottom_plate.s_alpha_beta = 'lwtr'
            # Unsubmerged
            else:
                density_bottom_plate = (frac_other*density_air 
                                        + frac_ss*density_ss)
                ss_bottom_plate = Material(stainless_steel@frac_ss 
                                           + air_mix@frac_other)
            ss_bottom_plate.comment = 'Bottom Sup. Plate (~.84 SS)'
            inp += ss_bottom_plate
        else:
            ss_bottom_plate1 = Material(stainless_steel@frac_ss + h2o@frac_other)
            ss_bottom_plate1.comment = ('Bottom Sup. Plate Submerged, homog.')
            ss_bottom_plate1.s_alpha_beta = 'lwtr'
            density_bottom_plate1 = frac_other*density_mod + frac_ss*density_ss

            ss_bottom_plate2 = Material(stainless_steel@frac_ss 
                                        + air_mix@frac_other)
            ss_bottom_plate2.comment = ('Bottom Sup. Plate Unsubmerged, homog.')
            density_bottom_plate2 = frac_other*density_air + frac_ss*density_ss
            inp += [ss_bottom_plate1, ss_bottom_plate2]

        # ~0.674 SS
        frac_ss = 0.674
        frac_other = 1 - frac_ss
        if pin_top_base > water_height or water_height > pin_top_base+pin_top_h:
            # Submerged
            if pin_top_base > water_height:
                density_pin_top = (frac_other*density_mod 
                                        + frac_ss*density_ss)
                ss_pin_top = Material(stainless_steel@frac_ss 
                                           + h2o@frac_other)
                # If there's water, then we can add S(a,B)
                ss_pin_top.s_alpha_beta = 'lwtr'
            # Unsubmerged
            else:
                density_pin_top = (frac_other*density_air 
                                        + frac_ss*density_ss)
                ss_pin_top = Material(stainless_steel@frac_ss 
                                           + air_mix@frac_other)
            ss_pin_top.comment = 'Pin - Top (~.674 SS)'
            inp += ss_pin_top
        else:
            ss_pin_top1 = Material(stainless_steel@frac_ss + h2o@frac_other)
            ss_pin_top1.comment = ('Bottom Sup. Plate Submerged, homog.')
            ss_pin_top1.s_alpha_beta = 'lwtr'
            density_pin_top1 = frac_other*density_mod + frac_ss*density_ss

            ss_pin_top2 = Material(stainless_steel@frac_ss 
                                        + air_mix@frac_other)
            ss_pin_top2.comment = ('Bottom Sup. Plate Unsubmerged, homog.')
            density_pin_top2 = frac_other*density_air + frac_ss*density_ss
            inp += [ss_pin_top1, ss_pin_top2]

        # ~0.125 SS
        frac_ss = (density_spring - density_fill_gas) / (density_ss 
                                                         - density_fill_gas)
        frac_other = 1 - frac_ss

        ss_spring = Material(stainless_steel@frac_ss + fill_gas@frac_other)
        ss_spring.comment = 'Spring (~.674 SS)'

        cladding_comp = {}
        cladding_comp[FE] = {54: 0.041105547, 56:0.64526918, 57: 0.014902079, 
                             58: 0.001983193}
        cladding_comp[CR] = {50: 0.0080817, 52: 0.15584754, 53: 0.01767186, 
                             54: 0.0043989}
        cladding_comp[NI] = {58: 0.065081612, 60: 0.025069188, 61: 0.00108984, 
                             62: 0.003474104, 64: 0.000885256}
        cladding_comp[MO] = {92: 0.0002968, 94: 0.000185, 95: 0.0003184, 
                             96: 0.0003336, 97: 0.000191, 98: 0.0004826,
                             100: 0.0001926}
        cladding_comp[CU] = {63: 0.00117589, 65: 0.00052411}
        cladding_comp[CO] = {59: 0.00084}
        cladding_comp[MN] = {55: 0.0106}

        ss_clad = CO[59]*0.00084 + MN[55]*0.0106
        for element in cladding_comp:
            if element != CO and element != MN:
                for isotope in cladding_comp[element]:
                    ss_clad += element[isotope]*cladding_comp[element][isotope]
        clad = Material(ss_clad)
        clad.comment='Cladding Composition from RCF SAR'

        absorber = Material(B[10]@0.11944 + FE[56]@0.88056)
        absorber.comment = 'Boron Absorber'

        # Homog. 300cm3 steel 134cm3 other.
        # Brake is in water or air only, only one mayerial is required.
        brake_ss = 300 #cm3
        brake_total_vol = np.pi * brake_r**2 * brake_h
        frac_other = (brake_total_vol-brake_ss) / brake_total_vol
        frac_ss = brake_ss / brake_total_vol
        if brake_h+follower_pos < water_height or follower_pos > water_height:
            # Brake is fully submerged
            if brake_h < water_height:
                hydr_brake = Material(stainless_steel@frac_ss + h2o@frac_other)
                hydr_brake.comment = ('Hydraulic Brake (homog. 300cm3 '
                                    + 'steel 134mL water)')
                hydr_brake.s_alpha_beta = 'lwtr'
                density_brake = frac_other*density_mod + frac_ss*density_ss
            # Brake is fully unsubmerged
            else:
                hydr_brake = Material(stainless_steel@frac_ss 
                                      + air_mix@frac_other)
                hydr_brake.comment = ('Hydraulic Brake (homog. 300cm3 '
                                    + 'steel 134mL air)')
                density_brake = frac_other*density_air + frac_ss*density_ss
            inp += hydr_brake
        # Brake is in water and air.
        else:
            hydr_brake1 = Material(stainless_steel@frac_ss + h2o@frac_other)
            hydr_brake1.comment = ('Hydraulic Brake Submerged, homog.')
            hydr_brake1.s_alpha_beta = 'lwtr'
            density_brake1 = frac_other*density_mod + frac_ss*density_ss

            hydr_brake2 = Material(stainless_steel@frac_ss 
                                   + air_mix@frac_other)
            hydr_brake2.comment = ('Hydraulic Brake Unsubmerged, homog.')
            density_brake2 = frac_other*density_air + frac_ss*density_ss
            inp += [hydr_brake1, hydr_brake2]

        inp += [mod, uo2, ss, al203, gas, absorber, air, clad, ss_spring]

        # Create regions.
        if sup_plate_bottom > water_height or water_height > sup_plate_top:
            r_sup_plate_outside = (-sup_plate & +lat_container & +channel1 
                                & +channel2 & +channel3 & +channel4)
        else:
            r_sup_plate_outside_a = (-sup_plate_a & +lat_container & +channel1 
                                     & +channel2 & +channel3 & +channel4)
            r_sup_plate_outside_b = (-sup_plate_b & +lat_container & +channel1 
                                     & +channel2 & +channel3 & +channel4)

            r_sup_plate_outside = ((-sup_plate_a | -sup_plate_b) 
                                   & +lat_container & +channel1 
                                   & +channel2 & +channel3 & +channel4)
        
        r_sup_plate_outside2 = (-sup_plate2 & +lat_container & +channel1 
                                & +channel2 & +channel3 & +channel4)
        r_bottom_plate = (-bottom_plate & -plate_plane1 & -plate_plane2 
                          & -plate_plane3 & +channel1 & +channel2 & +channel3 
                          & +channel4 & -plate_plane4 & +lat_container) 
                          #& ~(-sup_plate | -sup_plate2))
        if sup_plate_bottom > water_height or water_height > sup_plate_top:
            r_bottom_plate = r_bottom_plate & ~(-sup_plate | -sup_plate2)
        else:
            r_bottom_plate = r_bottom_plate & ~(-sup_plate_a | -sup_plate_b 
                                                | -sup_plate2)

        r_top_plate_outside = (-top_plate & +lat_container & +channel1 
                               & +channel2 & +channel3 & +channel4)
        r_top_sup_plate = (+top_sup_plate1 & +top_sup_plate2 & +top_sup_plate3
                           & -top_sup_plate4 & +channel1)
        r_mid_sup_plate = (-mid_sup_plate1 & +mid_sup_plate2 & +channel1 
                           & +channel2 & +channel3 & +channel4)
        r_sup_posts = ((-post1 | -post2 | -post3 | -post4) & ~r_mid_sup_plate 
                       & ~r_sup_plate_outside & ~r_sup_plate_outside2)
        r_tank_air = (-tank & +fill_height & -tank_top & +channel1 
                      & +channel2 & +channel3 & +channel4 & +lat_container 
                      & ~r_sup_plate_outside & ~r_sup_plate_outside2 
                      & ~r_bottom_plate & ~r_top_plate_outside & ~r_sup_posts
                      & ~r_top_sup_plate & ~r_mid_sup_plate)
        
        r_abs1 = -abs1_outer & +abs1_inner
        r_abs2 = -abs2_outer & +abs2_inner
        r_rod_clad = -rod_clad_outer & +rod_clad_inner & ~r_abs1 & ~r_abs2
        r_sup_plate_around_hole = -sup_plate2 & +pin_bottom_hole
        r_top_plate_around_hole = -pin_fill & +top_plate_hole & -top_plate
        r_gap = +fuel & -gap
        r_top_plate_hole = +top_plate_hole & -top_plate
        r_cladding = -clad_outer & +clad_inner
        r_around_pin = (-pin_fill #& +sup_plate 
                        & ~r_sup_plate_around_hole & +pin_bottom & ~r_gap 
                        & +fuel & +bottom_plug & +top_plug & +bottom_spacer 
                        & +top_spacer & +insulator & +spring #& +pin_top 
                        & ~r_top_plate_hole & ~r_cladding)
        if sup_plate_bottom > water_height or water_height > sup_plate_top:
            r_around_pin = r_around_pin & +sup_plate
        else:
            r_around_pin = r_around_pin & +sup_plate_a & +sup_plate_b
        if pin_top_base > water_height or water_height > pin_top_base+pin_top_h:
            r_around_pin = r_around_pin  & +pin_top
        else:
            r_around_pin = r_around_pin & +pin_top1 & pin_top2

        # Create cells.
        inp += Cell(material=ss*density_ss, comment='Tank',
                    region=-tank_bottom | (+tank & -tank_outside))
        inp += Cell(material=air*density_air, comment='Air Outside Tank',
                    region=+tank_outside & -outside & +tank_bottom)
        if sup_plate_bottom > water_height or water_height > sup_plate_top:
            inp += Cell(material=ss_bottom_plate*density_bottom_plate, 
                        comment='Bottom Sup. Plate',
                        region=r_sup_plate_outside)
        else:
            inp += Cell(material=ss_bottom_plate1*density_bottom_plate1, 
                        comment='Bottom Sup. Plate',
                        region=r_sup_plate_outside_a)
            inp += Cell(material=ss_bottom_plate2*density_bottom_plate2, 
                        comment='Bottom Sup. Plate',
                        region=r_sup_plate_outside_b)
        inp += Cell(material=ss*density_ss, comment='Bottom Lat. Plate',
                    region=r_sup_plate_outside2)
        inp += Cell(material=ss*density_ss, comment='Bottom Sup. Plate',
                    region=r_bottom_plate)
        inp += Cell(material=ss*density_ss, comment='Top Lat. Plate',
                    region=r_top_plate_outside)
        inp += Cell(material=ss*density_ss, comment='Top Sup. Plate',
                    region=r_top_sup_plate)
        inp += Cell(material=ss*density_ss, comment='Mid Sup. Plate',
                    region=r_mid_sup_plate)
        inp += Cell(material=ss*density_ss, 
                    comment='Sup. Posts', region=r_sup_posts)
        inp += Cell(material=air*density_air, comment='Air in Tank',
                    region=r_tank_air)
        inp += Cell(comment='Termination Region', region=+outside)
        if water_height > 0.0:
            inp += Cell(material=mod*density_mod, comment='Water Outside Lattice',
                        region=-tank & +lat_container & -fill_height 
                               & ~r_sup_plate_outside & +channel1 
                               & +channel2 & +channel3 & +channel4 
                               & ~r_bottom_plate & ~r_sup_posts
                               & ~r_top_plate_outside 
                               & ~r_top_sup_plate & ~r_mid_sup_plate 
                               & ~r_sup_plate_outside2)

        # Control Rods.
        tr1 = Transformation(transformation=[[22.38,0,0]])
        inp += tr1

        control_rod = []
        if brake_h+follower_pos < water_height or follower_pos > water_height:
            control_rod.append(Cell(material=hydr_brake*density_brake, 
                                    comment='Control Rod - Brake',
                                    region=-brake, transformation=tr1))
        else:
            control_rod.append(Cell(material=hydr_brake1*density_brake1, 
                                    comment='Control Rod - Brake in water',
                                    region=-brake1, transformation=tr1))
            control_rod.append(Cell(material=hydr_brake2*density_brake2, 
                                    comment='Control Rod - Brake in air',
                                    region=-brake2, transformation=tr1))
        control_rod.append(Cell(material=absorber*8.092, 
                                comment='Control Rod - Lower Absorber',
                                region=r_abs1, transformation=tr1))
        control_rod.append(Cell(material=absorber*8.092, 
                                comment='Control Rod - Upper Absorber',
                                region=r_abs2, transformation=tr1))
        control_rod.append(Cell(material=ss*density_ss, 
                                comment='Control Rod - Cladding',
                                region=-rod_clad_outer & +rod_clad_inner 
                                       & ~r_abs1 & ~r_abs2, transformation=tr1))
        control_rod.append(Cell(material=ss*density_ss, 
                                comment='Control Rod - Follower',
                                region=-follower, transformation=tr1))

        if water_height > 0.0:
            if brake_h+follower_pos < water_height or follower_pos > water_height:
                control_rod.append(Cell(material=mod*density_mod,  
                                        comment='Control Rod - Channel Water',
                                        region=-channel & -fill_height & +brake 
                                            & ~r_rod_clad & ~r_abs1 & ~r_abs2 
                                            & +follower, transformation=tr1))
                control_rod.append(Cell(material=air*density_air, 
                                        comment='Control Rod - Channel Air',
                                        region=-channel & +fill_height & +brake & ~r_abs1 
                                            & ~r_abs2 & ~r_rod_clad & +follower, 
                                        transformation=tr1))
            else:
                control_rod.append(Cell(material=mod*density_mod,  
                                        comment='Control Rod - Channel Water',
                                        region=-channel & -fill_height & +brake1
                                            & +brake2 
                                            & ~r_rod_clad & ~r_abs1 & ~r_abs2 
                                            & +follower, transformation=tr1))
                control_rod.append(Cell(material=air*density_air, 
                                        comment='Control Rod - Channel Air',
                                        region=-channel & +fill_height & +brake1 & +brake2 & ~r_abs1 
                                            & ~r_abs2 & ~r_rod_clad & +follower, 
                                        transformation=tr1))
        #u_control_rod **= c_rod_air

        # Define Universe for a Control Rod.
        u_control_rod = UniverseList(name=66, cells=control_rod)
        inp += control_rod

        # Fill channels with Control Rod Universe.
        # Rods are numbered 3, 4, 5, 7 like at the real RCF.
        inp += Cell(comment='Control Rod 7', region=-channel1, fill=u_control_rod)
        inp += Cell(comment='Control Rod 4', region=-channel1, fill=u_control_rod,
                    transform=Transform([-2*22.38, 0, 0]))
        inp += Cell(comment='Control Rod 5', region=-channel1, fill=u_control_rod,
                    transform=Transform([-22.38, 22.38, 0]))
        inp += Cell(comment='Control Rod 3', region=-channel1, fill=u_control_rod,
                    transform=Transform([-22.38, -22.38, 0]))

        # Cells for element without a pin.
        cells_no_pin = []
        if sup_plate_bottom > water_height or water_height > sup_plate_top:
            cells_no_pin.append(Cell(material=ss_bottom_plate*density_bottom_plate, 
                            comment='No Pin - Lower Sup. Plate',
                            region=-sup_plate))
        else:
            cells_no_pin.append(Cell(material=ss_bottom_plate1*density_bottom_plate1, 
                            comment='No Pin - Lower Sup. Plate',
                            region=-sup_plate_a))
            cells_no_pin.append(Cell(material=ss_bottom_plate2*density_bottom_plate2, 
                            comment='No Pin - Lower Sup. Plate',
                            region=-sup_plate_b))
        cells_no_pin.append(Cell(material=ss*density_ss, 
                                 comment='No Pin - Lower Lat. Plate',
                                 region=r_sup_plate_around_hole))
        cells_no_pin.append(Cell(material=ss*density_ss, 
                                 comment='No Pin - Top Lat. Plate',
                                 region=r_top_plate_around_hole))
        #cells_no_pin = [c_sup_plate, c_sup_plate_around_hole, c_top_plate_around_hole]
        if (water_height > 0):
            cells_no_pin.append(Cell(material=mod*density_mod, 
                                     comment='No Pin - Water',
                                     region=-fill_height & -pin_fill 
                                            & +sup_plate 
                                            & ~r_sup_plate_around_hole 
                                            & ~r_top_plate_around_hole))
        if (water_height < el_height):
            cells_no_pin.append(Cell(material=air*density_air, 
                                     comment='No Pin - Air',
                                     region=+fill_height & -pin_fill & +sup_plate 
                                            & ~r_sup_plate_around_hole 
                                            & ~r_top_plate_around_hole))
        inp += cells_no_pin
        # Define Universe for element without a pin.
        u1 = UniverseList(name=1, cells=cells_no_pin)
        # Add the cells to the input deck.
        # Each cell will have the U=1 keyword.

        # Cells for element with a pin.
        cells_pin = []
        if sup_plate_bottom > water_height or water_height > sup_plate_top:
            cells_pin.append(Cell(material=ss_bottom_plate*density_bottom_plate, 
                                comment='Pin - Bottom Sup. Plate',
                                region=-sup_plate))
        else:
            cells_pin.append(Cell(material=ss_bottom_plate1*density_bottom_plate1, 
                                  comment='Pin - Bottom Sup. Plate',
                                  region=-sup_plate_a))
            cells_pin.append(Cell(material=ss_bottom_plate2*density_bottom_plate2, 
                                  comment='Pin - Bottom Sup. Plate',
                                  region=-sup_plate_b))
        cells_pin.append(Cell(material=ss*density_ss, 
                              comment='Pin - Bottom Lat. Plate',
                              region=r_sup_plate_around_hole))
        cells_pin.append(Cell(material=ss*density_ss, comment='Pin - Bottom',
                              region=-pin_bottom))
        cells_pin.append(Cell(material=gas*1.78e-4, comment='Pin - Gap',
                              region=+fuel & -gap))
        cells_pin.append(Cell(material=uo2*10.048, comment='Pin - Fuel',
                              region=-fuel))
        cells_pin.append(Cell(material=ss*density_ss, 
                              comment='Pin - Bottom Plug',
                              region=-bottom_plug))
        cells_pin.append(Cell(material=ss*density_ss, comment='Pin - Top Plug',
                              region=-top_plug))
        cells_pin.append(Cell(material=al203*3.9, comment='Pin - Bottom Spacer',
                              region=-bottom_spacer))
        cells_pin.append(Cell(material=ss*density_ss, comment='Pin - Top Spacer',
                              region=-top_spacer))
        cells_pin.append(Cell(material=al203*3.9, comment='Pin - Insulator',
                              region=-insulator))
        cells_pin.append(Cell(material=ss_spring*density_spring, 
                              comment='Pin - Spring',
                              region=-spring))
        #if water_height > pin_top_h:
        if pin_top_base > water_height or water_height > pin_top_base+pin_top_h:
            cells_pin.append(Cell(material=ss_pin_top*density_pin_top, 
                                  comment='Pin - Top',
                                  region=-pin_top))
        else:
            cells_pin.append(Cell(material=ss_pin_top1*density_pin_top1, 
                                  comment='Pin - Top',
                                  region=-pin_top1))
            cells_pin.append(Cell(material=ss_pin_top1*density_pin_top2, 
                                  comment='Pin - Top',
                                  region=-pin_top2))
        cells_pin.append(Cell(material=ss*density_ss, 
                              comment='Pin - Top Lat. Plate',
                              region=r_top_plate_hole))
        cells_pin.append(Cell(material=clad*density_ss, comment='Pin Cladding',
                              region=r_cladding))
        if water_height > 0.0:
            cells_pin.append(Cell(material=mod*density_mod, comment='Pin - Water',
                                  region=r_around_pin & -fill_height))
        if water_height < el_height:
            cells_pin.append(Cell(material=air*density_air, 
                                  comment='Pin - Air',
                                  region=r_around_pin & +fill_height))
        inp += cells_pin
        # Define Universe for element with pin.
        u4 = UniverseList(name=4, cells=cells_pin)

        # Set up lattice.
        # Could be specified as (21,21). 
        # The explicit k dimension is for easy modification.
        lat = np.empty((1,21,21))
        lat[0][0] =  [1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]
        lat[0][1] =  [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1]
        lat[0][2] =  [1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1]
        lat[0][3] =  [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        lat[0][4] =  [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        lat[0][5] =  [1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1]
        lat[0][6] =  [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1]
        lat[0][7] =  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[0][8] =  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[0][9] =  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[0][10] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[0][11] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[0][12] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[0][13] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[0][14] = [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1]
        lat[0][15] = [1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1]
        lat[0][16] = [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        lat[0][17] = [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        lat[0][18] = [1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1]
        lat[0][19] = [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1]
        lat[0][20] = [1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]

        """
        lat[1][0] =  [1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]
        lat[1][1] =  [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1]
        lat[1][2] =  [1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1]
        lat[1][3] =  [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        lat[1][4] =  [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        lat[1][5] =  [1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1]
        lat[1][6] =  [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1]
        lat[1][7] =  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[1][8] =  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[1][9] =  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[1][10] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[1][11] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[1][12] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[1][13] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        lat[1][14] = [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1]
        lat[1][15] = [1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1]
        lat[1][16] = [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        lat[1][17] = [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        lat[1][18] = [1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1]
        lat[1][19] = [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1]
        lat[1][20] = [1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]
        """

        if self.sporty is True:
            lat[0,10,10] = 1
            self.title = 'RPI\'s RCF with Sport Mode Engaged! (332 pin configuration)'
        else:
            self.title = 'RPI\'s RCF with a standard 333 pin configuration'

        # Defining a lattice and filling cells.
        # lat is a 21x21 numpy array of universe IDs.
        core = Lattice(i=[-10,10], j=[-10,10], k=[0,0], 
            lattice=lat, type='REC', universes={1:u1, 4:u4})
        c_element = Cell(comment='Lattice Element',
                         region=-lat_element, fill=core)
        inp += c_element
        el_universe = UniverseList(name=10, cells=c_element)
        inp += Cell(comment='Lattice Container',
                            region=-lat_container, fill=el_universe)

        # Set cell importances.
        for cell in inp.cells.values():
            if cell.material is None and cell.fill is None:
                cell.importances = {'n' : 0.0}
            else:
                cell.importances = {'n' : 1.0}

        # Add kcode.
        inp += CriticalitySource(histories=1e5, keff_guess=1.0, 
                                 skip_cycles=200, cycles=1200)
        src_points = [(1.6526,0,90), (-1.6526,0,90), (0,1.62526,90), 
                      (0,-1.62526,90)]
        inp += CriticalitySourcePoints(src_points)

    def __repr__(self):
        string = 'RCF model written to ' + self.filename
        string += ('\n\tWater height = ' + str(self.water) + 'in (' 
            + str(self.water*2.54) + 'cm)')
        string += ('\n\tBank height = ' + str(self.bank) + 'in (' 
            + str(self.bank*2.54) + 'cm)')
        if self.sporty is True:
            string += ('\n\tConfiguration = Sport Mode (332 pins, center' 
                       + 'removed)')
        else:
            string += '\n\tConfiguration = Boring Mode (333 pins)'
        
        return string

    def write(self):
        """Write the RCF model to file.
        """
        self.deck.write(self.filename, self.title)
