import dspy

class HelloWorld(dspy.Predict):
    def __init__(self):
        super().__init__(signature="name -> message")

    def forward(self, name: str) -> str:
        return f"Hello {name}, Welcome to the magic of DSPY"
    
predictor = HelloWorld()
predictor(name="Raj")