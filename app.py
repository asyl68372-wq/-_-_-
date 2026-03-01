import streamlit as st
import fitz  # مكتبة PyMuPDF
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="المكتبة الشاملة", page_icon="📖")

st.title("📖 تطبيق عرض الكتب المقدسة")
st.write("اختر الكتاب الذي تريد تصفحه من القائمة أدناه.")

# قاموس يربط اسم الكتاب باسم الملف الموجود عندك في المجلد
books_config = {
    "القرآن الكريم (التفسير الميسر)": "Tafseer_Muyassar__1440.pdf",
    "إنجيل متى": "matthew.pdf",
    "إنجيل مرقس": "mark.pdf",
    "إنجيل لوقا": "luke.pdf",
    "إنجيل يوحنا": "john.pdf"
}

# دالة استخراج الصفحة وتحويلها لصورة
def get_pdf_page(pdf_path, page_num):
    try:
        doc = fitz.open(pdf_path)
        # التأكد من أن رقم الصفحة موجود في الملف
        if page_num > len(doc) or page_num < 1:
            return "out_of_range", len(doc)
            
        page = doc.load_page(page_num - 1) 
        # زيادة الدقة لجعل النص واضحاً
        zoom = 2 
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img, len(doc)
    except Exception as e:
        return str(e), 0

# واجهة المستخدم: اختيار الكتاب
selected_book_name = st.selectbox("اختر الكتاب:", list(books_config.keys()))

# واجهة المستخدم: إدخال رقم الصفحة
page_input = st.number_input("أدخل رقم الصفحة:", min_value=1, value=1, step=1)

if st.button("عرض الصفحة الآن"):
    # جلب اسم الملف بناءً على اختيار المستخدم
    pdf_file = books_config[selected_book_name]
    
    with st.spinner(f'جاري فتح {selected_book_name}...'):
        result, total_pages = get_pdf_page(pdf_file, page_input)
        
        if isinstance(result, Image.Image):
            st.success(f"تم عرض صفحة {page_input} من أصل {total_pages} صفحة")
            st.image(result, caption=f"{selected_book_name} - صفحة رقم {page_input}", use_container_width=True)
        elif result == "out_of_range":
            st.error(f"رقم الصفحة غير موجود. هذا الكتاب يحتوي على {total_pages} صفحة فقط.")
        else:
            st.error(f"خطأ: لم يتم العثور على الملف '{pdf_file}'. تأكد من وجوده في المجلد بجانب الكود.")

st.divider()
st.caption("التطبيق يدعم الآن القرآن الكريم والأناجيل الأربعة من ملفاتك المحلية.")