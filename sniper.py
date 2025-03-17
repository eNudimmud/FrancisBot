import requests
import json
import time

# 🔗 RPC Solana (remplace par ton propre endpoint si nécessaire)
RPC_URL = "https://proportionate-green-spree.solana-mainnet.quiknode.pro/ffd4d3e7fc85d7111ee510f91311e87a3a3ba311/"

# 📂 Fichier de sauvegarde des tokens valides
SAVE_FILE = "new_tokens.json"

# 📌 Fonction pour récupérer les dernières transactions de création de token
def get_latest_transactions():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedSignaturesForAddress2",
        "params": ["11111111111111111111111111111111", {"limit": 100}]  # Address par défaut pour scanner tout Solana
    }
    try:
        response = requests.post(RPC_URL, json=payload)
        return response.json().get("result", [])
    except Exception as e:
        print(f"❌ Erreur HTTP : {e}")
        return []

# 📌 Fonction pour vérifier si une transaction est une création de token
def is_new_token(tx_signature):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [tx_signature, "json"]
    }
    try:
        response = requests.post(RPC_URL, json=payload)
        data = response.json().get("result", {})
        instructions = data.get("transaction", {}).get("message", {}).get("instructions", [])

        for instruction in instructions:
            if instruction.get("programId") == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA":
                return instruction.get("parsed", {}).get("info", {}).get("mint")
        return None
    except Exception as e:
        print(f"❌ Erreur HTTP (getTransaction) : {e}")
        return None

# 📌 Fonction pour récupérer la liquidité d'un token
def get_token_liquidity(token_address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenSupply",
        "params": [token_address]
    }
    try:
        response = requests.post(RPC_URL, json=payload)
        return response.json().get("result", {}).get("value")
    except Exception as e:
        print(f"❌ Erreur HTTP (getTokenSupply) : {e}")
        return None

# 📌 Fonction principale du scanner
def scanner():
    print("🚀 Scanner de nouveaux tokens en cours d'exécution...")

    while True:
        latest_txs = get_latest_transactions()
        new_tokens = []

        for tx in latest_txs:
            tx_signature = tx.get("signature")
            new_token = is_new_token(tx_signature)

            if new_token:
                liquidity = get_token_liquidity(new_token)
                if liquidity and float(liquidity) > 10000:  # Filtre : minimum 10K tokens en supply
                    print(f"✅ Nouveau token détecté : {new_token} (Liquidité : {liquidity})")
                    new_tokens.append({"token": new_token, "liquidity": liquidity})

        # Sauvegarde les tokens valides
        if new_tokens:
            with open(SAVE_FILE, "w") as f:
                json.dump(new_tokens, f, indent=4)

        time.sleep(10)  # Pause pour éviter le spam API

# Lancer le scanner
if __name__ == "__main__":
    scanner()
