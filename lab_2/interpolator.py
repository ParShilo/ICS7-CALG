from newton import newton_interpolation_1d
from spline import cubic_spline_1d

def interpolate_3d(table_3d, coords, target_x, target_y, target_z, method_x='newton', method_y='newton', method_z='newton', degree_x=2, degree_y=2, degree_z=2):
    x_vals, y_vals, z_vals = coords
    
    # Интерполяция по X для всех (y, z) из сетки
    temp_yz = []
    for y_idx, y in enumerate(y_vals):
        row = []
        for z_idx, z in enumerate(z_vals):
            points = [(float(x), float(table_3d[z_idx][y_idx][x_idx])) for x_idx, x in enumerate(x_vals)]
            
            if method_x == 'newton':
                val = newton_interpolation_1d(points, target_x, degree_x)
            else:
                val = cubic_spline_1d(points, target_x)
            row.append(val)
        temp_yz.append(row)
    
    # Интерполяция по Y для всех z
    temp_z = []
    for z_idx, z in enumerate(z_vals):
        points = [(float(y), temp_yz[y_idx][z_idx]) for y_idx, y in enumerate(y_vals)]
        
        if method_y == 'newton':
            val = newton_interpolation_1d(points, target_y, degree_y)
        else:
            val = cubic_spline_1d(points, target_y)
        temp_z.append(val)
    
    # Интерполяция по Z
    points = [(float(z), temp_z[z_idx]) for z_idx, z in enumerate(z_vals)]
    
    if method_z == 'newton':
        result = newton_interpolation_1d(points, target_z, degree_z)
    else:
        result = cubic_spline_1d(points, target_z)
    
    return result


def interpolate_mixed(table_3d, coords, target, spline_axis=0, degree=2):
    methods = ['newton', 'newton', 'newton']
    methods[spline_axis] = 'spline'
    
    return interpolate_3d(table_3d, coords, target[0], target[1], target[2], method_x=methods[0], method_y=methods[1], method_z=methods[2], degree_x=degree, degree_y=degree, degree_z=degree)