import threading
import time
import random
import config as config
from flask import Flask, request
import requests
import queue

app = Flask(__name__)
threads = []

@app.route('/distribution', methods=['POST'])

def distribution():
    order = request.get_json()
    print(f'Received order from the kitchen. orderId: {order["order_id"]} items: {order["items"]}') 
    table_id = next((i for i, table in enumerate(config.TABLES) if table['id'] == order['table_id']), None)
    config.TABLES[table_id]['state'] = config.TABLE_STATE_2

    waiter_thread: Waiter = next((w for w in threads if type(w) == Waiter and w.id == order['waiter_id']), None)
    waiter_thread.serve_order(order)  
    return {'isSuccess': True}


class Waiter(threading.Thread):
    def __init__(self, info, *args, **kwargs):
        super(Waiter, self).__init__(*args, **kwargs)
        self.name = info['name']
        self.id = info['id']
        self.daemon = True

    def run(self):
        while True:
            self.search_order()

    def search_order(self):
        try:
            order = config.ORDER_Q.get()
            config.ORDER_Q.task_done()

            table_id = next((i for i, table in enumerate(config.TABLES) if table['id'] == order['table_id']), None)
            print(f'{threading.current_thread().name} picked up the order with Id: {order["id"]} | priority: {order["priority"]} | items: {order["items"]}')
            config.TABLES[table_id]['state'] = config.TABLE_STATE_2
            payload = dict({
                'order_id': order['id'],
                'table_id': order['table_id'],
                'waiter_id': self.id,
                'items': order['items'],
                'priority': order['priority'],
                'max_wait': order['max_wait'],
                'time_start': time.time()
            })
            time.sleep(random.randint(2, 4) * config.TIME_UNIT)
            requests.post('http://localhost:8080/order', json=payload, timeout=0.0000000001)

        except (queue.Empty, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            pass

    def serve_order(self, order_to_serve):
        req_order = next((order for i, order in enumerate(config.ORDERS) if order['id'] == order_to_serve['order_id']), None)
        if req_order is not None and req_order['items'].sort() == order_to_serve['items'].sort():
            # update table state
            table_id = next((i for i, table in enumerate(config.TABLES) if table['id'] == order_to_serve['table_id']), None)
            config.TABLES[table_id]['state'] = config.TABLE_STATE_3

            # calculate total order time
            order_serving_time = int(time.time() - order_to_serve['time_start'])

            # calculate nr of start
            order_stars = {'order_id': order_to_serve['order_id']}
            if order_to_serve['max_wait'] > order_serving_time:
                order_stars['star'] = 5
            elif order_to_serve['max_wait'] * 1.1 > order_serving_time:
                order_stars['star'] = 4
            elif order_to_serve['max_wait'] * 1.2 > order_serving_time:
                order_stars['star'] = 3
            elif order_to_serve['max_wait'] * 1.3 > order_serving_time:
                order_stars['star'] = 2
            elif order_to_serve['max_wait'] * 1.4 > order_serving_time:
                order_stars['star'] = 1
            else:
                order_stars['star'] = 0

            config.ORDER_RATING.append(order_stars)
            sum_stars = sum(feedback['star'] for feedback in config.ORDER_RATING)
            avg = float(sum_stars / len(config.ORDER_RATING))

            served_order = {**order_to_serve, 'serving_time': order_serving_time, 'status': 'DONE', 'feedback': order_stars}
            config.SERVED_ORDERS.append(served_order)
            print( f'Serving the order Endpoint: /distribution :\n'
                      f'Order Id: {served_order["order_id"]}\n'
                      f'Waiter Id: {served_order["waiter_id"]}\n'
                      f'Table Id: {served_order["table_id"]}\n'
                      f'Items: {served_order["items"]}\n'
                      f'Priority: {served_order["priority"]}\n'
                      f'Max Wait: {served_order["max_wait"]}\n'
                      f'Waiting time: {served_order["Serving_time"]}\n'
                      f'Stars: {served_order["Stars_feedback"]}\n'
                      f'Restaurant rating: {avg}')
        else:
            raise Exception(f'The order is not the same as was requested. Original: {req_order}, given: {order_to_serve}')


class Costumers(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Costumers, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            time.sleep(1)
            self.generate_order()

    @staticmethod
    def generate_order():
        (table_id, table) = next(
            ((idx, table) for idx, table in enumerate(config.TABLES) if table['state'] == config.TABLE_STATE_0), (None, None))
        if table_id is not None:
            max_wait_time = 0
            menu_choice = []
            for i in range(random.randint(1, 5)):
                choice = random.choice(config.MENU)
                if max_wait_time < choice['preparation-time']:
                    max_wait_time = choice['preparation-time']
                menu_choice.append(choice['id'])
            max_wait_time = max_wait_time * 1.3
            neworder_id = int(random.randint(1, 10000) * random.randint(1, 10000))
            neworder = {
                'table_id': table['id'],
                'id': neworder_id,
                'items': menu_choice,
                'priority': random.randint(1, 5),
                'max_wait': max_wait_time,

            }
            config.ORDER_Q.put(neworder)
            config.ORDERS.append(neworder)

            config.TABLES[table_id]['state'] = config.TABLE_STATE_1
            config.TABLES[table_id]['order_id'] = neworder_id

        else:
            time.sleep(random.randint(2, 10) * config.TIME_UNIT)
            (table_id, table) = next(
                ((idx, table) for idx, table in enumerate(config.TABLES) if table['state'] == config.TABLE_STATE_3), (None, None)
            )
            if table_id is not None:
                config.TABLES[table_id]['state'] = config.TABLE_STATE_0


def run_dinning_server():
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False),daemon=True)
    threads.append(flask_thread)

    costumer_thread = Costumers()
    threads.append(costumer_thread)

    for _, w in enumerate(config.WAITERS):
        waiter_thread = Waiter(w)
        threads.append(waiter_thread)

    for th in threads:
        th.start()

    for th in threads:
        th.join()

if __name__ == '__main__':
    run_dinning_server()