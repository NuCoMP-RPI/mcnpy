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
        from mcnpy import Material, Nuclide, Sab
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
        tank = RCC(name=1, comment='Tank - Inside',
                   base=Point(0,0,0),
                   axis=Point(0,0,tank_h),
                   r=tank_ir)
        tank_outside = RCC(name=2, comment='Tank - Outside',
                           base=Point(0,0,0),
                           axis=Point(0,0,tank_h),
                           r=tank_ir+1.0)
        tank_bottom = RCC(name=3, comment='Tank - Bottom',
                          base=Point(0,0,-1),
                          axis=Point(0,0,1),
                          r=tank_ir+1.0)
        fill_height = Plane(name=4, comment='Water Fill Height',
                            a=0, b=0, c=1, d=water_height)
        tank_top = Plane(name=5, comment='Tank - Top',
                         a=0, b=0, c=1, d=tank_h)
        bottom_plate = RPP(name=6, comment='Bottom Sup. Plate',
                          x0=-0.5*sup_plate_width, x1=0.5*sup_plate_width, 
                          y0=-0.5*sup_plate_width, y1=0.5*sup_plate_width, 
                          z0=sup_plate_bottom, z1=sup_plate_top)
        # Planes for making bottom plate an octagon.
        plate_plane1 = PPoints(name=7, comment='Bottom Sup. Plate',
                               points=[Point(25.4,41.28,0.0), 
                               Point(25.4,41.28,25.4),
                               Point(41.28,25.4,0.0)])
        plate_plane2 = PPoints(name=8, comment='Bottom Sup. Plate',
                               points=[Point(-25.4,41.28,0.0),
                               Point(-25.4,41.28,25.4),
                               Point(-41.28,25.4,0.0)])
        plate_plane3 = PPoints(name=9, comment='Bottom Sup. Plate',
                               points=[Point(-41.28,-25.4,0.0),
                              Point(-41.28,-25.4,25.4),
                              Point(-25.4,-41.28,0.0)])
        plate_plane4 = PPoints(name=10, comment='Bottom Sup. Plate',
                               points=[Point(25.4,-41.28,0.0),
                               Point(25.4,-41.28,25.4),
                               Point(41.28,-25.4,0.0)])
        # Cutouts and top support plate surfaces.
        top_sup_plate1 = RPP(name=12, comment='Top Sup. Plate',
                             x0=-33.8, x1=33.8,
                             y0=-11.4, y1=11.4,
                             z0=top_plate_bottom-top_sup_plate_t, 
                             z1=top_plate_bottom)
        top_sup_plate2 = RPP(name=13, comment='Top Sup. Plate',
                             x0=-26.4, x1=26.4,
                             y0=-26.4, y1=26.4,
                             z0=top_plate_bottom-top_sup_plate_t, 
                             z1=top_plate_bottom)
        top_sup_plate3 = RPP(name=14, comment='Top Sup. Plate',
                             x0=-11.4, x1=11.4,
                             y0=-33.8, y1=33.8,
                             z0=top_plate_bottom-top_sup_plate_t, 
                             z1=top_plate_bottom)
        top_sup_plate4 = RCC(name=15, comment='Top Sup. Plate',
                             base=Point(0,0,top_plate_bottom-top_sup_plate_t),
                             axis=Point(0,0,top_sup_plate_t),
                             r=top_sup_plate_r)
        # Mid support plate
        mid_sup_plate1 = RPP(name=16, comment='Mid Sup. Plate',
                             x0=-33.02, x1=33.02,
                             y0=-33.02, y1=33.02,
                             z0=96.84, z1=96.84+1.27)
        mid_sup_plate2 = RPP(name=17, comment='Mid Sup. Plate',
                             x0=-26.67, x1=26.67,
                             y0=-26.67, y1=26.67,
                             z0=96.84, z1=96.84+1.27)
        # Support posts.
        post1 = RCC(name=18, comment='Sup. Post',
                    base=Point(post_pos,post_pos,0),
                    axis=Point(0,0,top_plate_bottom-top_sup_plate_t),
                    r=post_r)
        post2 = RCC(name=19, comment='Sup. Post',
                    base=Point(-post_pos,post_pos,0),
                    axis=Point(0,0,top_plate_bottom-top_sup_plate_t),
                    r=post_r)
        post3 = RCC(name=20, comment='Sup. Post',
                    base=Point(-post_pos,-post_pos,0),
                    axis=Point(0,0,top_plate_bottom-top_sup_plate_t),
                    r=post_r)
        post4 = RCC(name=21, comment='Sup. Post',
                    base=Point(post_pos,-post_pos,0),
                    axis=Point(0,0,top_plate_bottom-top_sup_plate_t),
                    r=post_r)
        # Air region extending 20cm beyond top and sides of tank.
        outside = RCC(name=22, comment='Outside Air',
                      base=Point(0,0,-1),
                      axis=Point(0,0,tank_h+1.0+20.0),
                      r=tank_ir+1.0+20.0)

        lat_container = RPP(name=23, comment='Lattice Container',
                            x0=-lat_width, x1=lat_width, 
                            y0=-lat_width, y1=lat_width, 
                            z0=0.00, z1=el_height)
        lat_element = RPP(name=24, comment='Lattice Element',
                          x0=-el_width, x1=el_width, 
                          y0=-el_width, y1=el_width, 
                          z0=0.00, z1=el_height)
        pin_fill = RPP(name=25, comment='Pincell Fill',
                       x0=-1, x1=1, 
                       y0=-1, y1=1, 
                       z0=-1, z1=175)

        # Control Rod Surfaces.
        rod_clad_inner = RPP(name=30, comment='Control Rod - Cladding',
                             x0=-rod_inner, x1=rod_inner, 
                             y0=-rod_inner, y1=rod_inner, 
                             z0=rod_position, z1=boron2_top)
        rod_clad_outer = RPP(name=31, comment='Control Rod - Cladding',
                             x0=-rod_outer, x1=rod_outer, 
                             y0=-rod_outer, y1=rod_outer, 
                             z0=rod_position, z1=boron2_top+2.0)
        abs1_inner = RPP(name=32, comment='Control Rod - Lower Absorber',
                         x0=-abs_inner, x1=abs_inner, 
                         y0=-abs_inner, y1=abs_inner, 
                         z0=boron1_bottom, z1=boron1_top)
        abs2_inner = RPP(name=33, comment='Control Rod - Upper Absorber',
                         x0=-abs_inner, x1=abs_inner, 
                         y0=-abs_inner, y1=abs_inner, 
                         z0=boron2_bottom, z1=boron2_top)
        abs1_outer = RPP(name=34, comment='Control Rod - Lower Absorber',
                         x0=-abs_outer, x1=abs_outer, 
                         y0=-abs_outer, y1=abs_outer, 
                         z0=boron1_bottom, z1=boron1_top)
        abs2_outer = RPP(name=35, comment='Control Rod - Upper Absorber',
                         x0=-abs_outer, x1=abs_outer, 
                         y0=-abs_outer, y1=abs_outer, 
                         z0=boron2_bottom, z1=boron2_top)
        brake = RCC(name=36, comment='Control Rod - Brake',
                    base=Point(0,0,follower_pos),
                    axis=Point(0,0,brake_h),
                    r=brake_r)
        # Extends from the brake to bottom of tank.
        follower = RCC(name=37, comment='Control Rod - Follower',
                     base=Point(0,0,follower_pos),
                     axis=Point(0,0,-follower_pos),
                     r=guide_tube_r)
        # Extends through all structures.
        channel1 = RPP(name=38, comment='Control Rod 7 - Channel',
                       x0=-channel_width+22.38, x1=channel_width+22.38,
                       y0=-channel_width, y1=channel_width,
                       z0=0, z1=tank_h)
        channel2 = RPP(name=39, comment='Control Rod 4 - Channel',
                       x0=-channel_width-22.38, x1=channel_width-22.38,
                       y0=-channel_width, y1=channel_width,
                       z0=0, z1=tank_h) 
        channel3 = RPP(name=40, comment='Control Rod 5 - Channel',
                       x0=-channel_width, x1=channel_width,
                       y0=-channel_width+22.38, y1=channel_width+22.38,
                       z0=0, z1=tank_h) 
        channel4 = RPP(name=41, comment='Control Rod 3 - Channel',
                       x0=-channel_width, x1=channel_width,
                       y0=-channel_width-22.38, y1=channel_width-22.38,
                       z0=0, z1=tank_h) 
        channel = RPP(name=42, comment='Control Rod - Channel Fill',
                      x0=-2*tank_ir, x1=2*tank_ir,
                      y0=-2*tank_ir, y1=2*tank_ir,
                      z0=-1, z1=tank_h+1) 

        inp += [rod_clad_inner, rod_clad_outer, abs1_inner, abs1_outer,   
                abs2_inner, abs2_outer, brake, follower, channel1, 
                channel2, channel3, channel4, channel]

        # Lattice element surfaces
        sup_plate = RPP(name=50, comment='No Pin - Lower Sup. Plate',
                        x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                        y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                        z0=sup_plate_bottom, z1=sup_plate_top)
        sup_plate2 = RPP(name=51, comment='No Pin - Lower Lat. Plate',
                         x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                         y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                         z0=sup_plate_top, z1=bottom_plug_base)
        pin_bottom = RCC(name=52, comment='Pin - Bottom',
                         base=Point(0,0,sup_plate_top), 
                         axis=Point(0,0,pin_hole_h), 
                         r=pin_bottom_r)
        pin_bottom_hole = RCC(name=53, comment='Pin - Bottom Hole',
                              base=Point(0,0,sup_plate_top), 
                              axis=Point(0,0,pin_hole_h), 
                              r=sup_plate_hole_r)
        bottom_plug = RCC(name=54, comment='Pin - Bottom Plug',
                          base=Point(0,0,bottom_plug_base), 
                          axis=Point(0,0,bottom_plug_h), 
                          r=clad_or)
        bottom_spacer = RCC(name=55, comment='Pin - Bottom Spacer',
                            base=Point(0,0,bottom_spacer_base), 
                            axis=Point(0,0,spacer_h), 
                            r=clad_ir)
        fuel = RCC(name=56, comment='Pin - Fuel',
                   base=Point(0,0,fuel_base), 
                   axis=Point(0,0,fuel_h), 
                   r=fuel_or)
        insulator = RCC(name=57, comment='Pin - Insulator',
                        base=Point(0,0,insulator_base), 
                        axis=Point(0,0,spacer_h), 
                        r=clad_ir)
        top_spacer = RCC(name=58, comment='Pin - Top Spacer',
                         base=Point(0,0,top_spacer_base), 
                         axis=Point(0,0,spacer_h), 
                         r=clad_ir)
        spring = RCC(name=59, comment='Pin - Spring',
                     base=Point(0,0,spring_base), 
                     axis=Point(0,0,spring_h), 
                     r=clad_ir)
        top_plug = RCC(name=60, comment='Pin - Top Plug',
                       base=Point(0,0,top_plug_base), 
                       axis=Point(0,0,top_plug_h), 
                       r=clad_ir)
        pin_top = RCC(name=61, comment='Pin - Top',
                      base=Point(0,0,pin_top_base), 
                      axis=Point(0,0,pin_top_h), 
                      r=clad_or)
        clad_inner = RCC(name=62, comment='Pin - Cladding',
                         base=Point(0,0,bottom_spacer_base), 
                         axis=Point(0,0,clad_h), 
                         r=clad_ir)
        clad_outer = RCC(name=63, comment='Pin - Cladding',
                         base=Point(0,0,bottom_spacer_base), 
                         axis=Point(0,0,clad_h), 
                         r=clad_or)
        gap = RCC(name=64, comment='Pin - Gap',
                  base=Point(0,0,fuel_base), 
                  axis=Point(0,0,fuel_h), 
                  r=clad_ir)
        top_plate = RPP(name=65, comment='Pin - Top Lat. Plate',
                        x0=-0.5*lat_plate_width, x1=0.5*lat_plate_width, 
                        y0=-0.5*lat_plate_width, y1=0.5*lat_plate_width, 
                        z0=top_plate_bottom, z1=top_plate_top)
        top_plate_hole = RCC(name=66, comment='Pin - Top Lat. Plate Hole',
                             base=Point(0,0,top_plate_bottom), 
                             axis=Point(0,0,pin_hole_h), 
                             r=top_plate_hole_r)
        pin_top_water = RCC(name=67, comment='Pin - Top Water',
                            base=Point(0,0,pin_top_water_base), 
                            axis=Point(0,0,pin_top_water_h), 
                            r=clad_or)
        top_plate_hole_water = RCC(name=68, comment='Pin - Top Hole Water',
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
        lwtr_mod = [Nuclide(name='h1', fraction=0.666667), 
                    Nuclide(name='o16', fraction=0.333333)]
        """uo2 = [Nuclide(name='u233', fraction=0.0000035168), 
               Nuclide(name='u234', fraction=0.000222438),
               Nuclide(name='u235', fraction=0.042263144),
               Nuclide(name='u236', fraction=0.000411466),
               Nuclide(name='u238', fraction=0.836299436),
               Nuclide(name='o16', fraction=0.1208)]"""
        ss = [Nuclide(name='fe56', fraction=0.69500), 
              Nuclide(name='cr52', fraction=0.19000),
              Nuclide(name='ni58', fraction=0.09500),
              Nuclide(name='mn55', fraction=0.02000)]
        al203 = [Nuclide(name='al27', fraction=0.4), 
                 Nuclide(name='O16', fraction=0.6)]
        gas = [Nuclide(name='h1', fraction=0.5), 
               Nuclide(name='he4', fraction=0.5)]
        m_spring = [Nuclide(name='fe56', fraction=0.69500), 
                    Nuclide(name='cr52', fraction=0.19000),
                    Nuclide(name='ni58', fraction=0.09500),
                    Nuclide(name='mn55', fraction=0.02000)]
        m_pin_top = [Nuclide(name='fe56', fraction=0.46843), 
                     Nuclide(name='cr52', fraction=0.12806),
                     Nuclide(name='ni58', fraction=0.06403),
                     Nuclide(name='mn55', fraction=0.01348)]
        # ~.84 SS
        m_bottom_sup_plate = [Nuclide(name='fe56', fraction=0.5838), 
                              Nuclide(name='cr52', fraction=0.1596),
                              Nuclide(name='ni58', fraction=0.0798),
                              Nuclide(name='mn55', fraction=0.0168),
                              Nuclide(name='H1', fraction=0.1067), 
                              Nuclide(name='O16', fraction=0.0533)]
        m_cladding = [Nuclide(name='fe54', fraction=0.041105547, unit='-'), 
                      Nuclide(name='fe56', fraction=0.64526918, unit='-'),
                      Nuclide(name='fe57', fraction=0.014902079, unit='-'),
                      Nuclide(name='fe58', fraction=0.001983193, unit='-'),
                      Nuclide(name='cr50', fraction=0.0080817, unit='-'),
                      Nuclide(name='cr52', fraction=0.15584754, unit='-'),
                      Nuclide(name='cr53', fraction=0.01767186, unit='-'),
                      Nuclide(name='cr54', fraction=0.0043989, unit='-'),
                      Nuclide(name='ni58', fraction=0.065081612, unit='-'),
                      Nuclide(name='ni60', fraction=0.025069188, unit='-'),
                      Nuclide(name='ni61', fraction=0.00108984, unit='-'),
                      Nuclide(name='ni62', fraction=0.003474104, unit='-'),
                      Nuclide(name='ni64', fraction=0.000885256, unit='-'),
                      Nuclide(name='mn55', fraction=0.0106, unit='-'),
                      Nuclide(name='mo92', fraction=0.0002968, unit='-'),
                      Nuclide(name='mo94', fraction=0.000185, unit='-'),
                      Nuclide(name='mo95', fraction=0.0003184, unit='-'),
                      Nuclide(name='mo96', fraction=0.0003336, unit='-'),
                      Nuclide(name='mo97', fraction=0.000191, unit='-'),
                      Nuclide(name='mo98', fraction=0.0004826, unit='-'),
                      Nuclide(name='mo100', fraction=0.0001926, unit='-'),
                      Nuclide(name='cu63', fraction=0.00117589, unit='-'), 
                      Nuclide(name='cu65', fraction=0.00052411, unit='-'),
                      Nuclide(name='co59', fraction=0.00084, unit='-')]
        m_air = [Nuclide(name='C', fraction=0.000124, unit='-'),
                 Nuclide(name='N14', fraction=0.755268, unit='-'),
                 Nuclide(name='O16', fraction=0.231781, unit='-'),
                 Nuclide(name='Ar', fraction=0.012827, unit='-')]
        m_abs = [Nuclide(name='B10', fraction=0.11944),
                 Nuclide(name='fe56', fraction=0.88056)]
        #TODO: Need to update this for when the brake isn't fully submerged
        # or there is something besides water present.
        # Homog. 300cm3 steel 134cm3 water 
        m_brake = [Nuclide(name='fe56', fraction=0.45856),
                  Nuclide(name='cr52', fraction=0.12536),
                  Nuclide(name='ni58', fraction=0.06268),
                  Nuclide(name='mn55', fraction=0.01320),
                  Nuclide(name='h1', fraction=0.22682),
                  Nuclide(name='o16', fraction=0.11338)]

        m1 = Material(name=1, nuclides=lwtr_mod, 
                      comment='Light Water Moderator')
        #m2 = Material(name=2, comment='UO2 Fuel')
        m2 = (Nuclide('u233', 0.0000035168) 
             + Nuclide('u234', 0.000222438)
             + Nuclide('u235', 0.042263144)
             + Nuclide('u236', 0.000411466)
             + Nuclide('u238', 0.836299436)
             + Nuclide('o16', 0.1208))
        m2.unit = 'WEIGHT'
        #m2.name = 2

        m3 = Material(name=3, nuclides=ss, comment='Stainless Steel')
        m4 = Material(name=4, nuclides=al203, comment='Al203 Spacers')
        m5 = Material(name=5, nuclides=gas, comment='Gas Plenum')
        m6 = Material(name=6, nuclides=m_spring, comment='Spring Region')
        m7 = Material(name=7, nuclides=m_pin_top, 
                      comment='Top of Pin (SS comp=SS*0.674)')
        m8 = Material(name=8, nuclides=m_abs, comment='Boron Absorber')
        m9 = Material(name=9, nuclides=m_brake, 
                      comment='Hydraulic Brake (homog. 300cm3 '
                              +'steel 134mL water)')
        m10 = Material(name=10, nuclides=m_bottom_sup_plate, 
                       comment='Bottom Sup. Plate (~.84 SS)')
        m13 = Material(name=13, nuclides=m_air, comment='Air')
        m14 = Material(name=14, nuclides=m_cladding, 
                       comment='Cladding Composition from RCF SAR')
        inp += [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m13, m14]

        # Add SaB to m1, m2, and m9.
        inp += Sab(m1, ['lwtr'])
        inp += Sab(m2, ['o_in_uo2', 'u238_in_uo2'])
        inp += Sab(m9, ['lwtr'])

        # Create cells.
        c_tank = Cell(name=100, material=m3, density=8.0, comment='Tank',
                      region=-tank_bottom | (+tank & -tank_outside), 
                      density_unit = '-')
        c_outside_air = Cell(name=101, material=m13, density=0.001205, 
                             comment='Air Outside Tank',
                             region=+tank_outside & -outside & +tank_bottom, 
                             density_unit = '-')
        c_sup_plate_outside = Cell(name=102, material=m10, density=7.0, 
                                   comment='Bottom Sup. Plate',
                                   region=-sup_plate & +lat_container 
                                          & +channel1 & +channel2 
                                          & +channel3 & +channel4, 
                                   density_unit = '-')
        c_sup_plate_outside2 = Cell(name=103, material=m3, density=8.0, 
                                    comment='Bottom Lat. Plate',
                                    region=-sup_plate2 & +lat_container 
                                           & +channel1 & +channel2 
                                           & +channel3 & +channel4, 
                                    density_unit = '-')
        c_bottom_plate = Cell(name=104, material=m3, density=8.0, 
                              comment='Bottom Sup. Plate',
                              region=-bottom_plate & -plate_plane1 
                                     & -plate_plane2 
                                     & -plate_plane3 & +channel1 & +channel2 
                                     & +channel3 & +channel4
                                     & -plate_plane4 & +lat_container 
                                     & ~(-sup_plate | -sup_plate2), 
                              density_unit = '-')
        c_top_plate_outside = Cell(name=105, material=m3, density=8.0, 
                                  comment='Top Lat. Plate',
                                   region=-top_plate & +lat_container 
                                          & +channel1 & +channel2 
                                          & +channel3 & +channel4, 
                                   density_unit = '-')
        c_top_sup_plate = Cell(name=106, material=m3, density=8.0, 
                               comment='Top Sup. Plate',
                               region=+top_sup_plate1 & +top_sup_plate2 
                                      & +top_sup_plate3
                                      & -top_sup_plate4 & +channel1 
                                      & +channel2 & +channel3 & +channel4, 
                               density_unit = '-')
        c_mid_sup_plate = Cell(name=107, material=m3, density=8.0, 
                               comment='Mid Sup. Plate',
                               region=-mid_sup_plate1 & +mid_sup_plate2 
                                      & +channel1 & +channel2 
                                      & +channel3 & +channel4, 
                               density_unit = '-')
        c_sup_posts = Cell(name=108, material=m3, density=8.0, 
                           comment='Sup. Posts',
                           region=(-post1 | -post2 | -post3 | -post4) 
                                  & ~c_mid_sup_plate 
                                  & ~c_sup_plate_outside 
                                  & ~c_sup_plate_outside2, 
                           density_unit = '-')
        c_tank_air = Cell(name=109, material=m13, density=0.001205, 
                          comment='Air in Tank',
                          region=-tank & +fill_height & -tank_top & +channel1 
                                 & +channel2 & +channel3 & +channel4 
                                 & +lat_container & ~c_sup_plate_outside 
                                 & ~c_sup_plate_outside2 & ~c_bottom_plate 
                                 & ~c_top_plate_outside & ~c_sup_posts
                                 & ~c_top_sup_plate & ~c_mid_sup_plate, 
                          density_unit = '-')

        c_out_of_bounds = Cell(name=110, comment='Termination Region', 
                               region=+outside)
        if water_height > 0.0:
            inp += Cell(name=111, material=m1, density=density_mod, 
                        comment='Water Outside Lattice',
                        region=-tank & +lat_container & -fill_height 
                            & ~c_sup_plate_outside & +channel1 
                            & +channel2 & +channel3 & +channel4 
                            & ~c_bottom_plate & ~c_sup_posts
                            & ~c_top_plate_outside 
                            & ~c_top_sup_plate & ~c_mid_sup_plate 
                            & ~c_sup_plate_outside2, 
                        density_unit = '-')

        inp += [c_tank, c_tank_air, c_outside_air, c_sup_plate_outside, 
                c_bottom_plate, c_out_of_bounds, c_top_plate_outside, 
                c_top_sup_plate, c_mid_sup_plate, c_sup_plate_outside2, 
                c_sup_posts]

        # Control Rods.
        tr1 = Transformation(name=1, transformation=[[22.38,0,0]])
        inp += tr1

        #TODO: Need to update brake desnity for when rod isn't fully submerged.
        c_brake = Cell(name=200, material=m9, density=5.84, 
                       comment='Control Rod - Brake',
                       region=-brake, 
                       density_unit = '-',
                       transformation=tr1)
        c_abs1 = Cell(name=201, material=m8, density=8.092, 
                      comment='Control Rod - Lower Absorber',
                      region=-abs1_outer & +abs1_inner, 
                      density_unit = '-',
                      transformation=tr1)
        c_abs2 = Cell(name=202, material=m8, density=8.092, 
                      comment='Control Rod - Upper Absorber',
                      region=-abs2_outer & +abs2_inner, 
                      density_unit = '-',
                      transformation=tr1)
        c_rod_clad = Cell(name=203, material=m3, density=8.0, 
                          comment='Control Rod - Cladding',
                          region=-rod_clad_outer & +rod_clad_inner & ~c_abs1 
                                 & ~c_abs2, 
                          density_unit = '-',
                          transformation=tr1)
        c_follower = Cell(name=204, material=m3, density=8.0, 
                          comment='Control Rod - Follower',
                          region=-follower, 
                          density_unit = '-',
                          transformation=tr1)
        control_rod = [c_brake, c_abs1, c_abs2, c_rod_clad, c_follower]
        #u_control_rod = c_brake ** c_abs1 ** c_abs2 ** c_rod_clad ** c_follower

        if water_height > 0.0:
            c_rod_water = Cell(name=205, material=m1, density=density_mod,  
                               comment='Control Rod - Channel Water',
                               region=-channel & -fill_height & ~c_brake 
                                      & ~c_rod_clad & ~c_abs1 & ~c_abs2 
                                      & ~c_follower, 
                               density_unit = '-',
                               transformation=tr1)
            control_rod.append(c_rod_water)
            #u_control_rod **= c_rod_water
        c_rod_air = Cell(name=206, material=m13, density=0.001205, 
                         comment='Control Rod - Channel Air',
                         region=-channel & +fill_height & ~c_brake & ~c_abs1 
                                & ~c_abs2 & ~c_rod_clad & ~c_follower, 
                         density_unit = '-',
                         transformation=tr1)
        control_rod.append(c_rod_air)
        #u_control_rod **= c_rod_air

        # Define Universe for a Control Rod.
        u_control_rod = UniverseList(name=66, cells=control_rod)
        u_control_rod
        inp += control_rod

        # Fill channels with Control Rod Universe.
        # Rods are numbered 3, 4, 5, 7 like at the real RCF.
        inp += Cell(name=207, comment='Control Rod 7', region=-channel1, 
                      fill=u_control_rod)
        inp += Cell(name=208, comment='Control Rod 4', region=-channel1, 
                      fill=u_control_rod,
                      transform=Transform([-2*22.38, 0, 0]))
        inp += Cell(name=209, comment='Control Rod 5', region=-channel1, 
                      fill=u_control_rod,
                      transform=Transform([-22.38, 22.38, 0]))
        inp += Cell(name=210, comment='Control Rod 3', region=-channel1, 
                      fill=u_control_rod,
                      transform=Transform([-22.38, -22.38, 0]))

        # Cells for element without a pin.
        c_sup_plate = Cell(name=300, material=m10, density=7.0, 
                           comment='No Pin - Lower Sup. Plate',
                           region=-sup_plate, 
                           density_unit = '-')
        c_sup_plate_around_hole = Cell(name=301, material=m3, density=8.0, 
                                       comment='No Pin - Lower Lat. Plate',
                                       region=-sup_plate2 & +pin_bottom_hole, 
                                       density_unit = '-')
        c_top_plate_around_hole = Cell(name=302, material=m3, density=8.0, 
                                       comment='No Pin - Top Lat. Plate',
                                       region=-pin_fill & +top_plate_hole 
                                              & -top_plate, 
                                       density_unit = '-')
        cells_no_pin = [c_sup_plate, c_sup_plate_around_hole, c_top_plate_around_hole]
        if (water_height > 0):
            c_water_no_pin = Cell(name=303, material=m1, density=density_mod, 
                                  comment='No Pin - Water',
                                  region=-fill_height & -pin_fill 
                                         & ~c_sup_plate 
                                         & ~c_sup_plate_around_hole 
                                         & ~c_top_plate_around_hole, 
                                  density_unit = '-')
            cells_no_pin.append(c_water_no_pin)
        if (water_height < el_height):
            c_air_no_pin = Cell(name=304, material=m13, density=0.001205, 
                                comment='No Pin - Air',
                                region=+fill_height & -pin_fill & ~c_sup_plate 
                                       & ~c_sup_plate_around_hole 
                                       & ~c_top_plate_around_hole, 
                                density_unit = '-')
            cells_no_pin.append(c_air_no_pin)
        
        # Define Universe for element without a pin.
        u1 = UniverseList(name=1, cells=cells_no_pin)
        # Add the cells to the input deck.
        # Each cell will have the U=1 keyword.
        inp += cells_no_pin

        # Cells for element with a pin.
        c_sup_plate_pin = Cell(name=400, material=m10, density=7.0, 
                               comment='Pin - Bottom Sup. Plate',
                               region=-sup_plate, 
                               density_unit = '-')
        c_sup_plate_around_hole_pin = Cell(name=401, material=m3, density=8.0, 
                                           comment='Pin - Bottom Lat. Plate',
                                           region=-sup_plate2 
                                                  & +pin_bottom_hole, 
                                           density_unit = '-')
        c_pin_bottom = Cell(name=402, material=m3, density=8.0, 
                            comment='Pin - Bottom',
                            region=-pin_bottom, 
                            density_unit = '-')
        c_gap = Cell(name=403, material=m5, density=1.78e-4, 
                     comment='Pin - Gap',
                     region=+fuel & -gap, 
                     density_unit = '-')
        c_fuel = Cell(name=404, material=m2, density=10.048, 
                      comment='Pin - Fuel',
                      region=-fuel, 
                      density_unit = '-')
        c_bottom_plug = Cell(name=405, material=m3, density=8.0, 
                             comment='Pin - Bottom Plug',
                             region=-bottom_plug, 
                             density_unit = '-')
        c_top_plug = Cell(name=406, material=m3, density=8.0, 
                          comment='Pin - Top Plug',
                          region=-top_plug, 
                          density_unit = '-')
        c_bottom_spacer = Cell(name=407, material=m4, density=3.9,  
                               comment='Pin - Bottom Spacer',
                               region=-bottom_spacer, 
                               density_unit = '-')
        c_top_spacer = Cell(name=408, material=m3, density=8.0, 
                            comment='Pin - Top Spacer',
                            region=-top_spacer, 
                            density_unit = '-')
        c_insulator = Cell(name=409, material=m4, density=3.9, 
                           comment='Pin - Insulator',
                           region=-insulator, 
                           density_unit = '-')
        c_spring = Cell(name=410, material=m6, density=1.0, 
                        comment='Pin - Spring',
                        region=-spring, 
                        density_unit = '-')
        if water_height > pin_top_h:
            c_pin_top = Cell(name=411, material=m7, density=5.71, 
                             comment='Pin - Top',
                             region=-pin_top, 
                             density_unit = '-')
        else:
            c_pin_top = Cell(name=411, material=m7, density=5.39, 
                             comment='Pin - Top',
                             region=-pin_top, 
                             density_unit = '-')
        c_top_plate_hole = Cell(name=412, material=m3, density=8.0, 
                                comment='Pin - Top Lat. Plate',
                                region=+top_plate_hole & -top_plate, 
                                density_unit = '-')
        c_cladding = Cell(name=413, material=m14, density=8.0, 
                          comment='Pin Cladding',
                          region=-clad_outer & +clad_inner, 
                          density_unit = '-')
        cells_pin = [c_sup_plate_pin, c_sup_plate_around_hole_pin, 
                     c_pin_bottom, c_gap, c_fuel, c_bottom_plug, c_top_plug, 
                     c_bottom_spacer, c_top_spacer, c_insulator, c_spring, 
                     c_pin_top, c_top_plate_hole, c_cladding]
        if water_height > 0.0:
            c_water_around_pin = Cell(name=414, material=m1, 
                                      density=density_mod, 
                                      comment='Pin - Water',
                                      region=-fill_height & -pin_fill 
                                             & ~c_sup_plate_pin 
                                             & ~c_sup_plate_around_hole_pin 
                                             & ~c_pin_bottom & ~c_gap 
                                             & ~c_fuel & ~c_bottom_plug 
                                             & ~c_top_plug & ~c_bottom_spacer 
                                             & ~c_top_spacer & ~c_insulator 
                                             & ~c_spring & ~c_pin_top 
                                             & ~c_top_plate_hole 
                                             & ~c_cladding, 
                                      density_unit = '-')
            cells_pin.append(c_water_around_pin)
        if water_height < el_height:
            c_air_around_pin = Cell(name=415, material=m13, density=0.001205, 
                                    comment='Pin - Air',
                                    region=+fill_height & -pin_fill 
                                           & ~c_sup_plate_pin 
                                           & ~c_sup_plate_around_hole_pin 
                                           & ~c_pin_bottom & ~c_gap & ~c_fuel 
                                           & ~c_bottom_plug & ~c_top_plug 
                                           & ~c_bottom_spacer & ~c_top_spacer 
                                           & ~c_insulator & ~c_spring 
                                           & ~c_pin_top & ~c_top_plate_hole 
                                           & ~c_cladding, 
                                    density_unit = '-')
            cells_pin.append(c_air_around_pin)

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
        c_element = Cell(name=113, comment='Lattice Element',
                         region=-lat_element, fill=core)
        el_universe = UniverseList(name=10, cells=c_element)
        c_inside_lat = Cell(name=112, comment='Lattice Container',
                            region=-lat_container, fill=el_universe)
        inp += [c_element, c_inside_lat]

        # Set cell importances.
        for cell in inp.cells.values():
            if cell.material == c_out_of_bounds:
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
