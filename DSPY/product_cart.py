import dspy

class ProuductCartSummary(dspy.Predict):
    def __init__(self):
        super().__init__(signature="product_name, cart_items -> summary")

    def forward(self, product_name: str, cart_items: str) -> str:
        return f"You have a {product_name} in cart with {cart_items}"

predictor =  ProuductCartSummary()
response = predictor(product_name = "Wireless Mouse", cart_items = "Laptop, Headphones, Lpatop Bag")
print(response)
