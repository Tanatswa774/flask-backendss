import cv2
import numpy as np

def find_template(image_path, template_path, threshold=0.8):
    img = cv2.imread(image_path)
    template = cv2.imread(template_path)

    if img is None:
        raise ValueError(f"Could not read {image_path}")
    if template is None:
        raise ValueError(f"Could not read {template_path}")

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    return list(zip(*loc[::-1]))  # (x, y) coordinates
