def load_table(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    data = {}
    z_vals = []
    current_z = None
    x_vals = None
    y_vals = []
    
    for line in lines:
        if line.startswith('z='):
            current_z = int(line.split('=')[1].strip())
            z_vals.append(current_z)
            x_vals = None
            continue
        
        parts = line.split()
        if not parts:
            continue
        
        if parts[0] == 'y\\x' or (current_z is not None and x_vals is None and all(p.lstrip('-').isdigit() for p in parts)):
            x_vals = [int(v) for v in parts if v != 'y\\x']
            continue
        
        if current_z is not None and x_vals is not None and len(parts) >= 2:
            y = int(parts[0])
            if y not in y_vals:
                y_vals.append(y)
            values = [int(v) for v in parts[1:]]
            
            if current_z not in data:
                data[current_z] = {}
            
            for x, val in zip(x_vals, values):
                data[current_z][(y, x)] = val
    
    z_vals.sort()
    y_vals.sort()
    x_vals.sort()
    
    table_3d = []
    for z in z_vals:
        layer = []
        for y in y_vals:
            row = [data[z][(y, x)] for x in x_vals]
            layer.append(row)
        table_3d.append(layer)
    
    return table_3d, (x_vals, y_vals, z_vals)
