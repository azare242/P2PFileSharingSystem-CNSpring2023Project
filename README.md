# P2PFileSharingSystem

This is a Peer-to-Peer (P2P) file sharing system built in Python. It uses STUN server with Redis caching for NAT traversal, TCP connection for text file transfer, and UDP connection for image file transfer. The project also includes image processing capabilities using the Pillow library.

## Prerequisites

- Python 3.x
- Redis server
- Pillow library (`pip install Pillow`)

## Installation

1. Clone the repository
2. Install required packages: `pip install -r requirements.txt`
3. Start Redis server: `redis-server`
4. Run the STUN server: `python STUNServer/Main.py`
5. Start the P2P file sharing system: `python App/Main.py`

## Credits

This project was created by Alireza Zare Z. If you have any questions or feedback, feel free to contact me.
