from .elements import *

class RCF():
    """A full core model of RPI's Reactor Critical Facility. A very critical reactor that will live on in the virtual world no matter what Shirley and the RPI administration does. This example will generate a new MCNP deck, build the RCF, and write the model to file.`water` sets the height of the water in the reactor in inches (default is `68.0in`). `bank` sets the control rod bank height in inches (default is rods fully bottomed at `0.0in`). `sporty` when set to `True` removes the center fuel pin which puts the RCF in sport mode. `filename` specifies the name of the new MCNP input (default is `./mcnp_inps/rcf_full_api.mcnp`). The model can be accessed with the `model` attribute.

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
    deck : mcnp.InputDeck
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
        `./mcnp_inps/rcf_full_api.mcnp`). The model can be accessed with the 
        `model` attribute.
        """
        import numpy as np
        from mcnpy import Cell, Deck, Lattice, Point, UniverseList
        from mcnpy import Transform, Transformation
        from mcnpy import Material
        from mcnpy import CriticalitySource, CriticalitySourcePoints
        from mcnpy import CircularCylinder as RCC
        from mcnpy import RectangularPrism as RPP
        from mcnpy import Plane, PPoints

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
        density_mod = 0.998113

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
        brake = RCC(comment='Control Rod - Brake',
                    base=Point(0,0,follower_pos),
                    axis=Point(0,0,brake_h),
                    r=brake_r)
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
                abs2_inner, abs2_outer, brake, follower, channel1, 
                channel2, channel3, channel4, channel]

        # Lattice element surfaces
        sup_plate = RPP(comment='No Pin - Lower Sup. Plate',
                        x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                        y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                        z0=sup_plate_bottom, z1=sup_plate_top)
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
        pin_top = RCC(comment='Pin - Top',
                      base=Point(0,0,pin_top_base), 
                      axis=Point(0,0,pin_top_h), 
                      r=clad_or)
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
                lat_element, sup_plate, sup_plate2, pin_bottom,
                pin_bottom_hole, bottom_plug, bottom_spacer, spring, 
                top_plug, pin_top, clad_inner, clad_outer, gap, top_plate, 
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

        gas = Material(H[1]@0.5 + HE[4]@0.5)
        gas.comment = 'Gas Plenum'

        # ~0.84 SS
        ss_bottom_plate = Material(stainless_steel@0.84 + h2o@0.16)
        ss_bottom_plate.comment = 'Bottom Sup. Plate (~.84 SS)'

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

        air = Material(C%0.0124 + N[14]%75.5268 + O[16]%23.1781 + AR%1.2827)
        air.comment = 'Air'

        absorber = Material(B[10]@0.11944 + FE[56]@0.88056)
        absorber.comment = 'Boron Absorber'

        #TODO: Need to update this for when the brake isn't fully submerged
        # or there is something besides water present.
        # Homog. 300cm3 steel 134cm3 water 
        brake_h2o = 134 #cm3
        brake_ss = 300 #cm3
        frac_h2o = brake_h2o / (brake_h2o + brake_ss)
        frac_ss = brake_ss / (brake_h2o + brake_ss)
        hydr_brake = Material(stainless_steel@frac_ss + h2o@frac_h2o)
        hydr_brake.comment = ('Hydraulic Brake (homog. 300cm3 '
                              + 'steel 134mL water)')
        hydr_brake.s_alpha_beta = 'lwtr'

        inp += [mod, uo2, ss, al203, gas, absorber, hydr_brake, ss_bottom_plate, 
                air, clad]

        # Create regions.
        r_sup_plate_outside = (-sup_plate & +lat_container & +channel1 
                               & +channel2 & +channel3 & +channel4)
        r_sup_plate_outside2 = (-sup_plate2 & +lat_container & +channel1 
                                & +channel2 & +channel3 & +channel4)
        r_bottom_plate = (-bottom_plate & -plate_plane1 & -plate_plane2 
                          & -plate_plane3 & +channel1 & +channel2 & +channel3 
                          & +channel4 & -plate_plane4 & +lat_container 
                          & ~(-sup_plate | -sup_plate2))
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
        r_around_pin = (-fill_height & -pin_fill & +sup_plate 
                        & ~r_sup_plate_around_hole & +pin_bottom & ~r_gap 
                        & +fuel & +bottom_plug & +top_plug & +bottom_spacer 
                        & +top_spacer & +insulator & +spring & +pin_top 
                        & ~r_top_plate_hole & ~r_cladding)

        # Create cells.
        inp += Cell(material=ss*8.0, comment='Tank',
                    region=-tank_bottom | (+tank & -tank_outside))
        inp += Cell(material=air*0.001205, comment='Air Outside Tank',
                    region=+tank_outside & -outside & +tank_bottom)
        inp += Cell(material=ss_bottom_plate*7.0, 
                    comment='Bottom Sup. Plate',
                    region=r_sup_plate_outside)
        inp += Cell(material=ss*8.0, comment='Bottom Lat. Plate',
                    region=r_sup_plate_outside2)
        inp += Cell(material=ss*8.0, comment='Bottom Sup. Plate',
                    region=r_bottom_plate)
        inp += Cell(material=ss*8.0, comment='Top Lat. Plate',
                    region=r_top_plate_outside)
        inp += Cell(material=ss*8.0, comment='Top Sup. Plate',
                    region=r_top_sup_plate)
        inp += Cell(material=ss*8.0, comment='Mid Sup. Plate',
                    region=r_mid_sup_plate)
        inp += Cell(material=ss*8.0, comment='Sup. Posts', region=r_sup_posts)
        inp += Cell(material=air*0.001205, comment='Air in Tank',
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

        """inp += [c_tank, c_tank_air, c_outside_air, c_sup_plate_outside, 
                c_bottom_plate, c_out_of_bounds, c_top_plate_outside, 
                c_top_sup_plate, c_mid_sup_plate, c_sup_plate_outside2, 
                c_sup_posts]"""

        # Control Rods.
        tr1 = Transformation(transformation=[[22.38,0,0]])
        inp += tr1

        #TODO: Need to update brake desnity for when rod isn't fully submerged.
        control_rod = []
        control_rod.append(Cell(material=hydr_brake*5.84, 
                                comment='Control Rod - Brake',
                                region=-brake, transformation=tr1))
        control_rod.append(Cell(material=absorber*8.092, 
                                comment='Control Rod - Lower Absorber',
                                region=r_abs1, transformation=tr1))
        control_rod.append(Cell(material=absorber*8.092, 
                                comment='Control Rod - Upper Absorber',
                                region=r_abs2, transformation=tr1))
        control_rod.append(Cell(material=ss*8.0, comment='Control Rod - Cladding',
                                region=-rod_clad_outer & +rod_clad_inner 
                                       & ~r_abs1 & ~r_abs2, transformation=tr1))
        control_rod.append(Cell(material=ss*8.0, comment='Control Rod - Follower',
                                region=-follower, transformation=tr1))
        #control_rod = [c_brake, c_abs1, c_abs2, c_rod_clad, c_follower]
        #u_control_rod = c_brake ** c_abs1 ** c_abs2 ** c_rod_clad ** c_follower

        if water_height > 0.0:
            control_rod.append(Cell(material=mod*density_mod,  
                                    comment='Control Rod - Channel Water',
                                    region=-channel & -fill_height & +brake 
                                           & ~r_rod_clad & ~r_abs1 & ~r_abs2 
                                           & +follower, transformation=tr1))
            #u_control_rod **= c_rod_water
        control_rod.append(Cell(material=air*0.001205, 
                                comment='Control Rod - Channel Air',
                                region=-channel & +fill_height & +brake & ~r_abs1 
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
        cells_no_pin.append(Cell(material=ss_bottom_plate*7.0, 
                           comment='No Pin - Lower Sup. Plate',
                           region=-sup_plate))
        cells_no_pin.append(Cell(material=ss*8.0, 
                                 comment='No Pin - Lower Lat. Plate',
                                 region=r_sup_plate_around_hole))
        cells_no_pin.append(Cell(material=ss*8.0, 
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
            cells_no_pin.append(Cell(material=air*0.001205, 
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
        cells_pin.append(Cell(material=ss_bottom_plate*7.0, 
                              comment='Pin - Bottom Sup. Plate',
                              region=-sup_plate))
        cells_pin.append(Cell(material=ss*8.0, comment='Pin - Bottom Lat. Plate',
                              region=r_sup_plate_around_hole))
        cells_pin.append(Cell(material=ss*8.0, comment='Pin - Bottom',
                              region=-pin_bottom))
        cells_pin.append(Cell(material=gas*1.78e-4, comment='Pin - Gap',
                              region=+fuel & -gap))
        cells_pin.append(Cell(material=uo2*10.048, comment='Pin - Fuel',
                              region=-fuel))
        cells_pin.append(Cell(material=ss*8.0, comment='Pin - Bottom Plug',
                              region=-bottom_plug))
        cells_pin.append(Cell(material=ss*8.0, comment='Pin - Top Plug',
                              region=-top_plug))
        cells_pin.append(Cell(material=al203*3.9, comment='Pin - Bottom Spacer',
                              region=-bottom_spacer))
        cells_pin.append(Cell(material=ss*8.0, comment='Pin - Top Spacer',
                              region=-top_spacer))
        cells_pin.append(Cell(material=al203*3.9, comment='Pin - Insulator',
                              region=-insulator))
        cells_pin.append(Cell(material=ss*1.0, comment='Pin - Spring',
                              region=-spring))
        if water_height > pin_top_h:
            cells_pin.append(Cell(material=ss*5.71, comment='Pin - Top',
                                  region=-pin_top))
        else:
            cells_pin.append(Cell(material=ss*5.39, comment='Pin - Top',
                                  region=-pin_top))
        cells_pin.append(Cell(material=ss*8.0, comment='Pin - Top Lat. Plate',
                              region=r_top_plate_hole))
        cells_pin.append(Cell(material=clad*8.0, comment='Pin Cladding',
                              region=r_cladding))
        """cells_pin = [c_sup_plate_pin, c_sup_plate_around_hole_pin, 
                     c_pin_bottom, c_gap, c_fuel, c_bottom_plug, c_top_plug, 
                     c_bottom_spacer, c_top_spacer, c_insulator, c_spring, 
                     c_pin_top, c_top_plate_hole, c_cladding]"""
        if water_height > 0.0:
            cells_pin.append(Cell(material=mod*density_mod, comment='Pin - Water',
                                  region=r_around_pin))
        if water_height < el_height:
            cells_pin.append(Cell(material=air*0.001205, 
                                  comment='Pin - Air',
                                  region=r_around_pin))
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
