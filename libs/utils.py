import os
import sys

if sys.platform.count("win"):
    def clear():
        os.system("cls")
else:
    def clear():
        os.system("clear")