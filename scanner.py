import cv2

def find_template(screen_path, template_path, threshold=0.83):
    img = cv2.imread(screen_path)
    template = cv2.imread(template_path)
    if img is None or template is None:
        raise ValueError("Image or template not found.")
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    locations = zip(*((result >= threshold).nonzero()[::-1]))
    return [(int(x + template.shape[1] // 2), int(y + template.shape[0] // 2)) for (x, y) in locations]

def is_march_active(screen_path, march_icon_path="templates/march_active.png", threshold=0.8):
    img = cv2.imread(screen_path)
    template = cv2.imread(march_icon_path)
    if img is None or template is None:
        return False
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val > threshold
