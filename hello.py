class Car:
    NUMBER_OF_WHEELS = 4

    def __init__(self, model, make, price):
        self.model = model
        self.make = make
        self.price = price

    def car_info(self):
        print(self.NUMBER_OF_WHEELS)


audi = Car("Audi", "e-tron 6", 115000)
audi.car_info()
