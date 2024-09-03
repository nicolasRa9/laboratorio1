from scapy.all import *
import sys
import random
from datetime import datetime

def obtener_timestamp():
    # Obtener el tiempo actual en milisegundos desde la medianoche UTC
    ahora = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    ms_since_midnight = (ahora - epoch).total_seconds() * 1000
    return int(ms_since_midnight) & 0xFFFFFFFF  # Asegurar que se ajuste a 32 bits

def enviar_ping_stealth_con_timestamp(destino, mensaje):
    id_paquete = random.randint(0, 65535)
    
    for i, char in enumerate(mensaje):
        seq_num = i + 1

        # Crear el paquete ICMP con tipo 13 (Timestamp Request)
        timestamp_origen = obtener_timestamp()
        # Incluir el mensaje dividido en el campo de datos del paquete
        carga_util = char.encode()
        paquete = IP(dst=destino)/ICMP(type=8, id=id_paquete, seq=seq_num, ts_ori=timestamp_origen)/Raw(load=carga_util)

        # Enviar el paquete y esperar la respuesta
        respuesta = sr1(paquete, timeout=1, verbose=0)

        if respuesta:
            timestamp_recibido = respuesta[ICMP].ts_rx
            timestamp_respuesta = respuesta[ICMP].ts_tx

            print(f"Enviado: {char} | ID: 0x{id_paquete:04x}, Seq: {seq_num}, "
                  f"Timestamp de origen: {timestamp_origen}, "
                  f"Timestamp de recepción: {timestamp_recibido}, "
                  f"Timestamp de transmisión: {timestamp_respuesta}")
        else:
            print(f"No se recibió respuesta para el paquete con ID 0x{id_paquete:04x} y Seq: {seq_num}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 pingv4.py <destino> <mensaje>")
        sys.exit(1)
    
    destino = sys.argv[1]
    mensaje = sys.argv[2]
    enviar_ping_stealth_con_timestamp(destino, mensaje)
