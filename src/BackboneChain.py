"""
Created on 3 lut 2019

@author: Basia
"""

from KatDwuscienny import policz_kat_dwuscienny as dehydralAngle


def calcFiPsi(pos_list, ret_unit="deg"):
    a, b, c = pos_list[:3]
    start = 3
    count = len(pos_list) - start
    ret_list = []
    for idx in range(start, count, 2):
        fi_psi = {}
        d, e = pos_list[idx], pos_list[idx + 1]
        fi_psi["fi"] = dehydralAngle(a, b, c, d)[ret_unit]
        fi_psi["psi"] = dehydralAngle(b, c, d, e)[ret_unit]
        a = c
        b = d
        c = e
        ret_list += [fi_psi]
    return ret_list


class BackboneChain:
    def __init__(self, chainID=" "):
        self.ChainID = chainID
        self.Seqences = {}
        self.FiPsi = []

    def add_atom(self, new_atom):
        def read_position(pos_dict):
            return float(pos_dict["x"]), float(pos_dict["y"]), float(pos_dict["z"])

        if new_atom["resSeq"] not in self.Seqences:
            self.Seqences[new_atom["resSeq"]] = []
        SeqAtom = {
            "name": new_atom["name"],
            "residue": new_atom["resName"],
            "position": tuple(read_position(new_atom)),
        }
        self.Seqences[new_atom["resSeq"]] += [SeqAtom]

    def get_fi_psi(self):
        if not self.FiPsi:
            # tu wstaw weryfikacje poprawnosci
            positions = []
            for seqAtoms in self.Seqences.values():
                for atm in seqAtoms:
                    positions += [atm["position"]]
            self.FiPsi = calcFiPsi(positions)
        return self.FiPsi

    def quick_info(self, sortBy=None):
        print("Chain {0}".format(self.ChainID))

        seqKeys = self.Seqences.keys()
        if sortBy == "SEQ":
            seqKeys = sorted(seqKeys)

        for seqID in seqKeys:
            print("  Sequence{0}".format(seqID))
            for atm in self.Seqences[seqID]:
                print("    {residue}:{name}={position}".format(**atm))


class BackboneStructure:
    PeptideAtomNames = set((" N  ", " CA ", " C  "))

    def __init__(self):
        self.bbChains = []

    def add_bbChain(self, chainID, chainAtoms):
        bbc = BackboneChain(chainID)
        for atm in chainAtoms:
            if atm["name"] in BackboneStructure.PeptideAtomNames:
                bbc.add_atom(atm)
        self.bbChains.append(bbc)

    def build_from_atoms(self, chains):
        for chainID, chainAtoms in chains:
            self.add_bbChain(chainID, chainAtoms)

    def calculate_fi_psi(self):
        ret_list = []
        for bbc in self.bbChains:
            ret_list += bbc.get_fi_psi()
        return ret_list

    def quick_info(self, sortBy=None):
        if sortBy == "CHAIN":
            for bbc in sorted(self.bbChains):
                bbc.quick_info()
        else:
            for bbc in self.bbChains:
                bbc.quick_info(sortBy)


def test4(param1):
    from FilePDB import FilePDB

    file_pdb = FilePDB(param1)
    file_pdb.loadData()
    bbStruct = BackboneStructure()
    bbStruct.build_from_atoms(file_pdb.get_backbone())
    bbStruct.quick_info()

if __name__ == "__main__":
    test4("6e8z")

