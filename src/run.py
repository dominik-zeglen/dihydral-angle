from FilePDB import FilePDB
from BackboneChain import BackboneStructure


def run(pdbname):
    file_pdb = FilePDB(pdbname)
    file_pdb.loadData()
    bbStruct = BackboneStructure()
    bbStruct.build_from_atoms(file_pdb.get_backbone())
    fi_psi_list = bbStruct.calculate_fi_psi()
    for fi_psi in fi_psi_list:
        print("{fi}\t{psi}".format(**fi_psi))


def get_from_ftp(pdbname):
    return pdbname


if __name__ == "__main__":
    run("6e8z")

