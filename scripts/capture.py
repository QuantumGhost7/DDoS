from scapy.all import *
import logging
from datetime import datetime
from config import *

logging.basicConfig(
    filename='logs/capture.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class PacketCapture:
    def __init__(self):
        self.normal_packets = []
        self.attack_packets = []
        self.capture_filter = f"udp and (port {NORMAL_TRAFFIC_PORT} or port {ATTACK_TRAFFIC_PORT})"
    
    def packet_callback(self, packet):
        if UDP in packet and Raw in packet:
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            
            # Check if packet contains our signature
            if PACKET_SIGNATURE in payload:
                if "NORMAL" in payload:
                    self.normal_packets.append(packet)
                    print(f"\rNormal packets captured: {len(self.normal_packets)}", end='')
                elif "ATTACK" in payload:
                    self.attack_packets.append(packet)
                    print(f"\rAttack packets captured: {len(self.attack_packets)}", end='')
    
    def start_capture(self, duration):
        logging.info(f"Starting packet capture for {duration} seconds")
        print(f"Starting capture for {duration} seconds...")
        
        # Start capturing
        sniff(filter=self.capture_filter, 
              prn=self.packet_callback, 
              timeout=duration)
        
        # Save captured packets
        if self.normal_packets:
            wrpcap("data/captured_packets/normal_traffic.pcap", self.normal_packets)
            logging.info(f"Saved {len(self.normal_packets)} normal packets")
        
        if self.attack_packets:
            wrpcap("data/captured_packets/attack_traffic.pcap", self.attack_packets)
            logging.info(f"Saved {len(self.attack_packets)} attack packets")
        
        print("\nCapture completed!")

if __name__ == "__main__":
    capture = PacketCapture()
    duration = int(input("Enter capture duration in seconds: "))
    capture.start_capture(duration)