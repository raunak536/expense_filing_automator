import pytesseract
from PIL import Image
import cv2


def extract_text(image_path):
    processed_path = preprocess_image(image_path)
    text = pytesseract.image_to_string(Image.open(processed_path))
    print(text)
    return text

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 135, 255, cv2.THRESH_BINARY)
    processed_path = image_path.split('.')[0] + '.png'
    cv2.imwrite(processed_path, thresh)
    return processed_path