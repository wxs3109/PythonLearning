# Builder Pattern


class Car:
    def __init__(self, engine, transmission, color):
        self.engine = engine
        self.transmission = transmission
        self.color = color

    def print_car(self):
        print(f"Car with {self.engine} engine, {self.transmission} transmission, and {self.color} color")

class CarBuilder:
    def __init__(self):
        self.car = Car(None, None, None)

    def set_engine(self, engine):
        self.car.engine = engine
        return self

    def set_transmission(self, transmission):
        self.car.transmission = transmission
        return self

    def set_color(self, color):
        self.car.color = color
        return self

    def get_car(self):
        return self.car

car_builder = CarBuilder()
car_builder.set_engine("V8").set_transmission("Automatic").set_color("Red").get_car().print_car()