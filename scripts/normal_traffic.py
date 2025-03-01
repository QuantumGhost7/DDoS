from scapy.all import *
import random
import time
import logging
from datetime import datetime
from config import *

logging.basicConfig(
    filename='logs/normal_traffic.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class NormalTrafficGenerator:
    def __init__(self):
        self.running = True
        self.signature = PACKET_SIGNATURE + "NORMAL_"
    
    def generate_packet(self, size=None):
        if size is None:
            size = random.randint(64, 512)
        
        # Create packet with our signature and sequence number
        seq_num = random.randint(1, 1000)
        payload = f"{self.signature}{seq_num}".encode() + b"X" * size
        
        pkt = IP(dst=SERVER_IP)/\
              UDP(sport=NORMAL_TRAFFIC_PORT, dport=NORMAL_TRAFFIC_PORT)/\
              Raw(load=payload)
        
        return pkt
    
    def start_generation(self, duration):
        end_time = time.time() + duration
        packets_sent = 0
        
        logging.info(f"Starting normal traffic generation for {duration} seconds")
        print(f"Generating normal traffic to {SERVER_IP}")
        
        while time.time() < end_time:
            try:
                pkt = self.generate_packet()
                send(pkt, verbose=0)
                packets_sent += 1
                
                # Random delay between packets
                time.sleep(random.uniform(0.1, 0.5))
                
            except Exception as e:
                logging.error(f"Error: {str(e)}")
        
        logging.info(f"Traffic generation completed. Sent {packets_sent} packets")
        print(f"Sent {packets_sent} packets")

if __name__ == "__main__":
    generator = NormalTrafficGenerator()
    duration = int(input("Enter duration in seconds: "))
    generator.start_generation(duration)