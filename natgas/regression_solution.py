# Model: f(x) = θ₀ + θ₁x + θ₂sin(2πx/365) + θ₃cos(2πx/365)

import pandas as pd
import numpy as np

def polysin_features(X, K):
    X = X.flatten()
    N = X.shape[0]
    Phi = np.zeros((N, K + 3))
    for k in range(K + 1):
        Phi[:, k] = X**k
    Phi[:, K + 1] = np.sin((2 * np.pi * X) / 365)
    Phi[:, K + 2] = np.cos((2 * np.pi * X) / 365)
    return Phi

# Load and train
K = 1
df = pd.read_csv(r'natgas\Nat_Gas.csv')
df['Prices'] = pd.to_numeric(df['Prices'], errors='coerce')
df['Dates'] = pd.to_datetime(df['Dates'], errors='coerce')
start_date = df['Dates'].min()
X = np.array((df['Dates'] - start_date) / np.timedelta64(1, 'D')).reshape(-1, 1)
y = np.array(df['Prices']).reshape(-1, 1)
Phi = polysin_features(X, K)
theta = np.linalg.inv(Phi.T @ Phi + 1e-08 * Phi.shape[1]) @ Phi.T @ y

def estimate_price(date_string):
    days = (pd.to_datetime(date_string) - start_date) / np.timedelta64(1, 'D')
    return (polysin_features(np.array([[days]]), K) @ theta)[0, 0]

if __name__ == '__main__':
    date = input("Enter date (MM/DD/YYYY): ")
    print(f"Estimated price: ${estimate_price(date):.2f}")