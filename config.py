import queue

global TIME_UNIT
TIME_UNIT = 1

global ORDER_Q
ORDER_Q = queue.Queue()
ORDER_Q.join()

global ORDERS
ORDERS = []

global ORDER_RATING
ORDER_RATING = []

global SERVED_ORDERS
SERVED_ORDERS = []

global MENU 
MENU = [{
    "id": 1,
    "name": "pizza",
    "preparation-time":     20 ,
    "complexity":     2 ,
    "cooking-apparatus":    "oven"
}, {
    "id": 2,
    "name": "salad",
    "preparation-time":     10 ,
    "complexity":     1 ,
    "cooking-apparatus":    None
}, {
    "id": 3,
    "name": "zeama",
    "preparation-time":     7 ,
    "complexity":     1 ,
    "cooking-apparatus":    "stove"
}, {
    "id": 4,
    "name": "Scallop Sashimi with Meyer Lemon Confit",
    "preparation-time":     32 ,
    "complexity":     3 ,
    "cooking-apparatus":    None
}, {
    "id": 5,
    "name": "Island Duck with Mulberry Mustard",
    "preparation-time": 35,
    "complexity": 3,
    "cooking-apparatus": "oven"
}, {
    "id": 6,
    "name": "Waffles",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": "stove"
}, {
    "id": 7,
    "name": "Aubergine",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": None
}, {
    "id": 8,
    "name": "Lasagna",
    "preparation-time": 30,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 9,
    "name": "Burger",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": "oven"
}, {
    "id": 10,
    "name": "Gyros",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": None
}]

global TABLE_STAT_0
global TABLE_STATE_1
global TABLE_STATE_2
global TABLE_STATE_3
TABLE_STATE_0 = 'being free'
TABLE_STATE_1 = 'waiting to make a order'
TABLE_STATE_2 = 'waiting for the order to be served'
TABLE_STATE_3 = 'waiting to be free'

global TABLES
TABLES = [{
    "id": 1,
    "state": TABLE_STATE_0,
    "order_id": None
}, {
    "id": 2,
    "state": TABLE_STATE_0,
    "order_id": None
}, {
    "id": 3,
    "state": TABLE_STATE_0,
    "order_id": None
}, {
    "id": 4,
    "state": TABLE_STATE_0,
    "order_id": None
}, {
    "id": 5,
    "state": TABLE_STATE_0,
    "order_id": None
}
]

global WAITERS
WAITERS = [{
    'id' : 1,
    'name' : 'Jamie'
    },
    {
    'id' : 2,
    'name' : 'Oliver'
    },
    {
    'id' : 3,
    'name' : 'Gordon'
    },
    {
    'id' : 4,
    'name' : 'Jasmin'
    },
]