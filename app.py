import streamlit as st
import boto3
import json
from PIL import Image
import io
import base64

# Streamlit UI
st.title("Image Generator - Amazon Titan")
st.subheader("Generación de imágenes mediante Bedrock (Titan Image Generator v2)")

# AWS Client
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# -------- CONVERSIÓN BASE64 → PIL --------
def base64_to_pil(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

# -------- FUNCIÓN PARA LLAMAR A TITAN --------
def generate_image_titan(prompt):
    """
    Llama al modelo amazon.titan-image-generator-v2:0
    y devuelve la imagen en formato PIL.
    """

    body = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 1024,
            "width": 1024,
            "cfgScale": 8,
            #"quality": "high",
            "seed": 0
        }
    }

    try:
        response = bedrock_runtime.invoke_model(
            modelId="amazon.titan-image-generator-v2:0",
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response["body"].read())
        base64_img = response_body["images"][0]

        return base64_to_pil(base64_img)

    except Exception as e:
        st.error(f"Hubo un error al generar la imagen: {e}")
        return None


# -------- UI --------
prompt = st.text_input("Escribe tu prompt para generar la imagen:")

if st.button("Generar Imagen"):
    if prompt.strip() == "":
        st.warning("Por favor ingresa un prompt.")
    else:
        st.info("Generando imagen, espera un momento...")
        image = generate_image_titan(prompt)

        if image:
            st.image(image, caption="Imagen generada con Titan v2", use_container_width=True)
