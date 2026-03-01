import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import os

# 1. إعدادات الصفحة باسم الوالد (تظهر في تبويب المتصفح)
st.set_page_config(page_title="Rashid's Holy Library", page_icon="📖")

# 2. تصميم الواجهة العلوية (Header)
st.title("📖 Rashid's Holy Library")
st.markdown("### *Dedicated to my beloved father, Rashid*")
st.info("Choose a book and enter the page number to start reading.")

# 3. قاموس الكتب (تأكد من مطابقة أسماء الملفات في GitHub تماماً)
books_config = {
    "Holy Quran (Tafseer)": "Tafseer_Muyassar__1440.pdf",
    "Gospel of Matthew": "matthew.pdf",
    "Gospel of Mark": "mark.pdf",
    "Gospel of Luke": "luke.pdf",
    "Gospel of John": "john.pdf"
}

# 4. دالة استخراج الصفحة (مع تحسين جودة الخط لراحة عين الوالد)
def get_pdf_page(pdf_path, page_num):
    try:
        # التأكد من وجود الملف قبل محاولة فتحه لتجنب الخطأ الذي ظهر لك
        if not os.path.exists(pdf_path):
            return "file_not_found", 0
            
        doc = fitz.open(pdf_path)
        if page_num > len(doc) or page_num < 1:
            return "out_of_range", len(doc)
            
        page = doc.load_page(page_num - 1) 
        
        # زيادة التكبير (Zoom) ليكون النص كبيراً جداً للوالد
        zoom = 2.5 
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img, len(doc)
    except Exception as e:
        return str(e), 0

# 5. واجهة المستخدم باللغة الإنجليزية
col1, col2 = st.columns([2, 1])

with col1:
    selected_book_name = st.selectbox("Select the Book:", list(books_config.keys()))

with col2:
    page_input = st.number_input("Page Number:", min_value=1, value=1, step=1)

# 6. زر العرض (Display Button)
if st.button("Display Page Now"):
    pdf_file = books_config[selected_book_name]
    
    with st.spinner(f'Opening {selected_book_name}...'):
        result, total_pages = get_pdf_page(pdf_file, page_input)
        
        if isinstance(result, Image.Image):
            st.success(f"Page {page_input} of {total_pages}")
            st.image(result, caption=f"{selected_book_name} - Page {page_input}", use_container_width=True)
        elif result == "out_of_range":
            st.error(f"Page number not found. This book has only {total_pages} pages.")
        elif result == "file_not_found":
            st.error(f"Error: File '{pdf_file}' not found. Please upload it to GitHub in the main directory.")
        else:
            st.error(f"An unexpected error occurred: {result}")

# 7. التذييل (Footer)
st.divider()
st.caption("Developed with love for Rashid | 2026")