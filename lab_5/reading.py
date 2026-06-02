def read_data(file_name: str="data.txt"):
    f = open(file_name, "r")

    line = f.readline()
    data = []
    x_values = list(map(float, line.split()[1:]))

    while line := f.readline():
        line_data = line.split()
        y = float(line_data[0])
        z_values = list(map(float, line_data[1:]))

        for x, z in zip(x_values, z_values):
            data.append((x, y, z))

    f.close()

    return data
