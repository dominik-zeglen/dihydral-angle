import gzip
from ftplib import FTP

from .FilePDB import FilePDB
from .BackboneChain import BackboneStructure

TEMP_FILE_NAME = "temp.gz"


def get_pdb_info(pdb_name):
    # First check if file exists, then decide if it should be
    # downloaded in the first place
    try:
        open("data/" + pdb_name + ".pdb")
    except IOError:
        get_from_ftp(pdb_name)

    pdb_content = FilePDB(pdb_name)
    bbStruct = BackboneStructure()
    bbStruct.build_from_atoms(pdb_content.get_backbone())
    fi_psi_list = bbStruct.calculate_fi_psi()
    return [angles for angles in fi_psi_list]


def get_from_ftp(pdb_name):
    pdb_path = "/pub/pdb/data/structures/divided/pdb/" + pdb_name[1:3]
    pdb_file_name = "pdb" + pdb_name + ".ent.gz"

    with FTP("ftp.rcsb.org") as ftp:
        ftp.login()
        ftp.cwd(pdb_path)
        with open(TEMP_FILE_NAME, "wb") as tempFile:
            ftp.retrbinary("RETR " + pdb_file_name, tempFile.write)

    with gzip.open(TEMP_FILE_NAME) as gz_file:
        with open("data/" + pdb_name + ".pdb", "wb") as pdb_file:
            pdb_file.write(gz_file.read())

