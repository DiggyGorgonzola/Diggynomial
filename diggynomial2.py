import math, random, time

L = [2,-2,-8,-16,-26,-38,-52,-68,-86,-106,-128]
#fully functional!

class Diggynomial2():
    def __init__(self,coefficients=None, zc=None):
        self.coeff = coefficients if isinstance(coefficients, list) else [coefficients] if isinstance(coefficients, (int,float)) else [0]
        self.zc = zc if zc is not None else 0
    def copy(self):
        return Diggynomial2(coefficients=[i for i in self.coeff], zc=self.zc)
    def derivate(self):
        c = Diggynomial2(coefficients=[0 for _ in range(len(self.coeff) + 1)], zc=self.zc)
        for i in range(1,len(self.coeff)):
            c.coeff[i-1] = self.coeff[i]*(i-self.zc)
        return c.compress()
    def __add__(self, poly):
        s,p = self.format(poly)
        for i in range(len(s.coeff)):
            s.coeff[i] += p.coeff[i]
        return s
    def __mul__(self, poly):
        s,p = self.copy().format(poly.copy())
        c = Diggynomial2()
        for x in range(len(s.coeff)):
            for y in range(len(p.coeff)):
                s_pow = x - s.zc
                p_pow = y - p.zc
                q = s.coeff[x] * p.coeff[y]
                d = Diggynomial2(coefficients=q, zc=-(s_pow+p_pow))
                c += d
        return c.compress()
    def __pow__(self, val):
        s = self.copy()
        q = s.copy()
        if val > 0:
            for _ in range(val-1):
                q = q * s
            return q
        elif val == 1:
            return self
        elif val == 0:
            return Diggynomial2(1)
    # fix this
    def __call__(self, poly):
        if isinstance(poly, Diggynomial2):
            c = Diggynomial2()
            print(c)
            s,p = self.copy().format(poly.copy())
            for x in range(len(s.coeff)):
                s_pow = x - s.zc
                q = Diggynomial2(coefficients=[s.coeff[x]]) * (p ** s_pow)
                c += q
            return c
        elif isinstance(poly, (float, int)):
            sum = 0
            for i in range(len(self.coeff)):
                sum += self.coeff[i]*(poly ** i-self.zc)
            return sum
    def __repr__(self):
        return f"Diggynomial2(coefficients={self.coeff}, zc={self.zc})"

    def compress(self):
        while self.coeff[-1] == 0 and self.zc < len(self.coeff)-1 and len(self.coeff) > 1:
            self.coeff.pop(-1)
        while self.coeff[0] == 0 and len(self.coeff) > 1:
            self.coeff.pop(0)
            self.zc -= 1
        while self.zc < 0:
            self.coeff.insert(0,0)
            self.zc += 1
        return self
    
    def format(self, poly):
        s,p=self.copy(),poly.copy()
        s.compress()
        p.compress()
        lack = max(s.zc,p.zc) - min(s.zc,p.zc)
        dir = 1 if s.zc < p.zc else -1
        for _ in range(lack):
            if dir == 1:
                s.coeff.insert(0,0)
                s.zc += 1
            else:
                p.coeff.insert(0,0)
                p.zc += 1
        while len(s.coeff) < len(p.coeff):
            s.coeff.append(0)
        while len(p.coeff) < len(s.coeff):
            p.coeff.append(0)
        return (s,p)
    
a = Diggynomial2([1,0,0], 0)
print(a.integrate())
