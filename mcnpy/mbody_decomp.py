from mcnpy.surfaces import RectangularPrism as RPP
from mcnpy.surfaces import CircularCylinder as RCC
from mcnpy.surfaces import HexagonalPrism as HEX
from mcnpy.surfaces import Wedge as WED
from mcnpy.surfaces import Polyhedron as ARB
from mcnpy.surfaces import Box as BOX
from mcnpy.surfaces import TruncatedCone as TRC
from mcnpy.surfaces import Ellipsoid as ELL
from mcnpy.surfaces import EllipticalCylinder as REC
from mcnpy.surfaces import Plane, Quadric
import numpy as np
import math

def rotation_matrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    rot_mat = np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
        [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
        [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
    return(rot_mat)

def rpp(mbody:RPP):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    if mbody.x0 == mbody.x1:
        surfs.append(Plane(name=id+1, a=0, b=1, c=0, d=mbody.y1, boundary_type=bound))
        surfs.append(Plane(name=id+2, a=0, b=1, c=0, d=mbody.y0, boundary_type=bound))
        surfs.append(Plane(name=id+3, a=0, b=0, c=1, d=mbody.z1, boundary_type=bound))
        surfs.append(Plane(name=id+4, a=0, b=0, c=1, d=mbody.z0, boundary_type=bound))
    elif mbody.y0 == mbody.y1:
        surfs.append(Plane(name=id+1, a=1, b=0, c=0, d=mbody.x1, boundary_type=bound))
        surfs.append(Plane(name=id+2, a=1, b=0, c=0, d=mbody.x0, boundary_type=bound))
        surfs.append(Plane(name=id+3, a=0, b=0, c=1, d=mbody.z1, boundary_type=bound))
        surfs.append(Plane(name=id+4, a=0, b=0, c=1, d=mbody.z0, boundary_type=bound))
    elif mbody.z0 == mbody.z1:
        surfs.append(Plane(name=id+1, a=1, b=0, c=0, d=mbody.x1, boundary_type=bound))
        surfs.append(Plane(name=id+2, a=1, b=0, c=0, d=mbody.x0, boundary_type=bound))
        surfs.append(Plane(name=id+3, a=0, b=1, c=0, d=mbody.y1, boundary_type=bound))
        surfs.append(Plane(name=id+4, a=0, b=1, c=0, d=mbody.y0, boundary_type=bound))
    else:
        surfs.append(Plane(name=id+1, a=1, b=0, c=0, d=mbody.x1, boundary_type=bound))
        surfs.append(Plane(name=id+2, a=1, b=0, c=0, d=mbody.x0, boundary_type=bound))
        surfs.append(Plane(name=id+3, a=0, b=1, c=0, d=mbody.y1, boundary_type=bound))
        surfs.append(Plane(name=id+4, a=0, b=1, c=0, d=mbody.y0, boundary_type=bound))
        surfs.append(Plane(name=id+5, a=0, b=0, c=1, d=mbody.z1, boundary_type=bound))
        surfs.append(Plane(name=id+6, a=0, b=0, c=1, d=mbody.z0, boundary_type=bound))

    if len(surfs) == 6:
        region_pos = +surfs[0] | -surfs[1] | +surfs[2] | -surfs[3] | +surfs[4] | -surfs[5]
        region_neg = -surfs[0] & +surfs[1] & -surfs[2] & +surfs[3] & -surfs[4] & +surfs[5]
    else:
        region_pos = +surfs[0] | -surfs[1] | +surfs[2] | -surfs[3]
        region_neg = -surfs[0] & +surfs[1] & -surfs[2] & +surfs[3]

    return (surfs, region_pos, region_neg)

def rcc(mbody:RCC):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    base = np.array([mbody.base.x, mbody.base.y, mbody.base.z])
    axis = np.array([mbody.axis.x, mbody.axis.y, mbody.axis.z])
    p = [axis[0]+base[0], axis[1]+base[1], axis[2]+base[2]]
    h = (axis[0]**2 + axis[1]**2 + axis[2]**2)**0.5
    
    # Calculating coeffs for quadric surface (an inf cylinder)
    a = []
    b = []
    c = []
    a.append(base[2]-p[2])
    a.append(p[1]-base[1]) #axis[1]
    a.append(base[1]*p[2] - base[2]*p[1]) #axis[1]

    b.append(p[2]-base[2])
    b.append(base[0]-p[0]) #axis[0]
    b.append(base[2]*p[1] - base[0]*p[2]) #base[2]*p[1]

    c.append(base[1]-p[1]) #-axis[1]
    c.append(p[0]-base[0]) #axis[0]
    c.append(base[0]*p[1] - base[1]*p[0]) #axis[0]

    _a = b[0]**2 + c[0]**2
    _b = a[0]**2 + c[1]**2
    _c = a[1]**2 + c[1]**2
    _d = 2*c[0]*c[1]
    _e = 2*a[0]*a[1]
    _f = 2*b[0]*b[1]
    _g = 2*b[0]*b[2]*c[0]*c[2]
    _h = 2*a[0]*a[2]*c[1]*c[2]
    _j = 2*a[1]*a[2]*b[1]*b[2]
    _k = a[2]**2 + b[2]**2 + c[2]**2 - (mbody.r**2 * h**2)

    r = (axis[0]**2 + axis[1]**2 + axis[2]**2)**0.5
    sc8 = axis[0] / r
    sc9 = axis[1] / r
    sc10 = axis[2] / r
    r = base[0]**2 + base[1]**2 + base[2]**2
    scf1 = 1 - sc8**2
    scf2 = 1 - sc9**2
    scf3 = 1 - sc10**2
    scf4 = -2*sc8*sc9
    scf5 = -2*sc9*sc10
    scf6 = -2*sc8*sc10
    scf7 = -base[1]*scf4-base[2]*scf6-2*base[0]*scf1
    scf8 = -base[0]*scf4-base[2]*scf5-2*base[1]*scf2
    scf9 = -base[0]*scf6-base[1]*scf5-2*base[2]*scf3
    scf10 = base[0]*base[1]*scf4+base[1]*base[2]*scf5+base[0]*base[2]*scf6+base[0]**2*scf1+base[1]**2*scf2+base[2]**2*scf3-mbody.r**2
    

    # Normalize
    norm = max(abs(_a), abs(_b), abs(_c), abs(_d), abs(_e), abs(_f), abs(_g), abs(_h), abs(_j), abs(_k))
    plane_norm = max([abs(axis[0]), abs(axis[1]), abs(axis[2])])

    # Bottom plane
    d_base = ((axis[0]*base[0]) + (axis[1]*base[1]) + (axis[2]*base[2]))
    # Top plane
    d_top = ((axis[0]*p[0]) + (axis[1]*p[1]) + (axis[2]*p[2]))

    #surfs.append(Quadric(name=id+1, boundary_type=bound, a=_a/norm, b=_b/norm, c=_c/norm, d=_d/norm, 
    #    e=_e/norm, f=_f/norm, g=_g/norm, h=_h/norm, j=_j/norm, k=_k/norm))
    surfs.append(Quadric(name=id+1, boundary_type=bound, a=scf1, b=scf2, c=scf3, d=scf4, 
        e=scf5, f=scf6, g=scf7, h=scf8, j=scf9, k=scf10))
    surfs.append(Plane(name=id+2, boundary_type=bound, a=axis[0]/plane_norm, b=axis[1]/plane_norm, 
        c=axis[2]/plane_norm, d=d_base/plane_norm))
    surfs.append(Plane(name=id+3, boundary_type=bound, a=axis[0]/plane_norm, b=axis[1]/plane_norm, 
        c=axis[2]/plane_norm, d=d_top/plane_norm))

    s_top = s_top = axis[0]*base[0] + axis[1]*base[1] + axis[2]*base[2] - d_top
    if s_top < 0:
        region_pos = +surfs[0] | -surfs[1] | +surfs[2]
        region_neg = -surfs[0] & +surfs[1] & -surfs[2]
    else:
        region_pos = +surfs[0] | +surfs[1] | -surfs[2]
        region_neg = -surfs[0] & -surfs[1] & +surfs[2]

    return (surfs, region_pos, region_neg)

def hex(mbody:HEX):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    base = np.array([mbody.base.x, mbody.base.y, mbody.base.z])
    height = np.array([mbody.height.x, mbody.height.y, mbody.height.z])
    facets = [[mbody.facet1.x, mbody.facet1.y, mbody.facet1.z]]

    if mbody.facet2 is not None:
        facets.append([mbody.facet2.x, mbody.facet2.y, mbody.facet2.z])
    else:
        # Rotate by 60deg from facet1
        theta = math.pi/3
        facets.append(np.dot(rotation_matrix(height, theta), facets[0]))
    
    if mbody.facet3 is not None:
        facets.append([mbody.facet3.x, mbody.facet3.y, mbody.facet3.z])
    else:
        # Rotate by 120deg from facet1
        theta = 2*math.pi/3
        facets.append(np.dot(rotation_matrix(height, theta), facets[0]))
    # Now define the opposing facet vectors.
    theta = math.pi
    for i in range(3,6):
        facets.append(np.dot(rotation_matrix(height, theta), facets[i-3]))

    # Define plane for each facet.
    # Also store their halfspaces.
    region_pos = None
    region_neg = None
    for i in range(6):
        v = facets[i]
        d = 0
        for j in range(3):
            d = d + (base[j]+v[j])*v[j]
        plane_norm = max([abs(v[0]), abs(v[1]), abs(v[2])])
        surfs.append(Plane(name=id+1+i, boundary_type=bound, a=v[0]/plane_norm, b=v[1]/plane_norm, c=v[2]/plane_norm, d=d/plane_norm))

        # Use base point for sense. It will be inside the HEX (negative sense of the macrobody).
        s = v[0]*base[0] + v[1]*base[1] + v[2]*base[2] - d
        if s < 0:
            if region_pos is None:
                region_pos = +surfs[i]
                region_neg = -surfs[i]
            else:
                region_pos |= +surfs[i]
                region_neg &= -surfs[i]
        else:
            if region_pos is None:
                region_pos = -surfs[i]
                region_neg = +surfs[i]
            else:
                region_pos |= -surfs[i]
                region_neg &= +surfs[i]

    # Check if the HEX is infinite.
    h = math.sqrt(height[0]**2 + height[1]**2 + height[2]**2)
    # If infinite, the top and bottom plans are not required.
    if(h < 1.e6):
        plane_norm = max([abs(height[0]), abs(height[1]), abs(height[2])])
        # Define planes for top and bottom.
        d_base = height[0]*base[0] + height[1]*base[1] + height[2]*base[2]
        d_top = height[0]*(height[0]+base[0]) + height[1]*(height[1]+base[1]) + height[2]*(height[2]+base[2])
        surfs.append(Plane(name=id+7, boundary_type=bound, a=height[0]/plane_norm, b=height[1]/plane_norm, 
            c=height[2]/plane_norm, d=d_base/plane_norm))
        surfs.append(Plane(name=id+8, boundary_type=bound, a=height[0]/plane_norm, b=height[1]/plane_norm, 
            c=height[2]/plane_norm, d=d_top/plane_norm))

        s_top = height[0]*base[0] + height[1]*base[1] + height[2]*base[2] - d_top
        # Base point is in negative sense of the "top" plane.
        if s_top < 0:
            region_pos |= -surfs[6] 
            region_pos |= +surfs[7] 
            region_neg &= +surfs[6] 
            region_neg &= -surfs[7]
        else:
            region_pos |= +surfs[6] 
            region_pos |= -surfs[7] 
            region_neg &= -surfs[6] 
            region_neg &= +surfs[7]

    return (surfs, region_pos, region_neg)

def wed(mbody:WED):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    # Vertex of base triangle.
    vertex = np.array([mbody.vertex.x, mbody.vertex.y, mbody.vertex.z])
    # Vector for first side of triangle.
    v1 = np.array([mbody.vectors[0].x, mbody.vectors[0].y, mbody.vectors[0].z])
    # Vector for second side of triangle.
    v2 = np.array([mbody.vectors[1].x, mbody.vectors[1].y, mbody.vectors[1].z])
    # Height vector.
    axis = np.array([mbody.axis.x, mbody.axis.y, mbody.axis.z])

    '''
    Find sets of points used to define planes.
    Side 1: (vertex, vertex+v1, vertex+axis)
    Side 2: (vertex, vertex+v2, vertex+axis)
    Side 3: (vertex+v1, vertex+v2, vertex+v1+axis)
    Base: (vertex, vertex+v1, vertex+v2)
    Top: (vertex+axis, vertex+v1+axis, vertex+v2+axis)
    '''
    points = []
    v_v1 = np.array([vertex[0]+v1[0], vertex[1]+v1[1], vertex[2]+v1[2]])
    v_v2 = np.array([vertex[0]+v2[0], vertex[1]+v2[1], vertex[2]+v2[2]])
    v_axis = np.array([vertex[0]+axis[0], vertex[1]+axis[1], vertex[2]+axis[2]])
    v_v1_axis = np.array([vertex[0]+v1[0]+axis[0], vertex[1]+v1[1]+axis[1], vertex[2]+v1[2]+axis[2]])
    v_v2_axis = np.array([vertex[0]+v2[0]+axis[0], vertex[1]+v2[1]+axis[1], vertex[2]+v2[2]+axis[2]])
    points.append([vertex, v_v1, v_axis])
    points.append([vertex, v_v2, v_axis])
    points.append([v_v1, v_v2, v_v1_axis])
    points.append([vertex, v_v1, v_v2])
    points.append([v_axis, v_v1_axis, v_v2_axis])

    '''
    This is a test point for HS senses. 
    It should be slightly offset from the vertex in the direction
    of the other vectors.
    Vertex + v1 + v2 + axis would produce a 4th point on the top plane
    of the wedge (lying outside of the top triangular face). Traveling 1/2
    the distance to this point would fall on the boundary of the wedge.
    Traveling 1/10 the distance ensures the test point falls within the wedge.
    '''
    hs = []
    region_pos = None
    region_neg = None
    for i in range(3):
        hs.append(0.1 * (vertex[i]+v1[i]+v2[i]+axis[i]))
    #print('HS', hs)
    for i in range(5):
        p1 = points[i][0]
        p2 = points[i][1]
        p3 = points[i][2]

        vec1 = p3-p1
        vec2 = p2-p1
        cp = np.cross(vec1, vec2)
        a, b, c = cp
        d = np.dot(cp, p3)
        plane_norm = max([abs(a), abs(b), abs(c)])
        surfs.append(Plane(name=id+1+i, boundary_type=bound, a=a/plane_norm, b=b/plane_norm, 
            c=c/plane_norm, d=d/plane_norm))
        # Only need to check sense of the sides. Default is outside sense.
        if i < 3:
            s = a*hs[0] + b*hs[1] + c*hs[2] - d
            if s < 0:
                if region_pos is None:
                    region_pos = +surfs[i]
                    region_neg = -surfs[i]
                else:
                    region_pos |= +surfs[i]
                    region_neg &= -surfs[i]
            else:
                if region_pos is None:
                    region_pos = -surfs[i]
                    region_neg = +surfs[i]
                else:
                    region_pos |= -surfs[i]
                    region_neg &= +surfs[i]
        elif i == 4:
            s_top = a*vertex[0] + b*vertex[1] + c*vertex[2] - d
            if s_top < 0:
                region_pos |= -surfs[i-1] 
                region_pos |= +surfs[i]
                region_neg &= +surfs[i-1] 
                region_neg &= -surfs[i]
            else:
                region_pos |= +surfs[i-1] 
                region_pos |= -surfs[i]
                region_neg &= -surfs[i-1] 
                region_neg &= +surfs[i]

    return (surfs, region_pos, region_neg)

def ell(mbody:ELL):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    v1 = np.array([mbody.v1.x, mbody.v1.y, mbody.v1.z])
    v2 = np.array([mbody.v2.x, mbody.v2.y, mbody.v2.z])
    rm = mbody.rm

    # rm == 0 is an invalid radius.
    if rm == 0:
        print('INVALID RADIUS FOR ELL! rm == 0')
    # Negative rm corresponds to minor radius length.
    if rm < 0:
        b2 = rm**2
        a2 = v2[0]**2 + v2[1]**2 + v2[2]**2
        a = math.sqrt(a2)
        u = v2[0]/a
        v = v2[1]/a
        w = v2[2]/a
        x = v1[0]
        y = v1[1]
        z = v1[2]
    
    # Positive rm corresponds to major radius length.
    if rm > 0:
        a2 = rm**2
        c = math.sqrt((v2[0]-v1[0])**2 + (v2[1]-v1[1])**2 + (v2[2]-v1[2])**2)
        if c <= 0 :
            print('INVALID FOCI FOR ELL!')
        u = (v2[0]-v1[0])/c
        v = (v2[1]-v1[1])/c
        w = (v2[2]-v1[2])/c
        b2 = a2 - (c*0.5)**2
        if b2 <= 0:
            print('INVALID FOCI FOR ELL!')
        x = 0.5*(v1[0]+v2[0])
        y = 0.5*(v1[1]+v2[1])
        z = 0.5*(v1[2]+v2[2])

    am = b2-a2
    du = a2 + (am*u**2)
    dv = a2 + (am*v**2)
    dw = a2 + (am*w**2)

    _d = 2.0*u*v*am
    _e = 2.0*v*w*am
    _f = 2.0*u*w*am
    _g = -2.0*(x*du + u*v*y*am + u*w*z*am)
    _h = -2.0*(y*dv + u*v*x*am + v*w*z*am)
    _j = -2.0*(z*dw + u*w*x*am + v*w*y*am)
    _k = du*x**2 + dv*y**2 + dw*z**2 + 2.0*x*y*u*v*am + 2.0*y*z*v*w*am + 2.0*x*z*u*w*am - a2*b2
    norm = max(abs(du), abs(dv), abs(dw), abs(_d), abs(_e), abs(_f), abs(_g), abs(_h), abs(_j), abs(_k))

    surfs.append(Quadric(name=id+1, boundary_type=bound, a=du/norm, b=dv/norm, c=dw/norm, d=_d/norm, 
        e=_e/norm, f=_f/norm, g=_g/norm, h=_h/norm, j=_j/norm, k=_k/norm))
    
    return (surfs, +surfs[0], -surfs[0])

def rec(mbody:REC):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    base = np.array([mbody.base.x, mbody.base.y, mbody.base.z])
    axis = np.array([mbody.axis.x, mbody.axis.y, mbody.axis.z])
    v1 = np.array([mbody.v1.x, mbody.v1.y, mbody.v1.z])
    p = np.array([axis[0]+base[0], axis[1]+base[1], axis[2]+base[2]])

    if mbody.v2 is not None:
        v2 = np.array([mbody.v2.x, mbody.v2.y, mbody.v2.z])
        b2 = v2[0]**2 + v2[1]**2 + v2[2]**2
    else:
        rm = mbody.rm
        b2 = rm**2
    a2 = v1[0]**2 + v1[1]**2 + v1[2]**2
    h2 = axis[0]**2 + axis[1]**2 + axis[2]**2
    
    _a = a2*(1.0 - (axis[0]**2 / h2)) - v1[0]**2 * (1.0 - b2/a2)  
    _b = a2*(1.0 - (axis[1]**2 / h2)) - v1[1]**2 * (1.0 - b2/a2) 
    _c = a2*(1.0 - (axis[2]**2 / h2)) - v1[2]**2 * (1.0 - b2/a2) 
    _d = -2.0*(a2*axis[0]*axis[1]/h2 + v1[0]*v1[1]*(1.0 - b2/a2))
    _e = -2.0*(a2*axis[1]*axis[2]/h2 + v1[1]*v1[2]*(1.0 - b2/a2))
    _f = -2.0*(a2*axis[0]*axis[2]/h2 + v1[0]*v1[2]*(1.0 - b2/a2))
    _g = 2.0*(a2*((axis[0]/h2)*(base[1]*axis[1] + base[2]*axis[2]) 
        - base[0]*((1.0-(axis[0]**2 / h2))-((v1[1]**2 / a2)*(1.0 - b2/a2)))) 
        + (1.0 - b2/a2)*(base[1]*v1[0]*v1[1] + base[2]*v1[1]*v1[2]))
    
    _h = 2.0*(a2*((axis[1]/h2)*(base[0]*axis[0] + base[2]*axis[2]) 
        - base[1]*((1.0-(axis[1]**2 / h2))-((v1[1]**2 / a2)*(1.0 - b2/a2)))) 
        + (1.0 - b2/a2)*(base[0]*v1[0]*v1[1] + base[2]*v1[1]*v1[2]))
    
    _j = 2.0*(a2*((axis[2]/h2)*(base[0]*axis[0] + base[1]*axis[1]) 
        - base[2]*((1.0 - (axis[2]**2 / h2))-((v1[2]**2 / a2)*(1.0 - b2/a2)))) 
        + (1.0 - b2/a2)*(base[0]*v1[0]*v1[2] + base[1]*v1[1]*v1[2]))
    
    _k = (a2*(-2.0*base[0]*base[1]*axis[0]*axis[1]/h2 
            + base[1]*base[2]*axis[1]*axis[2] 
            + base[0]*base[2]*axis[0]*axis[2] 
            + base[0]**2 * (1.0-axis[0]**2 / h2) 
            + base[1]**2 * (1.0-axis[1]**2 / h2) 
            + base[2]**2 * (2.0-axis[2]**2 / h2)) 
        - (1.0 - b2/a2)*((base[0]**2 * v1[0]**2) 
            + (base[1]**2 * v1[1]**2) 
            + (base[2]**2 * v1[2]**2))
        - a2*b2 
        - 2.0*(base[0]*base[1]*v1[0]*v1[1] 
            + base[1]*base[2]*v1[1]*v1[2] 
            + base[0]*base[2]*v1[0]*v1[2])*(1.0 - b2/a2))

    norm = max(abs(_a), abs(_b), abs(_c), abs(_d), abs(_e), abs(_f), abs(_g), abs(_h), abs(_j), abs(_k))
    plane_norm = max([abs(axis[0]), abs(axis[1]), abs(axis[2])])

    # Bottom plane
    d_base = axis[0]*base[0] + axis[1]*base[1] + axis[2]*base[2]
    # Top plane
    d_top = axis[0]*p[0] + axis[1]*p[1] + axis[2]*p[2]
    print(_a,_b,_c,_d,_e,_f,_g,_h,_j,_k)
    surfs.append(Quadric(name=id+1, boundary_type=bound, a=_a/norm, b=_b/norm, c=_c/norm, d=_d/norm, 
        e=_e/norm, f=_f/norm, g=_g/norm, h=_h/norm, j=_j/norm, k=_k/norm))
    print(_a,_b,_c,_d,_e,_f,_g,_h,_j,_k)
    print(surfs[0])
    
    surfs.append(Plane(name=id+2, boundary_type=bound, a=axis[0]/plane_norm, b=axis[1]/plane_norm, 
        c=axis[2]/plane_norm, d=d_base/plane_norm))
    surfs.append(Plane(name=id+3, boundary_type=bound, a=axis[0]/plane_norm, b=axis[1]/plane_norm, 
        c=axis[2]/plane_norm, d=d_top/plane_norm))

    s_top = s_top = axis[0]*base[0] + axis[1]*base[1] + axis[2]*base[2] - d_top
    if s_top < 0:
        region_pos = +surfs[0] | -surfs[1] | +surfs[2]
        region_neg = -surfs[0] & +surfs[1] & -surfs[2]
    else:
        region_pos = +surfs[0] | +surfs[1] | -surfs[2]
        region_neg = -surfs[0] & -surfs[1] & +surfs[2]

    return (surfs, region_pos, region_neg)

def trc(mbody:TRC):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    base = np.array([mbody.base.x, mbody.base.y, mbody.base.z])
    axis = np.array([mbody.axis.x, mbody.axis.y, mbody.axis.z])
    r0 = mbody.r0
    r1 = mbody.r1

    # Define top and bottom planes.
    p = np.array([axis[0]+base[0], axis[1]+base[1], axis[2]+base[2]])
    d_base = axis[0]*base[0] + axis[1]*axis[1] + axis[2]*axis[2]
    d_top = axis[0]*p[0] + axis[1]*p[1] + axis[2]*p[2]
    
    # Find the apex of the non-truncated cone.
    # Distance from base to truncated top.
    d = math.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)
    # Slope of cone.
    #slope = (r1-r0)/d
    # Distance from base to apex (r=0).
    #d_apex = -r0/slope
    d_apex = -r0*d/(r1-r0)
    apex = (d_apex*axis/max(axis)) + base
    #print('APEX:', apex)
    #print('R0:', r0)
    #print('D_APEX:', d_apex)
    r2=(r0/d_apex)**2
    x0, y0, z0 = apex
    dx, dy, dz = axis/max(axis)
    cos2 = 1 / (1+r2)
    a = cos2 - dx*dx
    b = cos2 - dy*dy
    c = cos2 - dz*dz
    d = -2*dx*dy
    e = -2*dy*dz
    f = -2*dx*dz
    g = 2*(dx*(dy*y0 + dz*z0) - a*x0)
    h = 2*(dy*(dx*x0 + dz*z0) - b*y0)
    j = 2*(dz*(dx*x0 + dy*y0) - c*z0)
    k = a*x0*x0 + b*y0*y0 + c*z0*z0 - 2*(dx*dy*x0*y0 + dy*dz*y0*z0 +
                                            dx*dz*x0*z0)
    norm = max(abs(a), abs(b), abs(c), abs(d), abs(e), abs(f), abs(g), abs(h), abs(j), abs(k))
    plane_norm = max([abs(axis[0]), abs(axis[1]), abs(axis[2])])

    surfs.append(Quadric(name=id+1, boundary_type=bound, a=a/norm, b=b/norm, c=c/norm, d=d/norm, 
        e=e/norm, f=f/norm, g=g/norm, h=h/norm, j=j/norm, k=k/norm))
    surfs.append(Plane(name=id+2, boundary_type=bound, a=axis[0]/plane_norm, b=axis[1]/plane_norm, 
        c=axis[2]/plane_norm, d=d_base/plane_norm))
    surfs.append(Plane(name=id+3, boundary_type=bound, a=axis[0]/plane_norm, b=axis[1]/plane_norm, 
        c=axis[2]/plane_norm, d=d_top/plane_norm))

    s_top = s_top = axis[0]*base[0] + axis[1]*base[1] + axis[2]*base[2] - d_top
    if s_top < 0:
        region_pos = +surfs[0] | -surfs[1] | +surfs[2]
        region_neg = -surfs[0] & +surfs[1] & -surfs[2]
    else:
        region_pos = +surfs[0] | +surfs[1] | -surfs[2]
        region_neg = -surfs[0] & -surfs[1] & +surfs[2]

    return (surfs, region_pos, region_neg)

def box(mbody:BOX):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    corner = np.array([mbody.corner.x, mbody.corner.y, mbody.corner.z])
    # BOX can be infinite in 1 dimension meaning 2 instead of 3 vectors.
    vectors = mbody.vectors
    region_pos = None
    region_neg = None

    for i in range(len(vectors)):
        vector = vectors[i]
        v = np.array([vector.x, vector.y, vector.z]) 
        p = np.array([corner[0]+v[0], corner[1]+v[1], corner[2]+v[2]])
        d1 = v[0]*corner[0] + v[1]*corner[1] + v[2]*corner[2]
        d2 = v[0]*p[0] + v[1]*p[1] + v[2]*p[2]
        plane_norm = max([abs(v[0]), abs(v[1]), abs(v[2])])
        surfs.append(Plane(name=id+1+(i*2), boundary_type=bound, a=v[0]/plane_norm, b=v[1]/plane_norm, 
        c=v[2]/plane_norm, d=d1/plane_norm))
        surfs.append(Plane(name=id+2+(i*2), boundary_type=bound, a=v[0]/plane_norm, b=v[1]/plane_norm, 
        c=v[2]/plane_norm, d=d2/plane_norm))
        
        # Check HS senses.
        hs = corner + 0.5*v
        s = v[0]*hs[0] + v[1]*hs[1] + v[2]*hs[2] - d1
        if s < 0:
            if region_pos is None:
                region_pos = +surfs[i]
                region_neg = -surfs[i]
            else:
                region_pos |= +surfs[i]
                region_neg &= -surfs[i]
        else:
            if region_pos is None:
                region_pos = -surfs[i]
                region_neg = +surfs[i]
            else:
                region_pos |= -surfs[i]
                region_neg &= +surfs[i]

    return (surfs, region_pos, region_neg)

def arb(mbody:ARB):
    surfs = []
    id = int(mbody.name)
    bound = mbody.boundary_type
    corners = mbody.corners
    points = []
    ids = []
    region_pos = None
    region_neg = None

    for i in range(len(corners)):
        points.append(np.array([corners[i].x, corners[i].y, corners[i].z]))
    sides = mbody.sides
    for i in range(len(sides)):
        # Each side is a 4 digit INT where each digit corresponds to a corner.
        # Only 3 points are required to define planes.
        if sides[i] != 0:
            side = str(sides[i])
            #print('SIDE:',side)
            # These IDs can be used to reference the points stored in corner_points.
            ids.append([int(side[0]), int(side[1]), int(side[2])])

    '''
    For determining the HS sense test point, a point and vectors for 3 edges 
    intersecting at that point are needed. 
    '''
    v1 = [points[1][0]-points[0][0], points[1][1]-points[0][1], points[1][2]-points[0][2]]
    v2 = [points[2][0]-points[0][0], points[2][1]-points[0][1], points[2][2]-points[0][2]]
    v3 = [points[3][0]-points[0][0], points[3][1]-points[0][1], points[3][2]-points[0][2]]
    hs = []
    for i in range(3):
        hs.append(0.1 * (points[0][i]+v1[i]+v2[i]+v3[i]))

    for i in range(len(ids)):
        index = ids[i]
        p1 = np.asarray(points[index[0]-1])
        p2 = np.asarray(points[index[1]-1])
        p3 = np.asarray(points[index[2]-1])
        vec1 = p3-p1
        vec2 = p2-p1
        #print(p1,p2,p3)
        cp = np.cross(vec1, vec2)
        a, b, c = cp
        d = np.dot(cp, p3)
        plane_norm = max([abs(a), abs(b), abs(c)])
        surfs.append(Plane(name=id+1+i, boundary_type=bound, a=a/plane_norm, b=b/plane_norm, 
            c=c/plane_norm, d=d/plane_norm))

        s = a*hs[0] + b*hs[1] + c*hs[2] - d
        if s < 0:
            if region_pos is None:
                region_pos = +surfs[i]
                region_neg = -surfs[i]
            else:
                region_pos |= +surfs[i]
                region_neg &= -surfs[i]
        else:
            if region_pos is None:
                region_pos = -surfs[i]
                region_neg = +surfs[i]
            else:
                region_pos |= -surfs[i]
                region_neg &= +surfs[i]

    return (surfs, region_pos, region_neg)

def decomp(mbody):
    if isinstance(mbody, RPP):
        surfs, region_pos, region_neg = rpp(mbody)
    elif isinstance(mbody, RCC):
        surfs, region_pos, region_neg = rcc(mbody)
    elif isinstance(mbody, HEX):
        surfs, region_pos, region_neg = hex(mbody)
    elif isinstance(mbody, WED):
        surfs, region_pos, region_neg = wed(mbody)
    elif isinstance(mbody, ELL):
        surfs, region_pos, region_neg = ell(mbody)
    elif isinstance(mbody, REC):
        surfs, region_pos, region_neg = rec(mbody)
    elif isinstance(mbody, TRC):
        surfs, region_pos, region_neg = trc(mbody)
    elif isinstance(mbody, BOX):
        surfs, region_pos, region_neg = box(mbody)
    elif isinstance(mbody, ARB):
        surfs, region_pos, region_neg = arb(mbody)
    else:
        print('ERROR! The object "' + str(mbody) + '" is not a valid macrobody.')
    if mbody.transformation is not None:
        for i in range(len(surfs)):
            surfs[i].transformation = mbody.transformation
    
    return (surfs, region_pos, region_neg)
