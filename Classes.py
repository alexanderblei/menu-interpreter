class Maths():
    def __init__(self,total):
        self.numbers = total

    def addition(self):
        return self.numbers + 5

    def division(self,input):
        return self.numbers/input

do_test = Maths(10)
print do_test.division(5)


print do_test