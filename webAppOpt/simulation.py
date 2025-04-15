# simulation.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution, fsolve

# Constants and Parameters
g = 9.81
T_s = 60
T_c = 45
delta_T = T_s - T_c
T_film = (T_s + T_c) / 2
k_aluminum = 237
D, N_r, N_c = 0.01, 24, 2
H = 0.5
W = 0.036
L_array = 0.7
fin_thickness = 0.001
spacing_min = 0.001
spacing_max = 0.05
Q_target = 350

oil_data = {
    "Shell Risella X 430": {'T1': 40, 'nu1': 43.0e-6, 'T2': 100, 'nu2': 7.6e-6},
    "Shell Risella C 415": {'T1': 40, 'nu1': 12.60e-6, 'T2': 100, 'nu2': 3.10e-6},
}

def kinematic_viscosity_interp(T, T1, nu1, T2, nu2):
    log_nu1 = np.log10(nu1)
    log_nu2 = np.log10(nu2)
    log_nu_T = log_nu1 + ((T - T1) / (T2 - T1)) * (log_nu2 - log_nu1)
    return 10**log_nu_T

def compute_rayleigh(g, beta, delta_T, d, nu, alpha):
    return g * beta * delta_T * d**3 / (nu * alpha)

def churchill_chu(Ra_D, Pr):
    Nu_D = (0.60 + (0.387 * Ra_D**(1/6)) / (1 + (0.559 / Pr)**(9/16))**(8/27))**2
    return 0.12 * Nu_D

def compute_nusselt_elenbaas(Ra_s, S_over_L):
    exponent = -35 / (Ra_s * S_over_L)
    Nu_s = (1/24) * Ra_s * S_over_L * (1 - np.exp(exponent))**(0.75)
    return Nu_s

def compute_h(Nu, k, d):
    return Nu * k / d

def compute_fin_efficiency(h, k_fin, t, L):
    m = np.sqrt(2 * h / (k_fin * t))
    mL = m * L
    return np.tanh(mL) / mL

def compute_surface_area(spacing):
    A_base = np.pi * D * N_r * N_c * L_array
    N_channels = int((L_array + spacing) / (spacing + fin_thickness))
    N_fins = N_channels - 1
    A_fin_single = 2 * W * H
    A_fins_total = A_base + N_fins * A_fin_single
    return A_base, A_fins_total

def optimize_fin_spacing(fluid, delta_T):
    def objective(spacing):
        d = spacing[0]
        if not spacing_min <= d <= spacing_max:
            return 1e6
        Ra = compute_rayleigh(g, fluid['beta'], delta_T, d, fluid['nu'], fluid['alpha'])
        Nu = compute_nusselt_elenbaas(Ra, d / H)
        h = compute_h(Nu, fluid['k'], d)
        A_base, A_total = compute_surface_area(d)
        A_fins = A_total - A_base
        eta = compute_fin_efficiency(h, k_aluminum, fin_thickness, H)
        return -h * eta * A_fins * delta_T

    result = differential_evolution(objective, [(spacing_min, spacing_max)], strategy='best1bin', tol=1e-6)
    return result.x[0]

def suggested_spacing(fluid):
    def spacing_eq(S, L):
        Ra = compute_rayleigh(g, fluid['beta'], delta_T, S, fluid['nu'], fluid['alpha'])
        return S - 2.71 * (Ra / (S**3 * L))**(-0.25)
    S_opt = fsolve(spacing_eq, 0.005, args=(H))[0]
    return 1.71 * S_opt

def get_fluid_props(props):
    nu = kinematic_viscosity_interp(T_film, props['T1'], props['nu1'], props['T2'], props['nu2'])
    fluid = {
        'k': 0.13,
        'rho': 828,
        'c_p': 2100,
        'beta': 0.0009,
        'nu': nu,
    }
    fluid['alpha'] = fluid['k'] / (fluid['rho'] * fluid['c_p'])
    fluid['Pr'] = fluid['nu'] / fluid['alpha']
    return fluid
