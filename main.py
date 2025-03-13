import streamlit as st
import requests

def create_download_button(url, filename):
    html = f"""
    <a href="{url}" download="{filename}" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Download {filename}</a>
    """
    return html

def upload_file_to_filebin(file_path, url):
    print(url)
    try:
        with open(file_path, 'rb') as file:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/octet-stream'
            }
            
            response = requests.post(url, headers=headers, data=file)
            
            if response.status_code == 201:
                print("File uploaded successfully.")
                # Check response body for any additional information
                print("Response Body:", response.text)
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
                print("Response Body:", response.text)
            
            return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    st.title("File Sharing")
    
    # Add expandable guide section
    with st.expander("📘 How to Use This App", expanded=False):
        st.markdown("""
        **Welcome to File Sharing App!** Here's how to use it:

        ### 📤 Upload Files
        1. Click 'Browse files' to select one or more files from your device
        2. Enter upload URL in format: `folder_name/`
           - Example: `my_documents/`
        3. Click 'Upload Files'
        4. Wait for confirmation message

        ### 📥 Download Files
        1. Enter the exact folder name from Filebin
        2. Click 'Search folder'
        3. Click the download button that appears

        ⚠️ **Important Notes:**
        - Supported formats: TXT, PDF, JPG, PNG
        - Files are temporary - download links may expire
        - Folder names are case-sensitive
        """)

    get_zip = st.text_input("Search folder to download")
    search_file = st.button("search folder")
    if(search_file):
        try:
            st.text("https://filebin.net/archive/{}/zip".format(get_zip))
            html = create_download_button("https://filebin.net/archive/{}/zip".format(get_zip),"")
            st.markdown(html, unsafe_allow_html=True)
        except:
            st.error("Error occrured")

    files = st.file_uploader("Choose one or more files", type=['txt', 'pdf', 'jpg', 'png'], accept_multiple_files=True)
    
    if files is not None:
        url = st.text_input("Enter the upload URL (folder name only)")
        
        if st.button("Upload Files"):
            for file in files:
                file_path = f"temp_file_{file.name}"
                with open(file_path, 'wb') as f:
                    f.write(file.getbuffer())
                
                response = upload_file_to_filebin(file_path, f"https://filebin.net/{url}/{file.name}")
                if response is not None:
                    st.write(f"File {file.name} uploaded with status code: {response.status_code}")
                    st.write("Response Body:", response.text)
                else:
                    st.write(f"Upload of {file.name} failed. Check the logs for details.")
                
                # Clean up the temporary file
                import os
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to remove temporary file: {e}")

main()

