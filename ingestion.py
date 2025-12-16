import json
import threading
import websocket
import pandas as pd
from collections import deque

class BinanceWebSocket:
    def __init__(self, symbols):
        self.symbols = symbols
        self.buffer = deque(maxlen=10000)
        self.sockets = []

    def _on_message(self, ws, message):
        try:
            j = json.loads(message)

            # FUTURES raw trade event
            if j.get("e") != "trade":
                return

            tick = {
                "ts": pd.to_datetime(j["T"], unit="ms"),
                "symbol": j["s"],
                "price": float(j["p"]),
                "qty": float(j["q"]),
            }

            self.buffer.append(tick)

        except Exception:
            pass

    def start(self):
        for sym in self.symbols:
            url = f"wss://fstream.binance.com/ws/{sym.lower()}@trade"
            ws = websocket.WebSocketApp(
                url,
                on_message=self._on_message
            )
            t = threading.Thread(target=ws.run_forever, daemon=True)
            t.start()
            self.sockets.append(ws)
