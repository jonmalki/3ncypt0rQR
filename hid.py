import os
import sys
import pyotp
import qrcode
from PIL import Image

# Define the folder name
dir_name = "F0ld3r"

# Create a new directory in the current working directory if it doesn't exist
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# Generate a secret key
secret_key = pyotp.random_base32()

# Generate a QR code for the secret key and save it as an image file
qr_file_name = 'qrcode.png'
totp_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name='My App', issuer_name='Authenticator App')
qr = qrcode.QRCode(box_size=5)
qr.add_data(totp_uri)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(qr_file_name)

# Display the secret key and the QR code to the user
print('Please scan the QR code below or manually add the secret key to your OTP app:')
print(f'Secret key: {secret_key}')
Image.open(qr_file_name).show()

# Check for command-line argument to unhide or hide the folder
if len(sys.argv) > 1:
    if sys.argv[1] == "unhide":
        if pyotp.TOTP(secret_key).verify(input('Enter the OTP code: ')):
            os.system(f"chflags nohidden '{dir_name}'")
            print("The folder is now visible.")
        else:
            print("Invalid OTP code. Access denied.")
    elif sys.argv[1] == "hide":
        if pyotp.TOTP(secret_key).verify(input('Enter the OTP code: ')):
            os.system(f"chflags hidden '{dir_name}'")
            print("The folder is now hidden.")
        else:
            print("Invalid OTP code. Access denied.")
    else:
        print("Invalid command-line argument. Please use 'unhide' or 'hide'.")
else:
    os.system(f"chflags hidden '{dir_name}'")
    print("The folder is currently hidden. Run the script with 'unhide' or 'hide' argument to change its visibility.")
