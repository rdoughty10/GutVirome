import os
import glob
import subprocess

dir = 'P1*'

for folder in glob.glob(dir):
    print(f"sed -i 's/\s.*$//' {folder}")
    subprocess.call(["sed",
                    "-i",
                    's/\s.*$//',
                    folder])