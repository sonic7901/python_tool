from PIL import Image
import pytesseract
import cv2
import re


def recognize_text(image):
    # 降噪點
    blur = cv2.pyrMeanShiftFiltering(image, sp=8, sr=60)
    cv2.imshow('dst', blur)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 185, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('binary', binary)
    # 反白
    cv2.bitwise_not(binary, binary)
    cv2.imshow('bg_image', binary)
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message, config='digits')
    # 保留數字
    result = re.sub("\D", "", text)
    print(f'result：{result}')


if __name__ == '__main__':
    src = cv2.imread(r'./getLoginCode.png')
    cv2.imshow('input image', src)
    recognize_text(src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



