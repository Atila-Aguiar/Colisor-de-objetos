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
        Claro = f"Claro = [{hMin}, {sMin}, {vMin}]"
        Escuro = f"Escuro = [{hMax}, {sMax}, {vMax}]"
        BlocoDeNotas.writelines(f"\n{NomeDaCor}:\n{Claro}\n{Escuro}")
        BlocoDeNotas.close()
        print(Claro)
        print(Escuro)

captura.release()
cv2.destroyAllWindows()



# import cv2
# import numpy as np
#
# def nothing(x):
#     pass
#
# # Load image
# image = cv2.imread('1.jpg')
#
# # Create a window
# cv2.namedWindow('image')
#
# # Create trackbars for color change
# # Hue is from 0-179 for Opencv
# cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
# cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
# cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
# cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
# cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
# cv2.createTrackbar('VMax', 'image', 0, 255, nothing)
#
# # Set default value for Max HSV trackbars
# cv2.setTrackbarPos('HMax', 'image', 179)
# cv2.setTrackbarPos('SMax', 'image', 255)
# cv2.setTrackbarPos('VMax', 'image', 255)
#
# # Initialize HSV min/max values
# hMin = sMin = vMin = hMax = sMax = vMax = 0
# phMin = psMin = pvMin = phMax = psMax = pvMax = 0
#
# while(1):
#     # Get current positions of all trackbars
#     hMin = cv2.getTrackbarPos('HMin', 'image')
#     sMin = cv2.getTrackbarPos('SMin', 'image')
#     vMin = cv2.getTrackbarPos('VMin', 'image')
#     hMax = cv2.getTrackbarPos('HMax', 'image')
#     sMax = cv2.getTrackbarPos('SMax', 'image')
#     vMax = cv2.getTrackbarPos('VMax', 'image')
#
#     # Set minimum and maximum HSV values to display
#     lower = np.array([hMin, sMin, vMin])
#     upper = np.array([hMax, sMax, vMax])
#
#     # Convert to HSV format and color threshold
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv, lower, upper)
#     result = cv2.bitwise_and(image, image, mask=mask)
#
#     # Print if there is a change in HSV value
#     if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
#         print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
#         phMin = hMin
#         psMin = sMin
#         pvMin = vMin
#         phMax = hMax
#         psMax = sMax
#         pvMax = vMax
#
#     # Display result image
#     cv2.imshow('image', result)
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
#
# cv2.destroyAllWindows()