import streamlit as st
import requests
import os
import time
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="FileShare Hub",
    page_icon="📁",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #2E7D32;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        margin-bottom: 1rem;
    }
    .error-message {
        padding: 1rem;
        background-color: #FFEBEE;
        border-left: 5px solid #F44336;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        margin-bottom: 1rem;
    }
    .download-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        transition: background-color 0.3s;
    }
    .download-button:hover {
        background-color: #2E7D32;
    }
    .file-type-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def create_download_button(url, filename, button_text="Download"):
    html = f"""
    <a href="{url}" download="{filename}" class="download-button">
        {button_text} {filename}
    </a>
    """
    return html

def upload_file_to_filebin(file_path, url, progress_bar=None):
    try:
        with open(file_path, 'rb') as file:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/octet-stream'
            }
            
            # Get file size for progress reporting
            file_size = os.path.getsize(file_path)
            
            # Upload with progress simulation
            if progress_bar:
                for percent in range(0, 101, 10):
                    time.sleep(0.1)  # Simulate network delay
                    progress_bar.progress(percent/100)
            
            response = requests.post(url, headers=headers, data=file)
            
            if progress_bar:
                progress_bar.progress(1.0)
            
            return response
    except Exception as e:
        if progress_bar:
            progress_bar.empty()
        return None

def get_file_icon(file_type):
    icons = {
        'txt': "📄",
        'pdf': "📑",
        'jpg': "🖼️",
        'jpeg': "🖼️",
        'png': "🖼️",
        'zip': "📦",
        'mp3': "🎵",
        'mp4': "🎬",
        'doc': "📝",
        'docx': "📝",
        'xls': "📊",
        'xlsx': "📊",
        'ppt': "📊",
        'pptx': "📊",
    }
    return icons.get(file_type.lower(), "📎")

def main():
    # App header
    st.markdown('<h1 class="main-header">FileShare Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;">A simple way to share files securely</p>', unsafe_allow_html=True)
    
    # Create tabs for different functions
    tab1, tab2 = st.tabs(["📤 Upload Files", "📥 Download Files"])
    
    with tab1:
        st.markdown('<h2 class="subheader">Upload Files</h2>', unsafe_allow_html=True)
        
        # File uploader with expanded file types
        files = st.file_uploader(
            "Choose one or more files", 
            type=['txt', 'pdf', 'jpg', 'jpeg', 'png', 'mp3', 'mp4', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip'],
            accept_multiple_files=True
        )
        
        # Generate a default folder suggestion based on date
        default_folder = f"share_{datetime.now().strftime('%Y%m%d_%H%M')}"
        url = st.text_input("Enter folder name for uploads:", value=default_folder)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            upload_button = st.button("Upload Files", use_container_width=True)
        
        with col2:
            folder_link = f"https://filebin.net/{url}"
            if url:
                st.markdown(f"Your folder will be: [**{folder_link}**]({folder_link})", unsafe_allow_html=True)
        
        # How to Use section
        with st.expander("ℹ️ How to Use Upload Function", expanded=False):
            st.markdown("""
            **To upload files:**
            1. Click '**Browse files**' to select one or more files from your device
            2. The folder name is automatically generated, but you can customize it
            3. Click '**Upload Files**' button
            4. Share the folder link with recipients

            **Important Notes:**
            - Files will be stored temporarily on filebin.net
            - Default expiration is 6 days after the last download
            - Keep your folder name for later use
            """)
        
        if upload_button and files:
            total_files = len(files)
            success_count = 0
            
            st.markdown('<div class="info-box">Starting upload process...</div>', unsafe_allow_html=True)
            
            for i, file in enumerate(files):
                file_path = f"temp_file_{file.name}"
                with open(file_path, 'wb') as f:
                    f.write(file.getbuffer())
                
                st.markdown(f"**{i+1}/{total_files}**: Uploading {get_file_icon(file.name.split('.')[-1])} {file.name}")
                progress_bar = st.progress(0)
                
                response = upload_file_to_filebin(
                    file_path, 
                    f"https://filebin.net/{url}/{file.name}",
                    progress_bar
                )
                
                if response is not None and response.status_code == 201:
                    success_count += 1
                    st.markdown(f'<div class="success-message">✅ File {file.name} uploaded successfully!</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-message">❌ Failed to upload {file.name}. Please try again.</div>', unsafe_allow_html=True)
                
                # Clean up the temporary file
                try:
                    os.remove(file_path)
                except Exception as e:
                    pass
            
            if success_count > 0:
                st.markdown(f"""
                <div class="success-message">
                <h3>Upload Complete!</h3>
                <p>Successfully uploaded {success_count}/{total_files} files.</p>
                <p>Share this link with recipients: <a href="{folder_link}" target="_blank">{folder_link}</a></p>
                </div>
                """, unsafe_allow_html=True)
        
        elif upload_button and not files:
            st.markdown('<div class="error-message">Please select at least one file to upload.</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 class="subheader">Download Files</h2>', unsafe_allow_html=True)
        
        folder_name = st.text_input("Enter the folder name to download from:")
        
        # How to Use section
        with st.expander("ℹ️ How to Use Download Function", expanded=False):
            st.markdown("""
            **To download files:**
            1. Enter the folder name you received (e.g., "share_20250323_1030")
            2. Click '**Search Folder**' button
            3. Click the download button to get all files as a ZIP archive

            **Note:** Folder names are case-sensitive. Make sure to enter the exact name.
            """)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            search_file = st.button("Search Folder", use_container_width=True)
        
        if search_file and folder_name:
            download_url = f"https://filebin.net/archive/{folder_name}/zip"
            
            try:
                # Check if folder exists by making a head request
                head_response = requests.head(f"https://filebin.net/{folder_name}")
                
                if head_response.status_code == 200:
                    st.markdown(f"""
                    <div class="success-message">
                    <h3>Folder Found! 🎉</h3>
                    <p>You can download all files as a ZIP archive:</p>
                    {create_download_button(download_url, f"{folder_name}.zip", "📦 Download")}
                    <p style="margin-top: 10px;">Or visit the folder directly:</p>
                    <a href="https://filebin.net/{folder_name}" target="_blank">View files online</a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-message">❌ Folder "{folder_name}" not found. Please check the name and try again.</div>', unsafe_allow_html=True)
            except:
                st.markdown('<div class="error-message">❌ Error occurred while checking the folder. Please try again.</div>', unsafe_allow_html=True)
        
        elif search_file and not folder_name:
            st.markdown('<div class="error-message">Please enter a folder name to search.</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <p style="text-align: center; color: #666; font-size: 0.8rem;">
        FileShare Hub © 2025 | Files hosted on <a href="https://filebin.net">filebin.net</a> | 
        <a href="https://github.com/innovsm/push_pull">View on GitHub</a>
    </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
