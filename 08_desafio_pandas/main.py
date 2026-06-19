import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("status.csv")

df = df[df["status_code"] != "ERROR"]
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["response_time"] = df["response_time"].astype(float)

print(df)

# # Imprimindo os resultados do monitoramento
# for url in df["url"].unique():
#     dados_url = df[df["url"] == url]
#     print(f"URL: {url}")
#     print(f"Tempo médio de resposta: {dados_url['response_time'].mean():.2f} ms")
#     print(f"Tempo máximo de resposta: {dados_url['response_time'].max():.2f} ms")
#     print(f"Tempo mínimo de resposta: {dados_url['response_time'].min():.2f} ms")
#     print("-" * 40)

plt.figure(figsize=(12,6))

for url in df["url"].unique():
    dados_url = df[df["url"] == url]
    plt.plot(dados_url["timestamp"], dados_url["response_time"], label=url)

plt.title("Tempo de resposta das URLs monitoradas")
plt.xlabel("Tempo")
plt.ylabel("Tempo de resposta")
plt.legend()
plt.grid(True)
plt.show()