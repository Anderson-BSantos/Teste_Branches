import pandas as pd

# Planejamento de equipe por mês
equipe_fases = {
    "Mês": list(range(1, 25)),
    "Desenvolvedor SIG": [1]*6 + [1]*6 + [2]*12,
    "Dev Front-End / Dashboards": [1]*6 + [1]*6 + [1]*12,
    "Tech Lead / CTO": [1]*6 + [1]*6 + [1]*12,
    "Analista de Dados Pleno": [1]*6 + [1]*6 + [1]*12,
    "Cientista de Dados / DBA": [0]*6 + [1]*6 + [1]*12,
    "Dev Back-End": [0]*6 + [1]*6 + [1]*12,
    "UX/UI Designer": [0]*6 + [0.5]*6 + [0.5]*12,
    "Analista de Dados Júnior": [0]*12 + [1]*12,
    "Gerente de Projetos": [0]*12 + [1]*12,
}

salarios = {
    "Desenvolvedor SIG": 9000,
    "Dev Front-End / Dashboards": 8000,
    "Tech Lead / CTO": 15000,
    "Analista de Dados Pleno": 10000,
    "Cientista de Dados / DBA": 11000,
    "Dev Back-End": 10000,
    "UX/UI Designer": 7000,
    "Analista de Dados Júnior": 6000,
    "Gerente de Projetos": 12000,
}

# Criando DataFrame
df = pd.DataFrame(equipe_fases)

# Calcula o custo mensal
for cargo in salarios:
    df[f"Custo {cargo} (R$)"] = df[cargo] * salarios[cargo]

df["Custo Total Mensal (R$)"] = df[[col for col in df.columns if "Custo" in col]].sum(axis=1)
df["Custo Acumulado (R$)"] = df["Custo Total Mensal (R$)"].cumsum()

# Exportar para Excel
df.to_excel("planejamento_equipes_SIG_dashboards.xlsx", index=False)
print("Arquivo gerado: planejamento_equipes_SIG_dashboards.xlsx")
