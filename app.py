
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# إعداد واجهة التطبيق
st.set_page_config(page_title="خزنة المعنويات الدائمة", page_icon="✨")

st.title("✨ تطبيق حفظ الأشياء المعنوية (دائم)")
st.info("كل ما تحفظه هنا يتم تخزينه في ملف على جهازك ولا يضيع أبداً.")

# اسم الملف الذي ستخزن فيه البيانات
DB_FILE = "my_memories.csv"

# وظيفة لتحميل البيانات من الملف
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["التاريخ", "العنوان", "التصنيف", "الوصف", "الأثر"])

# تحميل البيانات الحالية
data_df = load_data()

# نموذج الإدخال
with st.form("my_form", clear_on_submit=True):
    title = st.text_input("ما هو الشيء المعنوي؟")
    category = st.selectbox("التصنيف", ["امتنان", "إنجاز", "ذكرى", "إلهام"])
    description = st.text_area("وصف الشعور أو الموقف:")
    impact = st.slider("مدى الأثر (1-10)", 1, 10, 5)
    
    submitted = st.form_submit_button("حفظ في الخزنة الدائمة")

if submitted:
    if title:
        new_entry = {
            "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "العنوان": title,
            "التصنيف": category,
            "الوصف": description,
            "الأثر": impact
        }
        # إضافة البيانات الجديدة وحفظها في الملف
        data_df = pd.concat([data_df, pd.DataFrame([new_entry])], ignore_index=True)
        data_df.to_csv(DB_FILE, index=False)
        st.success("تم الحفظ بأمان في ملفك الخاص! ✅")
        st.rerun() # تحديث الصفحة لإظهار البيانات الجديدة
    else:
        st.warning("يرجى كتابة عنوان.")

# عرض المحفوظات من الملف
if not data_df.empty:
    st.write("---")
    st.subheader("📜 سجل ذكرياتك المحفوظة (من الملف):")
    st.table(data_df)
    
    # زر اختياري لمسح كل البيانات
    if st.button("حذف كل السجل"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
