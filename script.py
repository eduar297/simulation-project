import random as rd
from math import *


class VarGenerator():  # Generacion de variables aleatorias
    def U(a, b):  # X~U(a,b)
        U = rd.random()  # U(0,1)
        while not U:  # pues el metodo rd.random() retorna U \in [0,1)
            U = rd.random()

        X = a+(b-a)*U
        return X

    def Ber(p):  # X~Ber(p)
        U = VarGenerator.U(0, 1)
        X = 0
        if U <= p:
            X = 1
        return X

    def Exp(l):  # X~Exp(lambda)
        U = VarGenerator.U(0, 1)
        X = -(1/l)*log(U)
        return X

    def Z():  # Z~N(0,1)
        while True:
            Y = VarGenerator.Exp(1)
            U = VarGenerator.U(0, 1)
            if U <= e**(-((Y-1)**2)/2):
                X = Y
                # Ahora return X o -X con 1/2 de probabilidad cada uno,
                #  esto lo hacemos con una v.a. de Bernoulli de p=1/2.
                Ber = VarGenerator.Ber(1/2)
                if Ber:
                    return X
                else:
                    return -X

    def N(m, s):  # X~N(mu,sigma^2)
        Z = VarGenerator.Z()
        X = Z*s+m
        return X

    def Poisson(l):  # X~Poisson(lambda)
        p = 1
        n = 0
        while 1:
            U = VarGenerator.U(0, 1)
            p *= U
            n += 1
            if p < e**(-l):
                break
        N = n - 1
        return N

    def sort(X, P):  # esto es ineficiente pues es O(n^2) :) :) pero hacer uno O(logn) es pesao, de igual forma solo es ordenar 4 valores :D
        n = len(X)
        for i in range(n-1):
            for j in range(i+1, n):
                if P[i] < P[j]:  # swap
                    P[i], P[j] = P[j], P[i]
                    X[i], X[j] = X[j], X[i]

    def simulate_random_var(X, P):
        VarGenerator.sort(X, P)
        U = VarGenerator.U(0, 1)
        Fx = 0  # funcion de distribucion acomulada de X
        n = len(X)
        for i in range(n):
            Fx += P[i]
            if U < Fx:
                return X[i]


class HappyComputing():
    # 8*60=480 es la jornada estandar de trabajo
    def __init__(self):
        self.t = 0  # linea de tiempo
        self.ta = VarGenerator.Poisson(20)  # tiempo de arribo de clientes
        self.T = 0  # jornada laboral
        self.tDv1 = inf  # tiempo de salida de vendedor 1
        self.tDv2 = inf  # tiempo de salida de vendedor 2
        self.tDe = inf  # tiempo de salida de especialista
        self.tDt1 = inf  # tiempo de salida de tecnico 1
        self.tDt2 = inf  # tiempo de salida de tecnico 2
        self.tDt3 = inf  # tiempo de salida de tecnico 3
        self.Dg = {}  # dicionario arribo:ganancia
        self.Na = 0  # cantidad de arribos
        self.A = {}  # diccionario arribo:tiempo
        self.nv = 0  # numero de clientes en vendedores
        self.NDv1 = 0  # cantidad de salidas de vendedor 1
        self.NDv2 = 0  # cantidad de salidas de vendedor 2
        self.Dv1 = {}  # dicionario cliente:salida de vendedor 1
        self.Dv2 = {}  # dicionario cliente:salida de vendedor 2
        self.ne = 0  # numero de clientes en especialista
        self.NDe = 0  # cantidad de salidas de especialista
        self.De = {}  # dicionario cliente:salida de especialista
        self.nt = 0  # numero de clientes en tecnicos
        self.NDt1 = 0  # cantidad de salidas de tecnico 1
        self.NDt2 = 0  # cantidad de salidas de tecnico 2
        self.NDt3 = 0  # cantidad de salidas de tecnico 3
        self.Dt1 = {}  # dicionario cliente:salida de tecnico 1
        self.Dt2 = {}  # dicionario cliente:salida de tecnico 2
        self.Dt3 = {}  # dicionario cliente:salida de tecnico 3
        # precios de servicios 1, 2, 3, 4 respectivamente
        self.P = [0, 350, 500, 750]
        # [n, Ct1, Ct2, Ct3 Qt] | n: numero de clientes en tecnicos, Cti: cliente en tecnico i, Qt: cola de clientes en tecnicos
        self.ST = [0, 0, 0, 0, []]
        # [n, Cv1, Cv2, Qv] | n: numero de clientes en vendedores, Cvi: cliente en vendedor i, Qv: cola de clientes en vendedores
        self.SV = [0, 0, 0, []]
        # [n, Ce, Qe] | | n: numero de clientes en especialista, Ce: cliente en especialista, Qe: cola de clientes en especialista
        self.SE = [0, 0, []]

    # simular la llegada de clientes al taller de reparaciones electronicas y las actividades realizadas
    def simular(self, T):
        self.__init__()
        self.T = T
        while True:
            # minimo de tiempos
            Min = min(self.ta, self.tDv1, self.tDv2, self.tDt1,
                      self.tDt2, self.tDt3, self.tDe)

            # eventos de arribo
            if Min == self.ta and self.ta <= self.T:
                self.evento_de_arribo()

            # eventos de salida
            elif Min == self.tDv1 and self.tDv1 <= self.T:
                self.evento_de_salida_vendedor_1()
            elif Min == self.tDv2 and self.tDv2 <= self.T:
                self.evento_de_salida_vendedor_2()
            elif Min == self.tDe and self.tDe <= self.T:
                self.evento_de_salida_especialista()
            elif Min == self.tDt1 and self.tDt1 <= self.T:
                self.evento_de_salida_tecnico_1()
            elif Min == self.tDt2 and self.tDt2 <= self.T:
                self.evento_de_salida_tecnico_2()
            elif Min == self.tDt3 and self.tDt3 <= self.T:
                self.evento_de_salida_tecnico_3()

            # eventos de cierre
            elif Min == self.tDv1 and Min > self.T and self.nv > 0:
                self.evento_de_cierre_vendedor_1()
            elif Min == self.tDv2 and Min > self.T and self.nv > 0:
                self.evento_de_cierre_vendedor_2()
            elif Min == self.tDe and Min > self.T and self.ne > 0:
                self.evento_de_cierre_especialista()
            elif Min == self.tDt1 and Min > self.T and self.nt > 0:
                self.evento_de_cierre_tecnico_1()
            elif Min == self.tDt2 and Min > self.T and self.nt > 0:
                self.evento_de_cierre_tecnico_2()
            elif Min == self.tDt3 and Min > self.T and self.nt > 0:
                self.evento_de_cierre_tecnico_3()

            else:
                break

    def evento_de_arribo(self):
        self.t = self.ta
        self.Na += 1
        self.ta = self.t + VarGenerator.Poisson(20)
        if self.ta > self.T:
            self.ta = inf
        self.A[self.Na] = self.t
        s = VarGenerator.simulate_random_var(
            [1, 2, 3, 4], [0.45, 0.25, 0.1, 0.2])
        self.Dg[self.Na] = self.P[s - 1]
        if s == 3:  # arribo a servicio cambio de equipo
            self.ne += 1
            if self.SE[1] == 0:
                self.SE = [self.ne, self.Na, self.SE[2]]
                self.tDe = self.t + VarGenerator.Exp(1/15)
            else:
                self.SE = [self.ne, self.SE[1], self.SE[2] + [self.Na]]
        elif s == 4:  # arribo a servicio venta(para comprar en este caso :D)
            self.nv += 1
            if self.SV[1] == 0:
                self.SV = [self.nv, self.Na, self.SV[2], self.SV[3]]
                self.tDv1 = self.t + VarGenerator.N(5, 2)
            elif self.SV[2] == 0:
                self.SV = [self.nv, self.SV[1], self.Na, self.SV[3]]
                self.tDv2 = self.t + VarGenerator.N(5, 2)
            else:
                self.SV = [self.nv, self.SV[1],
                           self.SV[2], self.SV[3] + [self.Na]]
        # arribo a servicio de reparacion ya sea por garantia (1) o fuera de garantia (2)
        else:
            self.nt += 1
            if self.ST[1] == 0:
                self.ST = [self.nt, self.Na,
                           self.ST[2], self.ST[3], self.ST[4]]
                self.tDt1 = self.t + VarGenerator.Exp(1/20)

            elif self.ST[2] == 0:
                self.ST = [self.nt, self.ST[1],
                           self.Na, self.ST[3], self.ST[4]]
                self.tDt2 = self.t + VarGenerator.Exp(1/20)

            elif self.ST[3] == 0:
                self.ST = [self.nt, self.ST[1],
                           self.ST[2], self.Na, self.ST[4]]
                self.tDt3 = self.t + VarGenerator.Exp(1/20)

            elif self.SE[2] == 0 and len(self.SE[3]) == 0:
                self.ne += 1
                self.nt -= 1
                self.SE = [self.ne, self.Na, []]
                self.tDe = self.t + VarGenerator.Exp(1/20)

            else:
                self.ST = [self.nt, self.ST[1], self.ST[2],
                           self.ST[3], self.ST[4] + [self.Na]]

    def evento_de_salida_vendedor_1(self):
        self.t = self.tDv1
        self.NDv1 += 1
        self.Dv1[self.SV[1]] = self.t
        if self.nv == 1:
            self.nv -= 1
            self.SV = [0, 0, 0, []]
            self.tDv1 = inf
        elif self.nv == 2:
            self.nv -= 1
            self.SV = [1, 0, self.SV[2], []]
            self.tDv1 = inf
        elif self.nv > 2:
            f = self.SV[3][0]
            self.SV[3].remove(f)
            self.nv -= 1
            self.SV = [self.nv, f, self.SV[2], self.SV[3]]
            self.tDv1 = self.t + VarGenerator.N(5, 2)

    def evento_de_salida_vendedor_2(self):
        self.t = self.tDv2
        self.NDv2 += 1
        self.Dv2[self.SV[2]] = t
        if self.nv == 1:
            self.nv -= 1
            self.SV = [0, 0, 0, []]
            self.tDv2 = inf
        elif self.nv == 2:
            self.nv -= 1
            self.SV = [1, self.SV[1], 0, []]
            self.tDv2 = inf
        elif self.nv > 2:
            self.nv -= 1
            f = self.SV[3][0]
            self.SV[3].remove(f)
            self.SV = [self.nv, self.SV[1], self.f, self.SV[3]]
            self.tDv2 = self.t + VarGenerator.N(5, 2)

    def evento_de_salida_especialista(self):
        self.t = self.tDe
        self.NDe += 1
        self.De[self.SE[1]] = self.t
        if len(self.SE[2]) == 0:
            if len(self.ST[4]) == 0:
                self.ne -= 1
                self.tDe = inf
                self.SE = [self.nv, 0, []]
            else:
                self.nt -= 1
                self.tDe = self.t + VarGenerator.Exp(1/20)
                f = self.ST[2][0]
                self.ST[2].remove(f)
                self.SE = [self.ne, f, []]
                self.ST[0] = self.nt
        else:
            self.ne -= 1
            self.tDe = self.t + VarGenerator.Exp(1/15)
            f = self.SE[2][0]
            self.SE[2].remove(f)
            self.SE = [self.ne, f, self.SE[2]]

    def evento_de_salida_tecnico_1(self):
        self.t = self.tDt1
        self.NDt1 += 1
        self.Dt1[self.ST[1]] = self.t
        if self.nt == 1:
            self.nt -= 1
            self.ST = [0, 0, 0, 0, []]
            self.tDt1 = inf
        elif self.nt == 2 or self.nt == 3:
            self.nt -= 1
            self.ST = [1, 0, self.ST[2], self.ST[3], []]
            self.tDt1 = inf
        elif self.nt > 3:
            self.nt -= 1
            f = self.ST[4][0]
            self.ST[4].remove(f)
            self.ST = [self.nt, f, self.ST[2], self.ST[3], self.ST[4]]
            self.tDt1 = self.t + VarGenerator.Exp(1/20)

    def evento_de_salida_tecnico_2(self):
        self.t = self.tDt2
        self.NDt2 += 1
        self.Dt2[self.ST[2]] = self.t
        if self.nt == 1:
            self.nt -= 1
            self.ST = [0, 0, 0, 0, []]
            self.tDt2 = inf
        elif self.nt == 2 or self.nt == 3:
            self.nt -= 1
            self.ST = [1, self.ST[1], 0, self.ST[3], []]
            self.tDt2 = inf
        elif self.nt > 3:
            self.nt -= 1
            f = self.ST[4][0]
            self.ST[4].remove(f)
            self.ST = [self.nt, self.ST[1], f, self.ST[3], self.ST[4]]
            self.tDt2 = self.t + VarGenerator.Exp(1/20)

    def evento_de_salida_tecnico_3(self):
        self.t = self.tDt3
        self.NDt3 += 1
        self.Dt3[self.ST[3]] = self.t
        if self.nt == 1:
            self.nt -= 1
            self.ST = [0, 0, 0, 0, []]
            self.tDt3 = inf
        elif self.nt == 2 or self.nt == 3:
            self.nt -= 1
            self.ST = [1, self.ST[1], self.ST[2], 0, []]
            self.tDt3 = inf
        elif self.nt > 3:
            self.nt -= 1
            f = self.ST[4][0]
            self.ST[4].remove(f)
            self.ST = [self.nt, self.ST[1], self.ST[2], f, self.ST[4]]
            self.tDt3 = self.t + VarGenerator.Exp(1/20)

    def evento_de_cierre_vendedor_1(self):
        self.t = self.tDv1
        self.NDv1 += 1
        self.Dv1[self.SV[1]] = self.t
        if self.nv == 1:
            self.nv -= 1
            self.SV = [0, 0, 0, []]
            self.tDv1 = inf
        elif self.nv == 2:
            self.nv -= 1
            self.SV = [1, 0, self.SV[2], []]
            self.tDv1 = inf
        elif self.nv > 2:
            f = self.SV[3][0]
            self.SV[3].remove(f)
            self.nv -= 1
            self.SV = [self.nv, f, self.SV[2], self.SV[3]]
            self.tDv1 = self.t + VarGenerator.N(5, 2)

    def evento_de_cierre_vendedor_2(self):
        self.t = self.tDv2
        self.NDv2 += 1
        self.Dv2[self.SV[2]] = self.t
        if self.nv == 1:
            self.nv -= 1
            self.SV = [0, 0, 0, []]
            self.tDv2 = inf
        elif self.nv == 2:
            self.nv -= 1
            self.SV = [1, self.SV[1], 0, []]
            self.tDv2 = inf
        elif self.nv > 2:
            self.nv -= 1
            f = self.SV[3][0]
            self.SV[3].remove(f)
            self.SV = [self.nv, self.SV[1], f, self.SV[3]]
            self.tDv2 = self.t + VarGenerator.N(5, 2)

    def evento_de_cierre_especialista(self):
        self.t = self.tDe
        self.NDe += 1
        self.De[self.SE[1]] = self.t
        if len(self.SE[2]) == 0:
            if len(self.ST[4]) == 0:
                self.ne -= 1
                self.tDe = inf
                self.SE = [self.nv, 0, []]
            else:
                self.nt -= 1
                self.tDe = self.t + VarGenerator.Exp(1/20)
                f = self.ST[2][0]
                self.ST[2].remove(f)
                self.SE = [self.ne, f, []]
                self.ST[0] = self.nt

    def evento_de_cierre_tecnico_1(self):
        self.t = self.tDt1
        self.NDt1 += 1
        self.Dt1[self.ST[1]] = self.t
        if self.nt == 1:
            self.nt -= 1
            self.ST = [0, 0, 0, 0, []]
            self.tDt1 = inf
        elif self.nt == 2 or self.nt == 3:
            self.nt -= 1
            self.ST = [1, 0, self.ST[2], self.ST[3], []]
            self.tDt1 = inf
        elif self.nt > 3:
            self.nt -= 1
            f = self.ST[4][0]
            self.ST[4].remove(f)
            self.ST = [self.nt, f, self.ST[2], self.ST[3], self.ST[4]]
            self.tDt1 = self.t + VarGenerator.Exp(1/20)

    def evento_de_cierre_tecnico_2(self):
        self.t = self.tDt2
        self.NDt2 += 1
        self.Dt2[self.ST[2]] = self.t
        if self.nt == 1:
            self.nt -= 1
            self.ST = [0, 0, 0, 0, []]
            self.tDt2 = inf
        elif self.nt == 2 or self.nt == 3:
            self.nt -= 1
            self.ST = [1, self.ST[1], 0, self.ST[3], []]
            self.tDt2 = inf
        elif self.nt > 3:
            self.nt -= 1
            f = self.ST[4][0]
            self.ST[4].remove(f)
            self.ST = [self.nt, self.ST[1], f, self.ST[3], self.ST[4]]
            self.tDt2 = self.t + VarGenerator.Exp(1/20)

    def evento_de_cierre_tecnico_3(self):
        self.t = self.tDt3
        self.NDt3 += 1
        self.Dt3[self.ST[3]] = self.t
        if self.nt == 1:
            self.nt -= 1
            self.ST = [0, 0, 0, 0, []]
            self.tDt3 = inf
        elif self.nt == 2 or self.nt == 3:
            self.nt -= 1
            self.ST = [1, self.ST[1], self.ST[2], 0, []]
            self.tDt3 = inf
        elif self.nt > 3:
            self.nt -= 1
            f = self.ST[4][0]
            self.ST[4].remove(f)
            self.ST = [self.nt, self.ST[1], self.ST[2], f, self.ST[4]]
            self.tDt3 = self.t + VarGenerator.Exp(1/20)


hc = HappyComputing()

hc.simular(T=8*60)
print(f'Total de Clientes que llegan a Happy Computing en una jornada de 8 horas: {len(hc.A.keys())}')
gt = 0
print('Cliente | Servicio              |Hor. de arribo | Hor. de salida                | Ganancia que reporta')
for item in hc.A:
    if item in hc.Dv1.keys():
        print(
            f'{item} \t|\t vendedor 1 \t|\t {hc.A[item]} \t|\t {hc.Dv1[item]} \t|\t {hc.Dg[item]}')
        gt += hc.Dg[item]
    if item in hc.Dv2.keys():
        print(
            f'{item} \t|\t vendedor 2 \t|\t {hc.A[item]} \t|\t {hc.Dv2[item]} \t|\t {hc.Dg[item]}')
        gt += hc.Dg[item]
    if item in hc.Dt1.keys():
        print(
            f'{item} \t|\t tecnico 1 \t|\t {hc.A[item]} \t|\t {hc.Dt1[item]} \t|\t {hc.Dg[item]}')
        gt += hc.Dg[item]
    if item in hc.Dt2.keys():
        print(
            f'{item} \t|\t tecnico 2 \t|\t {hc.A[item]} \t|\t {hc.Dt2[item]} \t|\t {hc.Dg[item]}')
        gt += hc.Dg[item]
    if item in hc.Dt3.keys():
        print(
            f'{item} \t|\t tecnico 3 \t|\t {hc.A[item]} \t|\t {hc.Dt3[item]} \t|\t {hc.Dg[item]}')
        gt += hc.Dg[item]
    if item in hc.De.keys():
        print(
            f'{item} \t|\t especialista \t|\t {hc.A[item]} \t|\t {hc.De[item]} \t|\t {hc.Dg[item]}')
        gt += hc.Dg[item]
print(f'Ganancia total: {gt}')
