import sys

def cifrado_cesar(texto, desplazamiento):
    texto_cifrado = []
    for caracter in texto:
        if caracter.isalpha():
            base_desplazamiento = ord('a') if caracter.islower() else ord('A')
            texto_cifrado.append(chr((ord(caracter) - base_desplazamiento + desplazamiento) % 26 + base_desplazamiento))
        else:
            texto_cifrado.append(caracter)
    return ''.join(texto_cifrado)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py <texto> <desplazamiento>")
        sys.exit(1)
    
    texto = sys.argv[1]
    desplazamiento = int(sys.argv[2])
    texto_cifrado = cifrado_cesar(texto, desplazamiento)
    print(texto_cifrado)
