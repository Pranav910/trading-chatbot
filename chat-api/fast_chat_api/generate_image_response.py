from mistralai import Mistral
from load_image_b64 import load_image

def generate_ocr_response(image_path):

    ocr_model = Mistral(api_key="6gLQ51YLy3XLl2yniTWxlMzCDXOzYtI8")

    image = load_image(image_path)

    ocr_response = ocr_model.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{image}" 
        }
    )

    return ocr_response.pages[0].markdown