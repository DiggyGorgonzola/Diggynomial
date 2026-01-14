import math, random, time

class Diggynomial():
    def __init__(self, coefficients=None, zero_coefficient=None):
        self.coefficients = coefficients or [1]
        self.zero_coefficient = zero_coefficient or 0
    def __repr__(self):
        return " + ".join([f"{self.coefficients[i] if ((self.coefficients[i]!=0 and i-self.zero_coefficient==0) or (self.coefficients[i]!=1 and i-self.zero_coefficient!=0)) else ""}{"x" if i-self.zero_coefficient != 0 else ''}{f"{f'**{i-self.zero_coefficient}' if i-self.zero_coefficient not in [0,1] else ''}"}" for i in range(len(self.coefficients))])
    def __call__(self, x):
        if type(x) in [float, int, bool]:
            x = float(x)
            return sum([self.coefficients[i]*(x**(i-self.zero_coefficient)) for i in range(len(self.coefficients))])
        elif isinstance(x, Diggynomial):
            for i in range(len(self.coefficients)):
                for j in range(len(x.coefficients)):
                    pass
        else:
            return TypeError(f"\x1B[3m\033[91m\033[1mTypeError\033[0m\033[31m\x1B[3m: Argument x ({x}) is not a float, int, boolean, or Diggynomial\033[0m")
    def __add__(self, poly):
        selfy,poly = Diggynomial(self.coefficients, self.zero_coefficient).format_with(Diggynomial(poly.coefficients, poly.zero_coefficient))
        for i in selfy.coefficients:
            selfy.coefficients += poly.coefficients
        return selfy
    def extend(self, times=1, dir=1):
        guh = lambda x: len(self.coefficients) if x == 1 else 0 if x == -1 else None
        for _ in range(times):
            self.coefficients.insert(guh(dir),0)
            if dir==-1:
                self.zero_coefficient += 1
    def compress(self):
        while self.coefficients[0] == 0:
            self.coefficients.pop(0)
            self.zero_coefficient -= 1
        while self.coefficients[-1] == 0:
            self.coefficients.pop(-1)
    def format_with(self, poly):
        self.compress()
        poly.compress()
        while min(self.zero_coefficient, poly.zero_coefficient) < max(self.zero_coefficient, poly.zero_coefficient):
            a = {self.zero_coefficient:self, poly.zero_coefficient:poly}[min(self.zero_coefficient, poly.zero_coefficient)]
            a.extend(dir=-1)
        while min(len(self.coefficients),len(poly.coefficients)) < max(len(self.coefficients),len(poly.coefficients)):
            a = {len(self.coefficients):self, len(poly.coefficients):poly}[min(len(self.coefficients),len(poly.coefficients))]
            a.extend(dir=1)
        return self,poly
a = Diggynomial([1, 1, 2, 3])
b = Diggynomial([1, 1, 2, 3], 3)
print((a+b).coefficients)
print(a.coefficients, a.zero_coefficient)
print(b.coefficients, b.zero_coefficient)