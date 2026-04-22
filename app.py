import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Инициализация на OCR четеца (поддържа английски + български)
reader = easyocr.Reader(['en', 'bg'], gpu=False)

st.title("📷 OCR проверка за вредни съставки")

st.write("Качи снимка на етикет с продукти, за да открием потенциално вредни съставки (напр. E621).")

uploaded_file = st.file_uploader("Качи изображение", type=["jpg", "jpeg", "png"])

# Списък с вредни съставки (може да разшириш)
harmful_ingredients = ["621", "E621", "E 621"]

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_column_width=True)

    # Преобразуване в numpy формат
    image_np = np.array(image)

    with st.spinner("Разчитане на текста..."):
        results = reader.readtext(image_np, detail=0)

    extracted_text = " ".join(results)

    st.subheader("📄 Разчетен текст:")
    st.write(extracted_text)

    # Търсене на вредни съставки
    found = [ingredient for ingredient in harmful_ingredients if ingredient.lower() in extracted_text.lower()]

    st.subheader("⚠️ Открити вредни съставки:")
    if found:
        for item in found:
            st.error(f"Открито: {item}")
    else:
        st.success("Не са открити вредни съставки 🎉")
