import numpy as np

def run_simulation(seed: int, n_samples: int = 10000) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    
    # Inputs
    x = rng.normal(0.0, 1.0, (n_samples, 2))
    z = x[:, 0]**2 + x[:, 1]**2
    y = np.cos(z)
    
    # Target standard deviations
    sigma_S = 0.1
    sigma_A = sigma_S / np.sqrt(2)
    sigma_B = sigma_S / np.sqrt(2)
    
    # Single layer simulation
    eta_G = rng.normal(0.0, sigma_S, n_samples)
    e_S = np.abs(eta_G)
    mae_S = float(np.mean(e_S))
    
    # Two layer simulation
    eta_A = rng.normal(0.0, sigma_A, n_samples)
    eta_B = rng.normal(0.0, sigma_B, n_samples)
    
    z_approx = z + eta_A
    y_approx = np.cos(z_approx) + eta_B
    e_AB = np.abs(y - y_approx)
    mae_AB = float(np.mean(e_AB))
    
    delta = (mae_S - mae_AB) / mae_S * 100.0
    return mae_S, mae_AB, delta

if __name__ == "__main__":
    print(f"{'seed':<6} | {'e_S':<8} | {'e_AB':<8} | {'delta':<8} | {'PASS/FAIL'}")
    print("-" * 50)
    for seed in range(6):
        e_S, e_AB, delta = run_simulation(seed)
        status = "PASS" if delta >= 10.0 else "FAIL"
        print(f"{seed:<6} | {e_S:<8.4f} | {e_AB:<8.4f} | {delta:<8.2f}% | {status}")
