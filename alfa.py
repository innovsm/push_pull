import requests

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

# Example usage
file_path = "temp_.txt"
url = "https://filebin.net/hello32532/ada"
response = upload_file_to_filebin(file_path, url)
