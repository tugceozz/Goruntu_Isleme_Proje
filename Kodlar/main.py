import os
from cvzone.HandTrackingModule import HandDetector
import cv2


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4,480)

imgBackground = cv2.imread("Resources/Background.png")

# "Modes" klasöründeki tüm mod resimlerini bir liste olarak içe aktarıyoruz
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes,imgModePath)))
print(listImgModes)

# "Icons" klasöründeki tüm ikonları bir liste olarak içe aktarıyoruz
folderPathIcons = "Resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconsPath in listImgIconsPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons,imgIconsPath)))


modeType = 0            # seçim modunu temsil eder.
selection = -1          # mevcut seçimi temsil eder.
counter = 0             # seçim sürecinin sayacını temsil eder.
selectionSpeed = 8      # seçim animasyonunun hızını belirler.
detector = HandDetector(detectionCon=0.8, maxHands=1)
modePositions = [(1136, 196), (1000, 384), (1136, 581)]      # modların konumlarını içerir. Her bir (x, y) koordinatı, bir modun konumunu temsil eder.
counterPause = 0                   # seçimler arasındaki duraklamayı kontrol eder.
selectionList = [-1, -1, -1]       # seçilen modların sırasıyla tutulmasını sağlar.

while True:
    success, img = cap.read()   # success değişkeni, karenin başarıyla okunup okunamadığını belirtir. img değişkeni, okunan kareyi temsil eder.
    # El ve el işaretlerini buluyoruz
    hands, img = detector.findHands(img)  # çizim yaparak
    # web kamerası görüntüsünü arka plan görüntüsünün üzerine yerleştiriyoruz
    imgBackground[139:139 + 480, 50:50 + 640] = img     # web kamerasının görüntüsünü arka plan görüntüsünün belirli bir bölgesine yerleştirir.
    imgBackground[0:720, 847:1280] = listImgModes[modeType]     #  seçilen modun görüntüsünü arka plan görüntüsünün belirli bir bölgesine yerleştirir.

    if hands and counterPause == 0 and modeType < 3:
        # El 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        if counter > 0:
            counter += 1
            print(counter)

            cv2.ellipse(imgBackground, modePositions[selection-1], (103, 103), 0, 0, counter * selectionSpeed, (0, 255, 0), 20)

            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1

    # her seçimden sonra duraklamak için
    if counterPause > 0:
        counterPause += 1
        if counterPause > 70:
            counterPause = 0

    # seçim ikonunu alt kısma ekliyoruz
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]

    # görüntüyü görüntülüyoruz
    # cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)

    # Bu kod,el izleme ile bir seçim arayüzü oluşturmak için kullanılan bir örnektir. El izleme yapmak için
    # "cvzone.HandTrackingModule" modülü kullanılıyor. Kod, el hareketlerini tanıyarak kullanıcının seçim
    # yapmasını sağlar. Bu seçimler,arka planda görüntülenen modları ve seçim ikonlarını değiştirir.