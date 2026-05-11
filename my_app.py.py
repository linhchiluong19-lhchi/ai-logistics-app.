import streamlit as st
import easyocr
import numpy as np
from PIL import Image
from fuzzywuzzy import fuzz

st.set_page_config(page_title="AI Logistics App", layout="wide")
st.title("🛡️ Hệ thống Giám sát AI Logistics")

@st.cache_resource
def load_reader():
    # Trên server Streamlit không cần quan tâm lỗi card đồ họa 1114
    return easyocr.Reader(['vi', 'en'], gpu=False)

reader = load_reader()

st.sidebar.header("📂 Tải vận đơn")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.sidebar.image(img, use_container_width=True)
    with st.spinner("🤖 AI đang đọc dữ liệu..."):
        img_np = np.array(img)
        results = reader.readtext(img_np)
        raw_text = " ".join([res[1] for res in results]).lower()

    st.subheader("📝 Đối soát thông tin")
    col1, col2 = st.columns(2)
    with col1:
        hawb_no = st.text_input("Mã vận đơn (HAWB No):")
        weight = st.text_input("Trọng lượng (GW):")
    with col2:
        dest = st.text_input("Nơi đến (Dest):")
        consignee = st.text_input("Người nhận (Consignee):")
    
    if st.button("🔍 Bắt đầu giám sát"):
        fields = {"Mã vận đơn": hawb_no, "Trọng lượng": weight, "Nơi đến": dest, "Người nhận": consignee}
        for label, val in fields.items():
            if val:
                score = fuzz.partial_ratio(val.lower(), raw_text)
                if score > 80: st.success(f"✅ {label}: KHỚP ({score}%)")
                else: st.error(f"❌ {label}: KHÔNG KHỚP! ({score}%)")