import numpy as np
import math


class Pontos():
    count = 0
    quant = 0
    apoios = []
    cargas = []
    cargas_ps = []
    def __init__(self, x,y,rx,ry,fx,fy):
        self.x = x
        self.y = y
        self.vx = Pontos.count
        self.vy = Pontos.count+1
        self.rx = rx
        self.ry = ry
        self.fx = fx
        self.fy = fy

        if self.rx == 1:
            Pontos.apoios.append(self.vx)
        else:
            Pontos.cargas.append(self.fx)
            Pontos.cargas_ps.append(self.vx)

        if self.ry == 1:
            Pontos.apoios.append(self.vy)
        else:
            Pontos.cargas.append(self.fy)
            Pontos.cargas_ps.append(self.vy)


        Pontos.count +=2
        Pontos.quant +=1


class Elementos():
    count1 = 0
    posicao = []
    direcao = []
    rigidez_elementos = []
    posicao_global = []


    def __init__(self, pi, pf, elasti, area):
        Elementos.count1 += 1

        self.pi = pi
        self.pf = pf
        self.elasti = elasti
        self.area = area
        self.comprimento = math.sqrt((pf.x - pi.x) ** 2 + ((pf.y - pi.y) ** 2))
        self.x = pf.x - pi.x
        self.y = pf.y - pi.y
        x = self.x / self.comprimento
        y = self.y / self.comprimento
        self.rigidez1 = [[x * x, x * y, -x * x, -x * y],
                         [x * y, y * y, -x * y, -y * y],
                         [-x * x, -x * y, x * x, x * y],
                         [-x * y, -y * y, x * y, y * y]]
        self.rigidez =np.array(self.rigidez1) * (self.elasti * self.area) / self.comprimento
        x1 = self.x
        y1 = self.y
        self.vetores = np.array([-x1,-y1,x1,y1])*self.area*self.elasti/(self.comprimento**2)
        self.posicao = np.array([self.pi.vx,self.pi.vy,self.pf.vx,self.pf.vy])
        Elementos.posicao_global.append(self.posicao)
        Elementos.rigidez_elementos.append(self.rigidez)



class Matriz_global():
    def __init__(self, pontos, barras,rigidez, posicao):
        self.pontos = pontos
        self.barras = barras
        self.rigidez = rigidez
        self.posicao = posicao

    def calculo_matriz(self):
        matriz_global = np.zeros((self.pontos, self.pontos))
        matriz_global_1 = np.zeros((self.pontos, self.pontos))
        for contador in range(self.barras):
            posicao_1 = self.posicao[contador]
            rigidez_1 = self.rigidez[contador]
            for linha in range(self.pontos):  # linha matrix grande
                for coluna in range(self.pontos):  # coluna matriz grande
                    for i, a in enumerate(posicao_1):  # linha matrix pequena
                        for j, b in enumerate(posicao_1):  # coluna matrix pequena
                            if [linha, coluna] == [a, b]:
                                matriz_global[linha, coluna] = matriz_global[linha,coluna] + rigidez_1[i, j]

        return matriz_global.round(3)








class Calculos():
    def __init__(self, matriz_global, desloc, cargas, apoios,barra):
        self.matriz_global = matriz_global
        self.desloc = desloc
        self.cargas = cargas
        self.apoios = apoios
        self.barra = barra

    def deslocamentos(self):
        desloc = np.zeros((np.size(self.desloc),np.size(self.desloc)))
        size = int(np.size(self.matriz_global)**(1/2))

        for linha in range(size):  # linha matrix grande
            for coluna in range(size):  # coluna matriz grande
                for i, a in enumerate(self.desloc):  # linha matrix pequena
                    for j, b in enumerate(self.desloc):  # coluna matrix pequena
                        if [linha, coluna] == [a, b]:
                            desloc[i, j] = self.matriz_global[linha, coluna]
        deslocamentos_gloabais = np.linalg.solve(desloc,self.cargas)


        return deslocamentos_gloabais

    def reacao_apoios(self):
        reacoes = np.zeros((np.size(self.apoios),2))
        size = int(np.size(self.matriz_global)**(1/2))


        for linha in range(size):  # linha matrix grande
            for coluna in range(size):  # coluna matriz grande
                for i, a in enumerate(self.apoios):  # linha matrix pequena
                    for j, b in enumerate(self.desloc):  # coluna matrix pequena
                        if [linha, coluna] == [a, b]:
                            #a=1
                            reacoes[i, j] = self.matriz_global[linha, coluna]
        reacoes_gloabais = np.sum(np.multiply(reacoes,self.deslocamentos()),axis=1).round(2)

        return reacoes_gloabais

    def deslocamentos_globais(self):
        deslocamentos_pontuais = self.deslocamentos()
        size = int(np.size(self.matriz_global) ** (1 / 2))
        deslocamentos_globais = np.zeros((size))


        for linha in range(size):  # linha matrix grande
            for i, a in enumerate(self.desloc):  # linha matrix pequena
                if linha == a:
                    deslocamentos_globais[linha] = deslocamentos_pontuais[i]
                    #deslocamentos_globais[i,j] = self.matriz_global[linha][coluna]
        return deslocamentos_globais

    def esforcos(self):
        size = int(np.size(self.matriz_global) ** (1 / 2))
        deslocamento = self.deslocamentos_globais()
        esforcos = np.zeros(4)

        for linha in range(size):  # linha matrix grande
            for i, a in enumerate(self.barra.posicao):  # linha matrix pequena
                if linha == a:
                    esforcos[i] = deslocamento[linha]

        return np.sum(np.multiply(esforcos,self.barra.vetores),axis=0).round(3)



ponto1 = Pontos(0,0,1,1,0,-10)
ponto2 = Pontos(2,0,0,0,0,0)
ponto3 = Pontos(4,0,0,0,0,0)
ponto4 = Pontos(6,0,0,0,0,0)
ponto5 = Pontos(8,0,1,1,0,-10)
ponto6 = Pontos(2,1,0,0,0,-10)
ponto7 = Pontos(6,1,0,0,0,-10)
ponto8 = Pontos(4,2,0,0,0,-10)

area = 1
elasticidade = 1000000

barra_1 = Elementos(ponto1,ponto2,elasticidade,area)
barra_2 = Elementos(ponto2,ponto3,elasticidade,area)
barra_3 = Elementos(ponto3,ponto4,elasticidade,area)
barra_4 = Elementos(ponto4,ponto5,elasticidade,area)
barra_5 = Elementos(ponto1,ponto6,elasticidade,area)
barra_6 = Elementos(ponto6,ponto8,elasticidade,area)
barra_7 = Elementos(ponto8,ponto7,elasticidade,area)
barra_8 = Elementos(ponto7,ponto5,elasticidade,area)
barra_9 = Elementos(ponto2,ponto6,elasticidade,area)
barra_10 = Elementos(ponto3,ponto8,elasticidade,area)
barra_11 = Elementos(ponto4,ponto7,elasticidade,area)
barra_12 = Elementos(ponto3,ponto6,elasticidade,area)
barra_13 = Elementos(ponto3,ponto7,elasticidade,area)




matriz_global = Matriz_global(Pontos.count,Elementos.count1,Elementos.rigidez_elementos,Elementos.posicao_global).calculo_matriz()
barra_1_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_1)
barra_2_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_2)
barra_3_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_3)
barra_4_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_4)
barra_5_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_5)
barra_6_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_6)
barra_7_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_7)
barra_8_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_8)
barra_9_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_9)
barra_10_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_10)
barra_11_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_11)
barra_12_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_12)
barra_13_1 = Calculos(matriz_global,Pontos.cargas_ps,Pontos.cargas,Pontos.apoios,barra_13)


#print(Pontos.count,Elementos.count1,Elementos.rigidez_elementos,Elementos.posicao_global)

#print(matriz_global)

#print(barra_2_1.cargas)

print(barra_1_1.esforcos())
print(barra_2_1.esforcos())
print(barra_3_1.esforcos())
print(barra_4_1.esforcos())
print(barra_5_1.esforcos())
print(barra_6_1.esforcos())
print(barra_7_1.esforcos())
print(barra_8_1.esforcos())
print(barra_9_1.esforcos())
print(barra_10_1.esforcos())
print(barra_11_1.esforcos())
print(barra_12_1.esforcos())
print(barra_13_1.esforcos())

