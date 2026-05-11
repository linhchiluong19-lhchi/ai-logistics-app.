import streamlit as st
import easyocr
import numpy as np
from PIL import Image
from fuzzywuzzy import fuzz

st.set_page_config(page_title="AI Logistics Pro", layout="wide")

# Giao diện tiêu đề
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🛡️ Hệ thống Giám sát Logistics Thông minh</h1>", unsafe_allow_html=True)
st.write("---")

# Nạp mô hình AI (Tối ưu RAM)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['vi', 'en'], gpu=False)

reader = load_reader()

# Thanh bên trái
st.sidebar.header("📂 Tải vận đơn")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh vận đơn (JPG, PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.sidebar.image(img, caption="Ảnh đã tải lên", use_container_width=True)
    
    with st.spinner("🤖 AI đang quét dữ liệu..."):
        # Chuyển ảnh sang dạng AI đọc được
        img_np = np.array(img)
        # detail=0 giúp AI chạy nhanh hơn và tiết kiệm RAM
        results = reader.readtext(img_np, detail=0, paragraph=True)
        raw_text = " ".join(results).lower()

    # Giao diện chính: Chia làm 2 cột để nhập liệu
    st.subheader("📝 Đối soát thông tin chi tiết")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hawb_no = st.text_input("1. Mã vận đơn (HAWB No):")
        flight_no = st.text_input("2. Số chuyến bay (Flight No):")
        shipper = st.text_input("3. Người gửi (Shipper):")
        weight = st.text_input("4. Trọng lượng (GW):")

    with col2:
        dest = st.text_input("5. Nơi đến (To/Dest):")
        consignee = st.text_input("6. Người nhận (Consignee):")
        pcs = st.text_input("7. Số kiện (Pieces):")
        nature = st.text_input("8. Loại hàng (Nature of Goods):")

    if st.button("🔍 Bắt đầu đối soát hệ thống"):
        st.write("### Kết quả kiểm tra:")
        
        # Danh sách các thông tin cần kiểm tra
        check_list = {
            "Mã vận đơn": hawb_no,
            "Chuyến bay": flight_no,
            "Người gửi": shipper,
            "Người nhận": consignee,
            "Nơi đến": dest,
            "Trọng lượng": weight,
            "Số kiện": pcs,
            "Loại hàng": nature
        }

        # Vẽ bảng kết quả
        for label, user_val in check_list.items():
            if user_val: # Chỉ kiểm tra nếu bạn có nhập vào ô
                # So khớp mờ (Fuzzy matching)
                score = fuzz.partial_ratio(user_val.lower(), raw_text)
                
                if score >= 80:
                    st.success(f"✅ {label}: **KHỚP** (Độ tin cậy: {score}%)")
                else:
                    st.error(f"❌ {label}: **KHÔNG KHỚP** (Độ tin cậy: {score}%)")
            else:
                st.warning(f"⚠️ {label}: Chưa nhập dữ liệu để đối soát.")

else:
    st.info("Vui lòng tải ảnh vận đơn ở thanh bên trái để bắt đầu.")
