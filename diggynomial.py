import math, random, time

class Diggynomial():
    def __init__(self, coefficients=None, zero_coefficient=None):
        self.coefficients = coefficients if coefficients is not None else [0]
        self.zero_coefficient = zero_coefficient if zero_coefficient is not None else 0
    def copy(self):
        return Diggynomial(coefficients=[i for i in self.coefficients], zero_coefficient=self.zero_coefficient)
    def __repr__(self):
        return " + ".join([f"{self.coefficients[i] if ((self.coefficients[i]!=0 and i-self.zero_coefficient==0) or (self.coefficients[i]!=1 and i-self.zero_coefficient!=0)) else ""}{"x" if i-self.zero_coefficient != 0 else ''}{f"{f'**{i-self.zero_coefficient}' if i-self.zero_coefficient not in [0,1] else ''}"}" for i in range(len(self.coefficients))])
    def __call__(self, x):
        if type(x) in [float, int, bool]:
            x = float(x)
            return sum([self.coefficients[i]*(x**(i-self.zero_coefficient)) for i in range(len(self.coefficients))])
        elif isinstance(x, Diggynomial):
            c = Diggynomial(coefficients=[0], zero_coefficient=0)
            b = self.copy()
            a = x.copy()
            for i, coeff in enumerate(b.coefficients):
                power = i - b.zero_coefficient
                if coeff == 0:
                    continue

                if power == 0:
                    c += coeff
                else:
                    c += coeff * (a ** power)

            c.compress()
            return c
        else:
            return TypeError(f"\033[91m\033[1mTypeError\033[0m\033[31m: Argument x ({x}) is not a float, int, boolean, or Diggynomial\033[0m")
    def __add__(self, poly):
        if isinstance(poly, Diggynomial):
            selfy,poly = self.copy().format_with(poly.copy())
            for i in range(len(selfy.coefficients)):
                selfy.coefficients[i] += poly.coefficients[i]
            return selfy
        elif isinstance(poly, int) or isinstance(poly, float):
            selfy = self.copy()
            selfy.coefficients[selfy.zero_coefficient] += poly
            return selfy
    def __mul__(self, poly):
        if isinstance(poly, Diggynomial):
            selfy,poly = self.copy().format_with(poly.copy())
            new_thingy,_ = Diggynomial([1 for _ in range(10)], 0).format_with(selfy)
            for i in range(len(selfy.coefficients)):
                for j in range(len(poly.coefficients)):
                    new_thingy.extend(i+j)
                    x=selfy.coefficients[i]
                    y=poly.coefficients[j]
                    new_thingy.coefficients[i+j] += x*y
                    new_thingy.compress()
            for i in range(len(new_thingy.coefficients)):
                new_thingy.coefficients[i] -= 1
            new_thingy.compress()
            return new_thingy
        elif isinstance(poly, int):
            selfy = self.copy()
            for i in range(len(selfy.coefficients)):
                selfy.coefficients[i] *= poly
            return selfy.compress()
    def __rmul__(self, poly):
        return self.copy().__mul__(poly)
    def __pow__(self, amt):
        g = self.copy()
        for _ in range(amt - 1):
            g = g.copy()*g.copy()
        return g.copy()
    def extend(self, times=1, dir=1):
        guh = lambda x: len(self.coefficients) if x == 1 else 0 if x == -1 else None
        for _ in range(times):
            self.coefficients.insert(guh(dir),0)
            if dir==-1:
                self.zero_coefficient += 1
    def compress(self):
        while len(self.coefficients) > 0 and self.coefficients[0] == 0:
            self.coefficients.pop(0)
            self.zero_coefficient += 1
        while len(self.coefficients) > 0 and self.coefficients[-1] == 0:
            self.coefficients.pop(-1)
        return self
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

"""

"""

'''Testing Zone'''

if __name__ == "__main__":
    a = Diggynomial(coefficients=[1,3])
    b = Diggynomial(coefficients=[0,1/2])
    print(a(b))

