import logging
import time
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.diagnostics.log_transmitter import LogTransmitterHandler

def test_transmitter():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("TestLogger")
    
    # Add the UDP transmitter
    handler = LogTransmitterHandler(port=54322)
    logger.addHandler(handler)
    
    print("Sending test logs...")
    logger.info("Test message 1: Application starting")
    logger.warning("Test message 2: Something might be wrong")
    logger.error("Test message 3: Simulation of an error")
    
    time.sleep(1)
    handler.close()
    print("Finished sending test logs.")

if __name__ == "__main__":
    test_transmitter()
