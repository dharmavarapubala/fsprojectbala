# You can use this for schema abstraction if needed later
def format_donation(donation):
    return {
        "id": str(donation["_id"]),
        "name": donation["name"],
        "food_item": donation["food_item"],
        "quantity": donation["quantity"],
        "contact": donation["contact"]
    }
