from ftplib import FTP
import os

# Connect to the FTP server
ftp = FTP('ftp.ebi.ac.uk')
ftp.login()  # anonymous login

# Change to the directory containing the images
ftp.cwd('/pub/databases/IDR/idr0160-lippincott-pyroptosis/Images/')

# List all files in the directory
files = ftp.nlst()

# Create local directory if needed
os.makedirs("downloaded_tiffs", exist_ok=True)

# Download all .tiff files
for fname in files:
    if fname.lower().endswith('.tiff'):
        print(f"Downloading {fname}...")
        with open(os.path.join("downloaded_tiffs", fname), 'wb') as f:
            ftp.retrbinary(f'RETR {fname}', f.write)

ftp.quit()
print("All .tiff downloads complete.")
