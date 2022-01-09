import cv2
import random
import numpy as np
from ContornoDeDetecção import DetectaObjetoHSV

ListaQuadrado = []
x = y = w = h = score = valor = 0
gameover = False
passou = 5

captura = cv2.VideoCapture(0)


class Quadrado:
    def __init__(self, cor, velocidade, largura, altura, passou, score):
        self.Cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.largura = largura
        self.cor = self.Cores[cor]
        self.velocidade = velocidade
        self.altura = altura

    def Rodada(self, x, y, w, h, img, listaQuadrados):
        self.largura -= self.velocidade
        #Compara se o Quadrado está colidindo com o objeto
        if (x < self.largura+20) and (x+w > self.largura) and (y < self.altura+20) and (y+h > self.altura):
            global score
            score += 1
            listaQuadrados.remove(self)
            del self
        #Colidiu com a linha de chegada
        elif self.largura <= 40:
            global passou
            passou -= 1
            listaQuadrados.remove(self)
            del self
        else:
            cv2.rectangle(img, (self.largura, self.altura), (self.largura+20, self.altura+20), self.cor, -1)







while True:
    gravando, imagem = captura.read(0)

    if not gravando:
        break

    #Espelhando a imagem
    imagem = cv2.flip(imagem,1)

    #Pegando as dimensões da imagem
    altura = imagem.shape[0]
    largura = imagem.shape[1]

    #Transformando a imagem em cinza com 3 canais de cores
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    img2 = np.zeros_like(imagem)
    img2[:, :, 0] = gray
    img2[:, :, 1] = gray
    img2[:, :, 2] = gray
    gray = img2

    #Desenhando a Linha de chegada, Score e as Vidas
    cv2.rectangle(gray, (40, 0), (40, altura), (0, 0, 0), 5)
    cv2.putText(gray, f"Score:{score}", (100, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255))
    cv2.putText(gray, f"Vidas:{passou}", (340, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255))

    #Pegando os pontos do objeto detectado
    x, y, w, h = DetectaObjetoHSV(imagem, gray)

    #Desenho do retangulo na imagem colorida
    cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #Desenha os quadrados na tela e muda o Score/Vidas
    if not gameover:
        for i in ListaQuadrado:
            i.Rodada(x, y, w, h, gray, ListaQuadrado)

    if passou <= 0:
        gameover = True
        cv2.putText(gray, "Fim de jogo", (250, 200), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255))


    #Criando novo Quadrado a cada 7 loops do while se não tiver acabado o jogo
    if not gameover:
        valor += 1
        if valor % 7 == 0:
            valor = 0
            ListaQuadrado.append(Quadrado(random.randrange(3), random.randrange(1, 4, 1), largura, random.randrange(altura-10), passou, score))

    cv2.imshow("Jogo", gray)
    cv2.imshow("Video", imagem)

    tecla = cv2.waitKey(1)

    if tecla == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()
