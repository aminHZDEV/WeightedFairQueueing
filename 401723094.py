import os
import sys

if not sys.platform.startswith("win"):
    os.system("python3 destination/destination.py &")
    os.system("python3 router/router.py &")
    os.system("python3 client/client.py")
else:
    os.system("python destination\\destination.py")
    os.system("python router\\router.py")
    os.system("python client\\client.py")
