import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging
from sklearn.preprocessing import StandardScaler

# Carregar dados do CSV
df_hoteis = pd.read_csv('hoteis_bahia_IBGE1.csv', sep=';')
print("Colunas do CSV original:", df_hoteis.columns.tolist())
print("Primeiras linhas do CSV:\n", df_hoteis.head())

# Se o merge não for necessário, podemos usar df_hoteis diretamente
df = df_hoteis.copy()

# Verificar colunas disponíveis
print("Colunas do DataFrame:", df.columns.tolist())

# Remover linhas com valores faltantes
required_columns = ["Longitude", "Latitude", "Diaria"]  # Ajuste para colunas reais
df = df.dropna(subset=required_columns)
print("Após dropna:\n", df.head())

# Preparar dados para krigagem
x = df["Longitude"].values  # Use "Longitude_x" se optar pelo merge
y = df["Latitude"].values   # Use "Latitude_x" se optar pelo merge
z = df["Diaria"].values

# Normalizar os valores de diária
scaler = StandardScaler()
z_scaled = scaler.fit_transform(z.reshape(-1, 1)).flatten()

# Criar grid para interpolação
grid_lon = np.linspace(min(x), max(x), 100)
grid_lat = np.linspace(min(y), max(y), 100)
grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)

# Aplicar Krigagem Ordinária
OK = OrdinaryKriging(
    x, y, z_scaled,
    variogram_model="spherical",
    verbose=True,
    enable_plotting=True
)
z_pred, ss = OK.execute("grid", grid_lon, grid_lat)

# Desnormalizar os resultados
z_pred = scaler.inverse_transform(z_pred.reshape(-5, 5)).reshape(z_pred.shape)

# Plotar o resultado
plt.figure(figsize=(10, 8))
plt.contourf(grid_lon, grid_lat, z_pred, cmap="coolwarm")
plt.colorbar(label="Preço da Diária (R$)")
plt.scatter(x, y, c=z, edgecolor="black", cmap="coolwarm", label="Dados Originais")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Mapa de Krigagem - Preço da Diária de Hotéis na Bahia")
plt.legend()
plt.show()