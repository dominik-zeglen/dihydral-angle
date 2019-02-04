'''
Created on 2 lut 2019

@author: Basia
'''

from src.BackboneChain import BackboneStructure, BackboneChain
from src.FilePDB import FilePDB


def main():
    file_pdb = FilePDB('data/1hy9')
    file_pdb.loadData()
    file_pdb.quick_info()

if __name__ == '__main__':
    main()