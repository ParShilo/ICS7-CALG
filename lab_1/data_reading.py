def read_1d_table(file):
    data = []
    line = file.readline()
    while line and line[0] != '#':
        parts = line.split()
        x = float(parts[1])
        y = float(parts[2])
        data.append((x, y))
        line = file.readline()

    return data

def read_I_table(file):
    data = []
    line = file.readline()
    while line and line[0] != '#':
        parts = line.split()
        x = float(parts[1])
        y = 0.6 * float(parts[2])
        data.append((x, y))
        line = file.readline()

    return data

def read_2d_table(file):
    line = file.readline()
    all_y = list(map(float, line.split()))

    data = []
    line = file.readline()
    while line != '' and line[0] != '#':
        float_line = list(map(float, line.split()))
        x = float_line[0]
        for y, z in zip(all_y, float_line[1:]):
            data.append((x, y, z))

        line = file.readline()

    return data


def read_data(filename="data.txt"):
    with open(filename, 'r') as f:
        f.readline()

        I_table = read_I_table(f)
        Nh_table = read_2d_table(f)
        G_table = read_2d_table(f)
        c_table = read_2d_table(f)
        q_table = read_2d_table(f)

        return (I_table, Nh_table, G_table, c_table, q_table)