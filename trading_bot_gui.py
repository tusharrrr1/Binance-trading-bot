import tkinter as tk
from tkinter import ttk, messagebox
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import logging

# Replace with your Binance Futures Testnet API keys
API_KEY = "7288968afa01a59b22ab734e36bf8ee7c3605359bab37afd7705caef80283120"
API_SECRET = "8afab34f33932e1d3dd679eae265c46b818aa6c6b0749d445cc8d2dc3edef5c5"

# Setup logging
logging.basicConfig(
    filename="trading_bot_gui.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Binance Futures Testnet client
client = Client(API_KEY, API_SECRET)
client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'


def place_order():
    symbol = symbol_var.get().upper()
    side = side_var.get().upper()
    order_type_name = order_type_var.get().upper()
    quantity = qty_var.get()
    price = price_var.get()
    stop_price = stop_var.get()

    try:
        order_type_map = {
            "MARKET": ORDER_TYPE_MARKET,
            "LIMIT": ORDER_TYPE_LIMIT,
            "STOP_LIMIT": ORDER_TYPE_STOP  # Futures stop-limit type
        }

        order_type = order_type_map.get(order_type_name)
        if not order_type:
            raise ValueError("Invalid order type selected.")

        params = {
            'symbol': symbol,
            'side': SIDE_BUY if side == "BUY" else SIDE_SELL,
            'type': order_type,
            'quantity': float(quantity)
        }

        if order_type == ORDER_TYPE_LIMIT:
            if not price:
                raise ValueError("Limit price is required for LIMIT orders.")
            params['price'] = float(price)
            params['timeInForce'] = TIME_IN_FORCE_GTC

        elif order_type == ORDER_TYPE_STOP:
            if not price or not stop_price:
                raise ValueError("Both stop price and limit price are required for STOP_LIMIT orders.")
            params['stopPrice'] = float(stop_price)
            params['price'] = float(price)
            params['timeInForce'] = TIME_IN_FORCE_GTC

        order = client.futures_create_order(**params)
        logging.info(f"Order placed: {order}")
        messagebox.showinfo("✅ Order Placed", f"Order ID: {order['orderId']}\nStatus: {order['status']}")

    except BinanceAPIException as e:
        logging.error(f"Binance API error: {e}")
        messagebox.showerror("❌ API Error", str(e))
    except ValueError as ve:
        logging.error(f"Value error: {ve}")
        messagebox.showerror("❗ Input Error", str(ve))
    except Exception as ex:
        logging.error(f"General error: {ex}")
        messagebox.showerror("❌ Error", str(ex))


# GUI Setup
root = tk.Tk()
root.title("Binance Futures Testnet Trading Bot")
root.geometry("400x420")
root.resizable(False, False)

# Variables
symbol_var = tk.StringVar(value="BTCUSDT")
side_var = tk.StringVar(value="BUY")
order_type_var = tk.StringVar(value="MARKET")
qty_var = tk.StringVar()
price_var = tk.StringVar()
stop_var = tk.StringVar()

# Widgets
tk.Label(root, text="🔹 Symbol (e.g., BTCUSDT)").pack(pady=2)
tk.Entry(root, textvariable=symbol_var).pack()

tk.Label(root, text="🔹 Side").pack(pady=2)
ttk.Combobox(root, textvariable=side_var, values=["BUY", "SELL"]).pack()

tk.Label(root, text="🔹 Order Type").pack(pady=2)
ttk.Combobox(root, textvariable=order_type_var, values=["MARKET", "LIMIT", "STOP_LIMIT"]).pack()

tk.Label(root, text="🔹 Quantity").pack(pady=2)
tk.Entry(root, textvariable=qty_var).pack()

tk.Label(root, text="🔹 Limit Price (for LIMIT or STOP_LIMIT)").pack(pady=2)
tk.Entry(root, textvariable=price_var).pack()

tk.Label(root, text="🔹 Stop Price (for STOP_LIMIT)").pack(pady=2)
tk.Entry(root, textvariable=stop_var).pack()

tk.Button(root, text="✅ Place Order", bg="green", fg="white", command=place_order).pack(pady=15)

tk.Label(root, text="Note:\nMarket orders don't need price or stop price.\nLimit and Stop-Limit orders require price.\nStop-Limit also requires stop price.", fg="gray").pack(pady=5)

root.mainloop()
