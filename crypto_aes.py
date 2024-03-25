#from tkinter.ttk import _Padding
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import hashlib
#simple_key = get_random_bytes(256)
#print(simple_key)

salt = b'\xdd\xd5\x9f\x93\x91\xff\xee~\xab\xaaM\x02\x9b\xa4\xdb\xe7\xef\xef\x92\xd2\xc6\xe6\xc8V\xdc(\xf7\xf4\n\x9b\x0f\xd1e\xb0n\xd4\x13\xbf$\x0ff*\x06\xb5\xd2\xda\xab\xa0\x9e\xe4g\xe2\x97\x82\xd1\xd0\xe4\xf5=S\xaeK\xa3&\x14\x06\x15\x7f\xc9\xc9\xaa\x9f}\x12s\x19e\xe6)\xf7\xac;\x81t\xe8\xac|\'\xc1\xb7t?\xc3f\x18\\\xb7"_T\x8d!\xf1i\x83\xf4C\xe9\xd7Xo\xbf\xbe=J\x9b\xca\xb8\x19a\xc2\x9b\x89\xc4\x16GG\xdf\xb8\xc4\x94$\x14`bn\xbbT\xaa\xee\xa8\xf1s\xfc\x92N`\x16\xc47\x8a\xf7CZ\x0f\xa0\xad\x86\xb3\xd0\xe1\xa4\x91\x16r4\xb4\xec4UJKq\xcf\xfc\xd2y\x02\x83H\x8e\xef\xb72[\x9a\t\xbaR\x81i\xec[\xe5\xf6\xcf=m\x1c\xf2\xf9y\xd8\x0b\xbb\x8b\n\xc3r2e\xbaT\x133F\x19\xcb\xc0O\xdf\xdf5\x01MK\xa2\xc0\x1f\x03\x96\x86\xaf=\r\xc1(\xc1\xf8}\x006!Q0"0u\x98\xd15\x88\xce\x19\xb16'
password = "000100111101011011011110011100101101100101011011001111010101101011110001101101010000010110001010001111010001001001001100110"

key = PBKDF2(password, salt, dkLen=32)
mensaje = b"Hola mundo Cuantico!"

def generate_iv():
    iv = get_random_bytes(AES.block_size)  # Genera un IV aleatorio
# Comprueba que el IV no es todo ceros
    if iv == b'\x00' * AES.block_size:
        return generate_iv()
    else:
        return iv

# --- Cifrado ---
iv = generate_iv()  # Llama a la función para generar el IV    
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphered_data = cipher.encrypt(pad(mensaje, AES.block_size))
#print(iv + ciphered_data)

with open(r'D:\cifrado.bin', 'wb') as f:
    f.write(cipher.iv)
    f.write(ciphered_data)

# --- Descifrado ---
received_data = iv + ciphered_data  # Simula la recepción del mensaje cifrado
iv = received_data[:AES.block_size]  # Extrae el IV del texto cifrado
ciphertext = received_data[AES.block_size:]  # Separa el texto cifrado real del IV

key = PBKDF2(password, salt, dkLen=32)
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

#cipher = AES.new(key, AES.MODE_CBC)
#original = unpad(cipher.decrypt)

####################

def decrypt(ciphertext, key, mode):
    cipher = AES.new(key, mode)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)

# Ruta del archivo cifrado
cifrado_file_path = r'd:\cifrado.bin'

# Cargar el contenido cifrado del archivo
with open(cifrado_file_path, 'rb') as file:
    ciphertext = file.read()

# Ruta del diccionario
diccionario_file_path = r'D:\rockyou.txt'

# Leer contraseñas desde el diccionario
with open(diccionario_file_path, 'r', errors='ignore') as file:
    passwords = file.read().splitlines()

# Auditoría de fuerza bruta
print('Realizando auditoría de fuerza bruta en', cifrado_file_path)
print('Probando contraseñas del diccionario', diccionario_file_path)

# Fuerza bruta
start_time = time.time()

for idx, password in enumerate(passwords):
    try:
        # Generar la clave desde la contraseña utilizando PBKDF2
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b'salt', 100000)
        
        # Descifrar utilizando AES en modo CBC
        plaintext = decrypt(ciphertext, key, AES.MODE_CBC)
        
        # Intentar quitar el relleno y mostrar el texto plano
        p = unpad(plaintext, AES.block_size)
        
        print('Contraseña probada:', password)
        print('Texto plano:', p)
        break  # Detener después de encontrar la contraseña correcta (solo para propósitos de demostración)
    except Exception as e:
        # Ignorar excepciones, ya que intentaremos múltiples contraseñas
        pass
    
    # Imprimir tiempo estimado cada 10 intentos (ajustable según sea necesario)
    if idx % 10 == 0 and idx > 0:
        current_time = time.time() - start_time
        estimated_total_time = (current_time / idx) * len(passwords)
        print(f'Tiempo transcurrido: {current_time:.2f} segundos | Tiempo estimado restante: {estimated_total_time - current_time:.2f} segundos')

# Calcular y mostrar
end_time = time.time()
elapsed_time = end_time - start_time
print('Tiempo transcurrido:', elapsed_time, 'segundos')