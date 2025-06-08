# Factory Method


class Car:

    def print_name(self):
        print("Car")

class BMW(Car):
    def print_name(self):
        print("BMW")

class Audi(Car):
    def print_name(self):
        print("Audi")

class CarFactory:
    def get_car(self, car_type):
        if car_type == "BMW":
            return BMW()
        elif car_type == "Audi":
            return Audi()
        else:
            return Car()

car_factory = CarFactory()
car_factory.get_car("BMW").print_name()