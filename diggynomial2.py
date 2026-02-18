import math, random, time

L = [2,-2,-8,-16,-26,-38,-52,-68,-86,-106,-128]

class Diggynomial2():
    def __init__(self,coefficients=None, zc=None):
        self.coeff = coefficients if isinstance(coefficients, list) else [coefficients] if isinstance(coefficients, (int,float)) else [0]
        self.zc = zc if zc is not None else 0
    def copy(self):
        return Diggynomial2(coefficients=[i for i in self.coeff], zc=self.zc)
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
        for i in range(val):
            s = s * s
        return s
    def __call__(self, poly):
        if isinstance(poly, Diggynomial2):
            c = Diggynomial2()
            s,p = self.copy().format(poly.copy())
            for x in range(len(s.coeff)):
                s_pow = x - s.zc
                q = Diggynomial2(coefficients=[s.coeff[x]]) * (p ** s_pow)
                c += q
            return c
    def __repr__(self):
        return f"Diggynomial2(coefficients={self.coeff}, zc={self.zc})"
    
    # not safe
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

a = Diggynomial2([4], 0)
b = Diggynomial2([0,2], 0)
print(a(a))
