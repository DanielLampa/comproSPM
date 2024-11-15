import streamlit as st
import PyPDF2
import io
import pyzipper

def encrypt_pdf(file, password):
    # Initialize the PDF reader and writer
    reader = PyPDF2.PdfReader(file)
    writer = PyPDF2.PdfWriter()

    # Add pages from the original PDF to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Encrypt the PDF
    writer.encrypt(password)

    # Write the encrypted PDF to a BytesIO object
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    return output.getvalue()

st.title("COMPRO PDF/ZIP Encryption Tool")
   
name = st.text_input("Name")
password = st.text_input("Enter Password for Encryption", type="password")

if password and name:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Encrypt PDF Files")
    uploaded_files = st.file_uploader("Choose PDF files to encrypt", type="pdf", accept_multiple_files=True)
        
    if uploaded_files:
        encrypted_files = []
        for uploaded_file in uploaded_files:
            # Check if the file extension is .pdf (case insensitive)
            if uploaded_file.name.lower().endswith('.pdf'):
                encrypted_pdf = encrypt_pdf(uploaded_file, password)
                encrypted_files.append((uploaded_file.name, encrypted_pdf))
            else:
                st.toast(f"Warning: {uploaded_file.name} is not a PDF file. Skipping encryption.", icon='😭')

        # Create a ZIP file in memory
        zip_buffer = io.BytesIO()

        # Open a pyzipper AESZipFile with password encryption
        with pyzipper.AESZipFile(zip_buffer, 'w', encryption=pyzipper.WZ_AES) as zipf:
            # Convert password to bytes and set it
            zipf.setpassword(password.encode('utf-8'))

            # Write encrypted PDFs into the ZIP archive
            for file_name, encrypted_pdf in encrypted_files:
                zipf.writestr(file_name, encrypted_pdf)
                st.toast('Encryption Done', icon='😍')

        # Seek to the beginning of the buffer to prepare for download
        zip_buffer.seek(0)

        # Offer the encrypted ZIP file for download
        st.download_button(
            label="Download Encrypted ZIP",
            data=zip_buffer,
            file_name=f"{name}.zip",
            mime='application/zip'
        )
