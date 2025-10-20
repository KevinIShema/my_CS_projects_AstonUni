# decrpting a ceasar cipher 

def mod26_decrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c = ord(char) - base
            p = (c - key) % 26
            result += chr(p + base)
        else:
            result += char
    return result

cipher_text = "TLXNZZW"
key = 11
decrypted = mod26_decrypt(cipher_text, key)
print("Decrypted word:", decrypted)

cipher_text2 = "QODVYCD"
key2 = 10
decrypted2 = mod26_decrypt(cipher_text2, key2)
print("Decrypted word 2:", decrypted2)
