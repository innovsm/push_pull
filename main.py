import streamlit as st
import requests
def create_download_button(url, filename):
    html = f"""
    <a href="{url}" download="{filename}" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Download {filename}</a>
    """
    return html

def upload_file_to_filebin(file_path, url):
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
    get_zip = st.text_input("Search folder to download")
    search_file = st.button("search folder")
    if(search_file):
        try:
            st.text("https://filebin.net/archive/{}/zip".format(get_zip))
            html = create_download_button("https://filebin.net/archive/{}/zip".format(get_zip),"")
            st.markdown(html, unsafe_allow_html=True)
        except:
            st.error("Error occrured")
    file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'jpg', 'png'])
    
    if file is not None:
        file_path = "temp_file"
        with open(file_path, 'wb') as f:
            f.write(file.getbuffer())
        
        url = st.text_input("Enter the upload URL")
        
        if st.button("Upload File"):
            response = upload_file_to_filebin(file_path, "https://filebin.net/{}/{}".format(url,file.name))
            if response is not None:
                st.write(f"Upload Status Code: {response.status_code}")
                st.write("Response Body:", response.text)
            else:
                st.write("Upload failed. Check the logs for details.")
            
            # Clean up the temporary file
            import os
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to remove temporary file: {e}")

main()


