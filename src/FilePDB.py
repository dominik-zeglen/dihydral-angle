"""
Created on 3 lut 2019

@author: Basia
"""

from fileinput import FileInput
from os import getcwd, path

from .colors import bcolors


class FilePDB:
    def __init__(self, pdb_id):
        self.ID = pdb_id
        self.fileName = "data/" + pdb_id + ".pdb"
        self.fileLocation = getcwd()
        self.filePath = path.join(self.fileLocation, self.fileName)
        self.Atoms = []
        self.Chains = []
        self.SeqRes = {}

        try:
            lines = FileInput(self.fileName)
            for line in lines:
                self.process_line(line)
            lines.close()
        except (IOError, OSError) as err:
            print(
                bcolors.FAIL
                + "Nie mozna odczytac pliku {0}!".format(self.fileName)
                + bcolors.ENDC
            )
            print(err)

    def process_line(self, record_line):
        record_type = record_line[0:6]
        if record_type == "ATOM  ":
            atom = {
                "name": record_line[12:16],
                "resName": record_line[17:20],
                "chainID": record_line[21:22],
                "resSeq": record_line[22:26],
                "x": record_line[30:38],
                "y": record_line[38:46],
                "z": record_line[46:54],
            }
            self.add_atom(atom)
        elif record_type == "SEQRES":
            serNum = record_line[7:10]
            chainID = record_line[11:12]
            if serNum == "  1":
                self.new_seqres(chainID)

            self.append_seqres(chainID, record_line[19:70])

    def add_atom(self, new_atom):
        self.Atoms.append(new_atom)

    def new_seqres(self, chainID):
        self.Chains.append(chainID)
        self.SeqRes[chainID] = []

    def append_seqres(self, chainID, resNameFields):
        resNames = resNameFields.split()
        for resName in resNames:
            self.SeqRes[chainID].append(resName)

    def get_backbone(self):
        backbone = []
        for chainID in self.Chains:
            atmList = []
            for atm in self.Atoms:
                if atm["chainID"] == chainID:
                    atmList.append(atm)
            backbone.append((chainID, atmList))
        return backbone
