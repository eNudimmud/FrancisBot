import asyncio
import websockets

async def test_ws():
    uri = "wss://proportionate-green-spree.solana-mainnet.quiknode.pro/ffd4d3e7fc85d7111ee510f91311e87a3a3ba311/"
    try:
        async with websockets.connect(uri) as ws:
            print("Connexion réussie !")
            await ws.send('{"jsonrpc":"2.0","id":1,"method":"getHealth"}')
            response = await ws.recv()
            print("Réponse :", response)
    except Exception as e:
        print(f"Erreur WebSocket : {e}")

asyncio.run(test_ws())
