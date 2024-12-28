from flask import Flask, request, send_file, render_template
from io import BytesIO
from PIL import Image
import torch
import torchvision.transforms as transforms
import cv2
import numpy as np
import os


from model.ImageRestoration_model import RestorationNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = Flask(__name__)


model_path = os.path.join("model", "Final_RestorationModel.pth")
model = RestorationNet().to(device)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

transform_to_tensor = transforms.ToTensor()
transform_to_pil = transforms.ToPILImage()

import cv2
import numpy as np

def Image_PostProcessing(image):
    bf = cv2.bilateralFilter(image, d=5, sigmaColor=75, sigmaSpace=75)
    limg = cv2.cvtColor(bf, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(limg)
    c = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = c.apply(l)
    el = cv2.merge((l, a, b))
    ce = cv2.cvtColor(el, cv2.COLOR_LAB2BGR)
    hsv_img = cv2.cvtColor(ce, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_img)
    brgt_scale = 1.5
    str_scale = 2.2 
    v = np.clip(v * brgt_scale, 0, 255).astype(np.uint8)
    s = np.clip(s * str_scale, 0, 255).astype(np.uint8)
    adj_hsv = cv2.merge((h, s, v))
    bv_img = cv2.cvtColor(adj_hsv, cv2.COLOR_HSV2BGR)
    gauss = cv2.GaussianBlur(bv_img, (9, 9), 10.0)
    shr_img = cv2.edgePreservingFilter(gauss, flags=1, sigma_s=100, sigma_r=0.2)
    return shr_img

def Image_PostProcessing2(image):
    limg = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(limg)
    c = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = c.apply(l)
    l = cv2.add(l, 40)  
    el = cv2.merge((l, a, b))
    res_img = cv2.cvtColor(el, cv2.COLOR_LAB2BGR)
    kernel = np.array([[0, -0.3, 0],
                      [-0.3, 2.2, -0.3],
                      [0, -0.3, 0]])
    sharpened = cv2.filter2D(res_img, -1, kernel)
    hsv = cv2.cvtColor(sharpened, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.multiply(s, 1.15) 
    v = cv2.multiply(v, 1.0) 
    final_hsv = cv2.merge((h, s, v))
    final_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return final_image


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/restore', methods=['POST'])
def restore_image():
    # Get the uploaded image
    file = request.files['image']
    input_image = Image.open(file).convert('RGB')

    input_tensor = transform_to_tensor(input_image).unsqueeze(0).to(device)
    with torch.no_grad():
        restored_tensor = model(input_tensor)

    restored_tensor = restored_tensor.squeeze().cpu().clamp(0, 1)
    restored_image = transform_to_pil(restored_tensor)
    restored_image_np = np.array(restored_image)[:, :, ::-1] 
    Final_img = Image_PostProcessing(restored_image_np)
    Final_img = Image_PostProcessing2(Final_img)
    Final_img_rgb = cv2.cvtColor(Final_img, cv2.COLOR_BGR2RGB)  
    Final_img_pil = Image.fromarray(Final_img_rgb)
    buffer = BytesIO()
    Final_img_pil.save(buffer, format="JPEG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/jpeg')
if __name__ == '__main__':
    app.run(debug=True, port=5002)
