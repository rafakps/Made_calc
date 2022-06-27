# Classe que cria / Calcula as propriedades geométricas
# Classe que já calcula todas as propriedades geométricas da madeira
# Todas as resistências devem ser calculadas em Kn/ cm²

import math
class Madeira:
    def __init__(self, base, altura, comprimento ,especie,kmod):
        self.base = base
        self.altura = altura
        self.comprimento = comprimento
        self.especie = especie
        self.kmod = kmod
# _____________________ MADEIRAS____________________________________________________
    def fu_p12(self,fu_p12):
        return fu_p12 * (1 + (3 * (15 - 12) / 100))


    def fvu_p12(self,fvu_p12):
        return fvu_p12 * (1 + (3 * (25 - 12) / 100))


    def eu_p12(self,eu_p12):
        return eu_p12 * (1 + (2 * (25 - 12) / 100))


    def fc0d1(self,fck):
        return self.kmod * fck / 1.4

    def fc0d2(self,fck):
        return self.kmod * self.eu_p12(fck) / 1.4



    def fvd1(self,fvk):
        return self.kmod *fvk / 1.8
    def fvd2(self,fvk):
        return self.kmod * self.fvu_p12(fvk) / 1.8



    def ec0d1(self,ec0m):
        return self.kmod * ec0m

    def fc0d(self):
        if self.especie == 'C20':
            fcd01 = self.fc0d1(2)
        elif self.especie == 'C30':
            fcd01 = self.fc0d1(3)
        elif self.especie == 'C40':
            fcd01 = self.fc0d1(4)
        elif self.especie == 'C60':
            fcd01 = self.fc0d1(6)
        elif self.especie == 'pinus':
            fcd01 = self.fc0d2(self.fu_p12(4.4))
        else:
            fcd01 = self.fc0d1(2)
        return fcd01

    def fvd(self):
        if self.especie == 'C20':
            fcd01 = self.fvd1(.4)
        elif self.especie == 'C30':
            fcd01 = self.fvd1(.5)
        elif self.especie == 'C40':
            fcd01 = self.fvd1(.6)
        elif self.especie == 'C60':
            fcd01 = self.fvd1(.8)
        elif self.especie == 'pinus':
            fcd01 = self.fvd2(self.fvu_p12(.77))
        else:
            fcd01 = self.fvd1(.4)
        return fcd01

    def ec0d(self):
        if self.especie == 'C20':
            fcd01 = self.ec0d1(950)
        elif self.especie == 'C30':
            fcd01 = self.ec0d1(1450)
        elif self.especie == 'C40':
            fcd01 = self.ec0d1(1950)
        elif self.especie == 'C60':
            fcd01 = self.ec0d1(2450)
        elif self.especie == 'pinus':
            fcd01 = self.ec0d1(self.eu_p12(1330))
        else:
            fcd01 = self.ec0d1(950)
        return fcd01

    def peso_metro_1(self,densidade):
        # Retorna o peso da peça em Kn / m
        return self.base * self.altura * densidade

    def peso_metro(self):
        # Retorna o peso da peça em Kn / m
        if self.especie == 'C20':
            fcd01 = self.base * self.altura * 6.5/100**2
        elif self.especie == 'C30':
            fcd01 = self.base * self.altura * 8/100**2
        elif self.especie == 'C40':
            fcd01 = self.base * self.altura * 9.5/100**2
        elif self.especie == 'C60':
            fcd01 = self.base * self.altura * 10/100**2
        elif self.especie == 'pinus':
            fcd01 = self.base * self.altura * 7/100**2
        else:
            fcd01 = self.base * self.altura * 6.5/100**2
        return fcd01

# _______________ GEOMETRIA_______________________
    def area(self):
            return self.base * self.altura

    def inercia_x(self):
            return self.base * (self.altura **3)/12

    def inercia_y(self):
            return self.altura * (self.base ** 3) / 12

    def esbeltez_x(self):
        return self.comprimento / (self.inercia_x()/self.area())**.5

    def esbeltez_y(self):
        return self.comprimento / (self.inercia_y()/self.area())**.5


    def wx(self):
        return self.inercia_x() / (self.altura/2)

    def wy(self):
        return self.inercia_y() / (self.base/2)

    def tensão(self,força):
        # Colocar esforço de tração ou compressão
        return força/self.area()

    def tensão_mx(self,mx):
        # Colocar momento fletor eixo X
        return mx/self.wx()

    def tensão_my(self, my):
        # Colocar momento fletor eixo Y
        return my / self.wy()

    def tração_verificação(self,força):
        # Colocar força atuante na seção transversal
        return self.tensão(força)/self.fc0d()

    def compressão_verificação(self,força,mx,my):
        # Preencher com a força de compressão, momento fletor no eixo X e momento fletor eixo Y
        ea0 = self.comprimento/300
        try:
            eix1 = max(mx / força,self.altura / 30)
            eiy1 = max(my / força, self.base / 30)
        except:
            eix1 = max(mx / 1, self.altura / 30)
            eiy1 = max(my / 1, self.base / 30)

        ei_x = eix1 + ea0
        ei_y = eiy1 + ea0
        fex = math.pi**2 * self.ec0d() * self.inercia_x() / self.comprimento**2
        fey = math.pi**2 * self.ec0d() * self.inercia_y() / self.comprimento**2
        mex = abs(força * ei_x * (fex/(fex-força)))
        mey = abs(força * ei_y * (fey/(fey-força)))

        if self.base == self.altura:
            km = 1
        else:
            km = 0.5

        if self.esbeltez_x() >= 140:
            return "esbeltez maior do que 140, redimensionar",round(self.esbeltez_x(),2)
        elif self.esbeltez_y() >= 140:
            return "esbeltez maior do que 140, redimensionar",round(self.esbeltez_y(),2)
        else:
            ten_normal = (self.tensão(força)/self.fc0d())**2 + (max(self.tensão_mx(mx),self.tensão_my(my)) + km * min(self.tensão_mx(mx),self.tensão_my(my))) / self.fc0d()
            ten_mx = (self.tensão(força) + mex/self.wx())/self.fc0d()
            ten_my = (self.tensão(força)+ mey/self.wy())/self.fc0d()
            return round(max(ten_mx,ten_my,ten_normal),4)
            #return  ten_normal
            #return ten_my
            #return ten_mx

    def viga_verificação(self,momento,cortante):
        momento_verificação = (momento/self.wx())/self.fc0d()
        cortante_verificação = (cortante * 1.5 / self.area())/self.fvd()
        return round(max(momento_verificação,cortante_verificação),4)

    def viga_deformação(self,carregamento):
        deformação = (5/384) * (carregamento/100) * self.comprimento**4 / (self.ec0d()*self.inercia_x())
        deformação_máxima = self.comprimento/200
        return round(deformação/deformação_máxima,4)

    def viga_estabilidade(self):
        beta_M = [6,6,8.8,12.3,15.9,19.5,23.1,26.7,30.3,34,37.6]

        beta_atual = round(self.altura / self.base,2)

        comprimento_max = self.base * self.ec0d() /(beta_M[int(beta_atual)]*self.fc0d())

        return comprimento_max / self.comprimento








#pine = Madeira(5,20,300,'C20',0.56)

#print(pine.fc0d())
#print(pine.viga_verificação(98,0.7))
#print(pine.viga_deformação(4))
#print(pine.viga_estabilidade())

