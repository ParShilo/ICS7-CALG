import matplotlib.pyplot as plt
import numpy as np
import math_actions, data_reading

INITIAL_TIME = 14e-6
FINAL_TIME = 450e-6
TIME_STEP = 1e-6
INITIAL_TEMP = 5400
PX = 0.04
TX = 300.0
TUBE_RADIUS = 0.25
TUBE_LENGTH = 12
CONST_K = 7.242e4

def main():
    t = INITIAL_TIME
    tk = FINAL_TIME
    T = INITIAL_TEMP
    degree = 3

    I_tab, Nh_tab, sigma_tab, c_tab, q_tab = data_reading.read_data()

    K_const = CONST_K * PX / TX

    times = []
    T_vals = []
    p_vals = []
    sigma_vals = []
    q_vals = []
    Rd_vals = []
    Fr_vals = []

    while t <= tk + 1e-10:
        p = math_actions.calculate_p(T, K_const, Nh_tab, degree)
        sigma = math_actions.newton_interpolation_2d(sigma_tab, T, p, degree)
        q = math_actions.newton_interpolation_2d(q_tab, T, p, degree)
        Rd = TUBE_LENGTH / (np.pi * sigma * TUBE_RADIUS**2)
        Fr = q * TUBE_RADIUS / 2

        times.append(t * 1e6)
        T_vals.append(T)
        p_vals.append(p)
        sigma_vals.append(sigma)
        q_vals.append(q)
        Rd_vals.append(Rd)
        Fr_vals.append(Fr)

        T = math_actions.rk2_step(t, T, TIME_STEP, K_const, I_tab, Nh_tab, sigma_tab, q_tab, c_tab, degree, TUBE_RADIUS)
        t += TIME_STEP

    # Построение графиков
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    ax = axes.flatten()

    # Цвета для графиков
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'orange']

    # График T(t)
    ax[0].plot(times, T_vals, color=colors[0])
    ax[0].set_title('T(t)')
    ax[0].set_xlabel('Время t, мкс')
    ax[0].set_ylabel('Температура T, K')
    ax[0].grid(True, linestyle='--', alpha=0.7)

    # График p(t)
    ax[1].plot(times, p_vals, color=colors[1])
    ax[1].set_title('p(t)')
    ax[1].set_xlabel('Время t, мкс')
    ax[1].set_ylabel('Давление p, МПа')
    ax[1].grid(True, linestyle='--', alpha=0.7)

    # График sigma(t)
    ax[2].plot(times, sigma_vals, color=colors[2])
    ax[2].set_title('σ(t)')
    ax[2].set_xlabel('Время t, мкс')
    ax[2].set_ylabel('Электропроводность σ, 1/(Ом·см)')
    ax[2].grid(True, linestyle='--', alpha=0.7)

    # График q(t)
    ax[3].plot(times, q_vals, color=colors[3])
    ax[3].set_title('q(t)')
    ax[3].set_xlabel('Время t, мкс')
    ax[3].set_ylabel('Объемная мощность q, Вт/см³')
    ax[3].grid(True, linestyle='--', alpha=0.7)

    # График Rd(t)
    ax[4].plot(times, Rd_vals, color=colors[4])
    ax[4].set_title('Rd(t)')
    ax[4].set_xlabel('Время t, мкс')
    ax[4].set_ylabel('Сопротивление Rd, Ом')
    ax[4].grid(True, linestyle='--', alpha=0.7)

    # График Fr(t)
    ax[5].plot(times, Fr_vals, color=colors[5])
    ax[5].set_title('Fr(t)')
    ax[5].set_xlabel('Время t, мкс')
    ax[5].set_ylabel('Поток излучения Fr, Вт/см²')
    ax[5].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()