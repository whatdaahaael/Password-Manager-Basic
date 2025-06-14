import hashlib

# Character set
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['`', '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '[', ']', '{', '}', '|', ':', ';', '"', "'", '<', '>', '?', ',', '.', '/']
values = letters + numbers + symbols  # All characters

class CryptIt:

    def getHash(self, str):
        hash_str = hashlib.sha256(str.encode())
        return hash_str.hexdigest()

    def checkHash(self, str, hash_str):
        new_hash = self.getHash(str)
        return new_hash == hash_str

    def getKey(self, str):
        key = 0
        for c in str:
            key += ord(c)
        return key

    def getEncrypt(self, str, key):
        encrypted_password = ""
        for c in str:
            index = values.index(c) + key  # Shift by the key value
            encrypted_password += values[index % len(values)]  # Ensure it wraps around within bounds
        return encrypted_password

    def getDecrypt(self, encrypted_str, key):
        decrypted_password = ""
        for c in encrypted_str:
            value_index = values.index(c)  # Get the index of the encrypted character
            original_index = (value_index - key) % len(values)  # Reverse the shift using the key
            decrypted_password += values[original_index]  # Retrieve the original character
        return decrypted_password


