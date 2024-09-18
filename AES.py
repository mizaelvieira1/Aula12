import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Diretório raiz
root_dir = r'C:\Users\mizae\OneDrive\FIAP\Python\2 Semestre\Arquivos\desafio_python_AES'

# Função para gerar uma chave a partir da senha
def generate_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Função para criptografar arquivos
def encrypt_file(password, filepath, backup_folder):
    salt = os.urandom(16)
    key = generate_key(password, salt)

    with open(filepath, 'rb') as file:
        data = file.read()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(data) + encryptor.finalize()

    # Criar backup folder se não existir
    os.makedirs(backup_folder, exist_ok=True)

    # Salvar arquivo criptografado com extensão .enc
    encrypted_filepath = os.path.join(backup_folder, os.path.basename(filepath) + '.enc')
    with open(encrypted_filepath, 'wb') as enc_file:
        enc_file.write(salt + iv + encrypted_data)

    print(f'Arquivo {filepath} criptografado com sucesso.')

# Função para descriptografar arquivos
def decrypt_file(password, filepath, output_folder):
    with open(filepath, 'rb') as enc_file:
        salt = enc_file.read(16)
        iv = enc_file.read(16)
        encrypted_data = enc_file.read()

    key = generate_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Salvar arquivo descriptografado na pasta de saída
    decrypted_filepath = os.path.join(output_folder, os.path.basename(filepath).replace('.enc', ''))
    os.makedirs(output_folder, exist_ok=True)
    with open(decrypted_filepath, 'wb') as dec_file:
        dec_file.write(decrypted_data)

    print(f'Arquivo {filepath} descriptografado com sucesso.')

# Exemplo de uso:
password = input("Digite a senha: ")
folder = os.path.join(root_dir, 'original')  # Substitua pelo caminho da pasta original
backup_folder = os.path.join(root_dir, 'backup')

# Criptografar todos os arquivos na pasta 'original'
for filename in os.listdir(folder):
    filepath = os.path.join(folder, filename)
    encrypt_file(password, filepath, backup_folder)

# Descriptografar os arquivos na pasta 'backup'
output_folder = os.path.join(root_dir, 'descriptografados')
for enc_filename in os.listdir(backup_folder):
    enc_filepath = os.path.join(backup_folder, enc_filename)
    decrypt_file(password, enc_filepath, output_folder)