import cv2
import numpy as np

captura = cv2.VideoCapture(0)
cv2.namedWindow("HSVFiltro")
# cv2.resizeWindow("HSVFiltro", 800, 600)


def PraMostrarOValor(trackBar):
    print(trackBar)


cv2.createTrackbar("H-", "HSVFiltro", 0, 255, PraMostrarOValor)
cv2.createTrackbar("H+", "HSVFiltro", 0, 255, PraMostrarOValor)

cv2.createTrackbar("S-", "HSVFiltro", 0, 255, PraMostrarOValor)
cv2.createTrackbar("S+", "HSVFiltro", 0, 255, PraMostrarOValor)

cv2.createTrackbar("V-", "HSVFiltro", 0, 255, PraMostrarOValor)
cv2.createTrackbar("V+", "HSVFiltro", 0, 255, PraMostrarOValor)

cv2.setTrackbarPos("H+", "HSVFiltro", 255)
cv2.setTrackbarPos("S+", "HSVFiltro", 255)
cv2.setTrackbarPos("V+", "HSVFiltro", 255)


while True:
    Rodando, Imagem = captura.read()

    if not Rodando:
        break

    hMin = cv2.getTrackbarPos('H-', 'HSVFiltro')
    sMin = cv2.getTrackbarPos('S-', 'HSVFiltro')
    vMin = cv2.getTrackbarPos('V-', 'HSVFiltro')
    hMax = cv2.getTrackbarPos('H+', 'HSVFiltro')
    sMax = cv2.getTrackbarPos('S+', 'HSVFiltro')
    vMax = cv2.getTrackbarPos('V+', 'HSVFiltro')

    Claro = np.array([hMin, sMin, vMin])
    Escuro = np.array([hMax, sMax, vMax])

    hsv = cv2.cvtColor(Imagem, cv2.COLOR_BGR2HSV_FULL)
    Mascara = cv2.inRange(hsv, Claro, Escuro)
    Saida = cv2.bitwise_and(Imagem, Imagem, mask=Mascara)

    SaidaCinza = cv2.cvtColor(Saida, cv2.COLOR_BGR2GRAY)
    _, SaidaCinza = cv2.threshold(SaidaCinza, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contornos, hierarquia = cv2.findContours(SaidaCinza, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if contornos:
        MaxArea = cv2.contourArea(contornos[0])
        IndiceDoMaiorContorno = 0
        i = 0
        for cnt in contornos:
            if MaxArea < cv2.contourArea(cnt):
                MaxArea = cv2.contourArea(cnt)
                IndiceDoMaiorContorno = i
            i += 1

        ContornoComMaiorArea = contornos[IndiceDoMaiorContorno]
        # boundingRect retorna um retanguo que envolve o contorno
        x, y, w, h = cv2.boundingRect(ContornoComMaiorArea)

        cv2.rectangle(Imagem, (x, y), (x + w, y + h), (0, 255, 0), 2)


    ImagemESaida = np.hstack([Imagem,Saida])

    cv2.imshow("HSVFiltro", ImagemESaida)
    tecla = cv2.waitKey(1)
    if tecla == ord("q"):
        break
    if tecla == ord("s"):
        BlocoDeNotas = open("Cores.txt", "a")
        NomeDaCor = input("Digite o nome da cor: ")
        Claro = f"Claro = np.array([{hMin}, {sMin}, {vMin}])"
        Escuro = f"Escuro = np.array([{hMax}, {sMax}, {vMax}])"
        BlocoDeNotas.writelines(f"\n{NomeDaCor}:\n{Claro}\n{Escuro}")
        BlocoDeNotas.close()
        print(Claro)
        print(Escuro)

captura.release()
cv2.destroyAllWindows()
