import threading
import time
import random
import socket
from config import ORDERS, TABLES, MENU

HEADER = 64
PORT = 8080
SERVER = "127.0.0.1"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (HEADER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(ADDR)


def generate_order():
    while True:
        time.sleep(1)
        for idx, tables in enumerate(TABLES):
            if tables['state'] == 'TABLE_FREE':
                max_wait_time = 0
                items = []
                for i in range(random.randint(1, 5)):
                    food = random.choice(MENU)
                    if max_wait_time < food['preparation-time']:
                        max_wait_time = food['preparation-time']
                    items.append(food['id'])
                max_wait_time  = round(max_wait_time * 1.3)

                new_order_id = len(ORDERS)
                ORDERS.append({
                    "id" : new_order_id,
                    "items" : items,
                    "priority" : random.randint(1, 5),
                    "max_wait" : max_wait_time
                })
                return True

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def send_order(ORDERS):
    client.listen()
    threads=[]
    l=len(threads)
    length= len(ORDERS)
    for i in range(0,length):
        threads[i] = threading.Thread(target=handle_client_kitchen,args=(ORDERS[l]))

def handle_client_kitchen(ORDERS):
    print(f"[NEW CONNECTION] KITCHEN connected.")
    connected = True
    while connected:
        for i in range(0,len(ORDERS)):
            for idx in enumerate(ORDERS):
                send(ORDERS[idx][i])

send("Connection to the server!")
generate_order()
send_order(ORDERS)
send(DISCONNECT_MESSAGE)