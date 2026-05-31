def read_data(file_name: str = "data.txt"):
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header = lines[0].split()
    x_values = [float(val) for val in header[1:]]

    data = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split()
        y = float(parts[0])
        z_values = [float(val) for val in parts[1:]]
        
        for x, z in zip(x_values, z_values):
            data.append((x, y, z))
            
    return data