"""
Script that runs all the tests we have written.

Author: Nerius Ilmonas
Date: 24/03/2021
"""

from testing import test_sax, test_manepi
from sys import argv


if __name__ == "__main__":
    if "-sax" in argv:
        print("[!] Testing SAX...")
        test_sax()
        print("[!] SAX testing complete")
    elif "-manepi" in argv:
        print("[!] Testing MANEPI....")
        test_manepi()
        print("[!] MANEPI testing complete")
    else:
        print("Please specify which algorithm to test")
