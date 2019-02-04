'''
Created on 3 lut 2019

@author: Basia
'''
from fileinput import FileInput

class FilePDB():
    #from os import getcwd as LocalWorkDir
    from fileinput import FileInput as LocalPDB

    def __init__(self,pdb_id,pdb_input=LocalPDB,pdb_inputName=lambda pdb_id : pdb_id + '.pdb' ):
        self.ID             = pdb_id
        self.fileInput      = pdb_input
        self.fileInputName  = pdb_inputName(self.ID)
        #self.fileLocation   = getcwd()
        #self.filePath       = path.join(self.fileLocation, self.fileName)
        self.Atoms          = []
        self.Chains         = {}#[]
        #self.SeqRes         = {}
        self.ModelLoaded    = False
        
    def loadData(self,*args):
        status = {'Linijka':0}
        #inputRecord = None
        try:
            for record_line in self.fileInput(self.fileInputName):
                print('Przetwarzanie wiersza nr {linijka}'.format(**status))
                self.process_line(record_line)
            print('Zaladowano {0}'.format(self.fileInputName))
        except (IOError, OSError) as err:
            print('Blad wczytywania pliku "{0}"; {1}'.format(self.fileInputName, err))
            #del inputRecord
            return False
        finally:
            #inputRecord.close()
            return True
            
    def process_line(self,record_line):
        record_type = record_line[0:6]
        if record_type == 'ENDMDL':
            self.ModelLoaded = True
        elif record_type == 'ATOM  ':
            if not self.ModelLoaded:
                atom = {
                    "atomID"     : int(record_line[6:11]),
                    "name"       : record_line[12:16].strip(),
                    "resName"    : record_line[17:20].upper(),
                    "chainID"    : record_line[21:22],
                    "seqID"      : int(record_line[22:26]),
                    "position"   : tuple( map(float, [record_line[a:a+8] for a in range(30,8,46)] ) )
                }
                self.Atoms.append(atom)
        elif record_type == 'SEQRES':
            seqRes = {
                'chainID'   : record_line[11:12],
                'resNumber' : int(record_line[13:17]),
                'resNames'  : record_line[19:70].split()
            }
            self.add_seqRes(seqRes)
        elif record_type == 'END   ':
            self.ModelLoaded = True
            self.validate()
        
    def add_seqRes(self,new_seqRes):
        chainID, chainLen = new_seqRes['chainID'], new_seqRes['resNumber']
        seqRes  = self.Chains.get(chainID,[]) + new_seqRes['resNames'][:]
        if len(seqRes) >= chainLen:
            self.Chains[chainID] = tuple([{"resName" : resName, 'atomSeq' : []} for resName in seqRes])
            
    def validate(self):
        for chainID, chainSeq in self.Chains.iteritems():
            for atmSeq in filter(lambda atm : (atm['chainID'] == chainID), self.Atoms ):
                sequence = chainSeq[atmSeq['seqID']]
                assert sequence['resName'] == atmSeq['resName'], 'Invalid residue name for atom {0}'.format(atmSeq)
                sequence['atomSeq'] += [atmSeq]

    def get_backboneStructure(self,model_type='N=C-CA'):
        checkAtom = lambda atm : (atm['name'] in set(model_type.split(sep = '=-')))
        backbone = {}
        for chainID, chainSeq in self.Chains.items():
            backbone[chainID] = [filter(checkAtom, chainSeq['atomSeq'])]
        return backbone
        
    def quick_info(self):
        #for atm in self.Atoms:
        for chainID, chainSeq in self.get_backboneStructure().items():
            print('chain({0})'.format(chainID))
            for atm in chainSeq:
                print('[seqID]{resName} {name}={position}'.format(**atm))
        #for chn in self.SeqRes.iteritems():
        #    print('{0} {1}'.format(*chn))
            
def test1(param1):
    print('START Test for {0}'.format(param1))
    file_pdb = FilePDB(param1)
    file_pdb.loadData()
    file_pdb.quick_info()
    print(file_pdb.Atoms)
    print('FINISH Test for {0}'.format(param1))
    
if __name__ == 'FilePDB':
    test1('6e8z')
            