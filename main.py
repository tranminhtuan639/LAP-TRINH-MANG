"""
Cách dùng:
    python main.py           
    python main.py --server  
    python main.py --cli    
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_server():
    from server.server import Chatserver
    print("=" * 40)
    print("  TCP Chat Server")
    print("=" * 40)
    server = Chatserver(host="0.0.0.0", port=9999)
    server.start()


def run_gui():
    from gui.chat_gui import run_client
    run_client()


def run_cli():
    from client.client import main
    main()
        
if __name__ == "__main__":
    args = sys.argv[1:]
    if "--server" in args:
        run_server()
    elif "--cli" in args:
        run_cli()
    else:
        run_gui()   