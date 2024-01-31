from fastapi import FastAPI
from fastapi import Request

import db_helper
import generic_helper

app = FastAPI()

inprogress_orders = {}

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    output_contexts = payload["queryResult"]["outputContexts"]

    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        "new.order": new_order,
        "order.add - context: ongoing-order": add_to_order,
        "order.remove - context: ongoing-order": remove_from_order,
        "order.complete - context: ongoing-order": complete_order,
        "track.order - context: ongoing-tracking": track_order
    }

    return intent_handler_dict[intent](parameters, session_id)


def new_order(parameters:dict, session_id:str):
    del inprogress_orders[session_id]

def track_order(parameters:dict, session_id:str):
    order_id = int(parameters["order_id"])

    order_status = db_helper.get_order_status(order_id)

    fulfillment = f"The order with order id #{order_id} is {order_status}."

    return generic_helper.json_response(fulfillment)

def add_to_order(parameters:dict, session_id:str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment = "Please specify each food and their quantities."
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = ', '.join(f"{int(quantity)} {food}" for food, quantity in inprogress_orders[session_id].items())
        fulfillment = f"So far your order is: {order_str}. Do you want anything to remove or add?"

    return generic_helper.json_response(fulfillment)

def complete_order(parameters:dict, session_id:str):
    if session_id not in inprogress_orders:
        fulfillment = "It seems like you haven't placed an order yet. If you want to order, please say something like 'I want to order'"
    else:
        order = inprogress_orders[session_id]
        next_order_id = db_helper.get_next_order_id()

        save_to_db(order, next_order_id)
        order_str = ", ".join({f"{int(quantity)} {item}"for (item, quantity) in inprogress_orders[session_id].items()})
        del inprogress_orders[session_id]


        fulfillment = f"Your order details: {order_str}. Enjoy your meal. Here is your order id: #{next_order_id}"
        return generic_helper.json_response(fulfillment)

def save_to_db(order:dict, next_order_id:int):
    db_helper.insert_order_tracking(next_order_id, "in progress")

    for food_item, quantity in order.items():
        db_helper.insert_orders(food_item, quantity, next_order_id)

# inprogress_orders = {
#     "session_id_1": {"pizza": 2, "sushi": 1},
#     "session_id_2": {"pasta": 3}
# }

def remove_from_order(parameters:dict, session_id:str):
    if session_id not in inprogress_orders:
        fulfillment = "There is no such an order with that id. Please make sure you wrote the id correct."

    else:
        removed_food_items = []
        no_such_items = []
        food_items = parameters["food-item"]

        for food_item in food_items:
            if food_item in inprogress_orders.get(session_id, {}):
                removed_food_items.append(food_item)
                del inprogress_orders[session_id][food_item]
            else:
                no_such_items.append(food_item)

        removed_food_items_str = ", ".join(removed_food_items)
        fulfillment_str = f"{removed_food_items_str} is removed from the bucket"
        current_order_items_str = ", ".join([f"{int(quantity)} {food}" for food, quantity in inprogress_orders[session_id].items()])

        if len(no_such_items) > 0:
            no_items_join = ", ".join(no_such_items)
            fulfillment_str = f"There are no such items in your order: {no_items_join}. So we couldn't delete them"
        fulfillment = f"{fulfillment_str} .Your order currently seems like this:  {current_order_items_str} . Do you want to add or remove anything else?"

    return generic_helper.json_response(fulfillment)