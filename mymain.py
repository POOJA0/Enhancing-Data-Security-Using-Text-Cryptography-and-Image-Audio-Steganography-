from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from LSBSteg import LSBSteg
import cv2
import cv2
from wavsteg import hide_data
from wavsteg import recover_data
import os





#key = get_random_bytes(16)
keys='BALABALABALABALA'
output_file='enresult'
key=bytes(keys, 'utf-8')
cipher = AES.new(key, AES.MODE_CBC)


text_file = open("testfile.txt", "r")
data = text_file.read()
text_file.close()

print('original data');
print(data)

bdata=bytes(data,'utf-8')


ciphered_data = cipher.encrypt(pad(bdata, AES.block_size)) 


file_out = open(output_file, "wb") # Open file to write bytes
file_out.write(cipher.iv) # Write the iv to the output file (will be required for decryption)
file_out.write(ciphered_data) # Write the varying length ciphertext to the file (this is the encrypted data)
file_out.close()

sound_path='sample.wav'
file_path='enresult'
output_path='stegnoaudio.wav'
num_lsb=2

size = os.path.getsize('enresult') 
print('Size of file is', size, 'bytes')


hide_data(sound_path, file_path, output_path, num_lsb)

recover_data(output_path,'refromaudio',2,size)



#steg = LSBSteg(cv2.imread("baboon.png"))
#data = open("enresult", "rb").read()
#new_img = steg.encode_binary(data)
#cv2.imwrite("new_image.png", new_img)

#decoding
#steg = LSBSteg(cv2.imread("new_image.png"))
#binary = steg.decode_binary()
#file_out = open("recovered.bin", "wb")
#file_out.write(binary);
#file_out.close()


#file_in = open("recovered.bin", 'rb') # Open the file to read bytes
#iv = file_in.read(16) # Read the iv out - this is 16 bytes long
#ciphered_data = file_in.read() # Read the rest of the data
#file_in.close()

#cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
#original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result

#txtdata=original_data.decode('utf-8')

#print('After stegno and decryption')
#print(txtdata)


file_in = open("refromaudio", 'rb') # Open the file to read bytes
iv = file_in.read(16) # Read the iv out - this is 16 bytes long
ciphered_data = file_in.read() # Read the rest of the data
file_in.close()

cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result

txtdata=original_data.decode('utf-8')

print('After stegno and decryption')
print(txtdata)




