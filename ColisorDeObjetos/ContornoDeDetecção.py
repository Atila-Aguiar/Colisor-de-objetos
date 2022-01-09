import cv2
import numpy as np


def DetectaObjetoHSV(imagem, img2):
    #Cor Azul Claro/Escuro
    Claro = np.array([101, 104, 65])
    Escuro = np.array([176, 255, 255])

    # Converte a imagem para hsv
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV_FULL)
    # Separa a imagem hsv para saber se os pixeis pertencem ao intervalo ou não
    Mascara = cv2.inRange(hsv, Claro, Escuro)
    # Aplica a mascara e só deixar passar apenas pixeis do intervalo do Escuro~Claro
    Saida = cv2.bitwise_and(imagem, imagem, mask=Mascara)

    #SaidaGray e img2 tem o mesmo retorno, não consegui deixar a cor original na imagem cinza :C
    SaidaGray = cv2.bitwise_not(imagem, img2, mask=Mascara)

    # Transforma a Saida em cinza para facilitar a limiarização
    SaidaCinza = cv2.cvtColor(Saida, cv2.COLOR_BGR2GRAY)
    # Aplica a limiarização
    _, SaidaCinza = cv2.threshold(SaidaCinza, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Da limiarização ele consegue pega o contorno e a hierarquia
    contornos, hierarquia = cv2.findContours(SaidaCinza, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Se existir algum contorno
    if contornos:
        # Ele vai colocar aqui na primeira area que encontrar
        MaxArea = cv2.contourArea(contornos[0])
        IndiceDoMaiorContorno = 0
        i = 0

        # Vai percorrer todos os contornos para encontrar a maior area
        for cnt in contornos:
            # Procura a maior area
            if MaxArea < cv2.contourArea(cnt):
                MaxArea = cv2.contourArea(cnt)
                IndiceDoMaiorContorno = i
            i += 1

        ContornoComMaiorArea = contornos[IndiceDoMaiorContorno]
        # boundingRect retorna um retanguo que envolve o contorno
        return cv2.boundingRect(ContornoComMaiorArea)

    return 0, 0, 0, 0