"""Util file containing random useful functions used throughout"""
import os

def mkdir_p(directory:str):
    '''make directory if does not exist'''
    if not os.path.exists(directory):
        os.mkdir(directory)
