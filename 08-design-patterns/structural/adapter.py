# Adapter Pattern

class OldPrinter:
    def print_old(self):
        print("Printing old")

class NewPrinter:
    def print(self):
        print("Printing new")

class PrinterAdapter:
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def print(self):
        self.old_printer.print_old()

def use_printer(printer):
    printer.print()

old_printer = OldPrinter()
new_printer = NewPrinter()
adapter = PrinterAdapter(old_printer)


# use new printer
use_printer(new_printer)

# use adapter
use_printer(adapter)