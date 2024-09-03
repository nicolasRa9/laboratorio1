from scapy.all import *
import sys

def cifrado_cesar(texto, desplazamiento):
    texto_descifrado = []
    for char in texto:
        if char.isalpha():
            base_desplazamiento = ord('a') if char.islower() else ord('A')
            texto_descifrado.append(chr((ord(char) - base_desplazamiento - desplazamiento) % 26 + base_desplazamiento))
        else:
            texto_descifrado.append(char)
    return ''.join(texto_descifrado)

def es_texto_probable(texto):
    palabras_comunes = ["la", "de", "que", "y", "el", "en", "los", "del", "se", "las"]
    contador = 0
    for palabra in palabras_comunes:
        if palabra in texto:
            contador += 1
    return contador

def descifrar_cesar(texto):
    mejor_puntuacion = -1
    mejor_texto = ""
    for i in range(1, 26):
        texto_descifrado = cifrado_cesar(texto, i)
        puntuacion = es_texto_probable(texto_descifrado)
        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_texto = texto_descifrado
        print(f"Desplazamiento {i}: {texto_descifrado}")

    # Imprimir la mejor opción en verde
    print("\033[92m" + f"Texto más probable: {mejor_texto}" + "\033[0m")

def extraer_datos_pcapng(archivo):
    # Leer el archivo pcapng
    paquetes = rdpcap(archivo)
    mensaje = ""
    
    for paquete in paquetes:
        if ICMP in paquete and Raw in paquete:
            # Extraer la carga útil de los paquetes ICMP
            mensaje += paquete[Raw].load.decode(errors='ignore')
    
    return mensaje

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 readv2.py <archivo.pcapng>")
        sys.exit(1)

    archivo = sys.argv[1]
    
    # Extraer el mensaje del archivo pcapng
    mensaje = extraer_datos_pcapng(archivo)
    print(f"Mensaje extraído: {mensaje}")

    # Proceder a descifrar el mensaje
    descifrar_cesar(mensaje)
