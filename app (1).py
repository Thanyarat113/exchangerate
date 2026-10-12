import streamlit as st
import requests
import pandas as pd

# ตั้งค่าหัวข้อเว็บแอป
st.set_page_config(page_title="Currency Exchange Rate App", page_icon="💱", layout="centered")

st.title("💱 โปรแกรมแสดงและแปลงอัตราแลกเปลี่ยนเงินตรา")
st.markdown("เรียกใช้งานข้อมูลแบบเรียลไทม์จาก **ExchangeRate-API**")

# ฟังก์ชันดึงเรทอัตราแลกเปลี่ยนผ่าน API แบบฟรี (ไม่ต้องใช้ API Key)
@st.cache_data(ttl=3600)
def get_rates(base="USD"):
    url = f"https://open.er-api.com/v6/latest/{base}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("rates", {})
    return None

# Sidebar เลือกสกุลเงินตั้งต้น
st.sidebar.header("⚙️ ตั้งค่าสกุลเงิน")
base_currency = st.sidebar.selectbox("เลือกสกุลเงินหลัก (Base):", ["USD", "THB", "EUR", "GBP", "JPY", "SGD"], index=0)

rates = get_rates(base_currency)

if rates:
    # ส่วนคำนวณแปลงเงิน
    st.subheader("🧮 เครื่องมือคำนวณอัตราแลกเปลี่ยน")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        amount = st.number_input("จำนวนเงิน:", min_value=0.0, value=100.0, step=10.0)
    with col2:
        target_currency = st.selectbox("แปลงเป็นสกุลเงิน:", options=list(rates.keys()), index=list(rates.keys()).index("THB") if "THB" in rates else 1)
    
    if target_currency in rates:
        converted = amount * rates[target_currency]
        with col3:
            st.metric(label=f"ยอดเงินที่แปลงได้ ({target_currency})", value=f"{converted:,.2f}")
        st.info(f"💡 อัตราแลกเปลี่ยน ณ ปัจจุบัน: 1 {base_currency} = {rates[target_currency]:,.4f} {target_currency}")

    st.divider()

    # ส่วนแสดงตารางอัตราแลกเปลี่ยนทั้งหมด
    st.subheader(f"📊 ตารางอัตราแลกเปลี่ยนทั้งหมด (เทียบกับ {base_currency})")
    df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
    
    # ช่องค้นหาสกุลเงินในตาราง
    search = st.text_input("🔍 ค้นหาสกุลเงิน (เช่น THB, EUR):", "").upper()
    if search:
        df = df[df["Currency"].str.contains(search)]
        
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.error("ไม่สามารถเชื่อมต่อกับ API ได้ในขณะนี้")
