#  encryption using ceasar cipher

def mod26_encrypt(text, key):
	result = ""
	for char in text:
		if char.isalpha():
			base = ord('A') if char.isupper() else ord('a')
			p = ord(char) - base
			c = (p + key) % 26
			result += chr(c + base)
		else:
			result += char
	return result

word = "get a coffee"
key = 7
encrypted = mod26_encrypt(word, key)
print("Encrypted word:", encrypted)