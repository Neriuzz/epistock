"""
Script that runs all the tests we have written.

Author: Nerius Ilmonas
Date: 24/03/2021
"""

from testing import test_sax, test_manepi
import sys


if __name__ == "__main__":
    if "-sax" in sys.argv:
        print("[!] Testing SAX...")
        test_sax()
        print("[!] SAX testing complete")
        sys.exit(0)
    elif "-manepi" in sys.argv:
        print("[!] Testing MANEPI....")
        test_manepi()
        print("[!] MANEPI testing complete")
        sys.exit(0)
    else:
        print("Please specify which algorithm to test")
        sys.exit(0)
