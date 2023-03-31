import paramiko
import urllib.request
from io import BytesIO
from tqdm import tqdm

url = #"Enter the url you want to upload from"
sftp_host = #"host address"
sftp_user = #"username"
sftp_pass = #"Password"
sftp_dir = "/"

print("Uploading file from URL to SFTP server...")
# Get the file name from the URL
file_name = url.split("/")[-1]

# Open a connection to the SFTP server
transport = paramiko.Transport((sftp_host, 22))
transport.connect(username=sftp_user, password=sftp_pass)
sftp = paramiko.SFTPClient.from_transport(transport)

# Get the size of the file in bytes
response = urllib.request.urlopen(url)
file_size = int(response.getheader("Content-Length"))

# Create a progress bar
progress_bar = tqdm(total=file_size, unit="B", unit_scale=True)

# Stream the file from the URL to the SFTP server
with urllib.request.urlopen(url) as file_contents:
    with sftp.file(sftp_dir + file_name, "wb") as sftp_file:
        while True:
            data = file_contents.read(131072)
            if not data:
                break
            sftp_file.write(data)
            progress_bar.update(len(data))  

# Close the SFTP connection and progress bar
sftp.close()
transport.close()
progress_bar.close()

print("File upload complete.")
