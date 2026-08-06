from pathlib import Path
import pandas as pd

# ==========================================
# CONFIGURAÇÕES
# ==========================================

ARQUIVO_CSV = Path(r"C:\Users\BR0450988468\Documents\GitHub\DASH_MEDIDORES\base\base.csv")

INSTALACAO_PROCURADA = "0056429690"


# ==========================================
# LEITURA DA BASE
# ==========================================

df = pd.read_csv(
    ARQUIVO_CSV,
    sep=None,
    engine="python",
    dtype=str,
    encoding="utf-16"
    
)

# Remove espaços e garante que tudo seja string
df["INSTALACAO"] = (
    df["INSTALACAO"]
    .astype(str)
    .str.strip()
)

instalacao = INSTALACAO_PROCURADA.strip()

resultado = df[df["INSTALACAO"] == instalacao]


# ==========================================
# RESULTADO
# ==========================================

if resultado.empty:
    print(f"❌ Instalação {instalacao} NÃO encontrada.")
else:
    print(f"✅ Instalação {instalacao} encontrada!")
    print(f"Foram encontrados {len(resultado)} registro(s).\n")

    print(resultado)