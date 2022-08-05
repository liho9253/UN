import os
import sys

restart = input("\nDo you want to restart the program? [y/n] > ")

if restart == "y":
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
else:
    print("\nThe program will be closed...")
    sys.exit(0)