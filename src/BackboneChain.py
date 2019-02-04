'''
Created on 3 lut 2019

@author: Basia
'''
def CalcDihedralAngle(Points):
    from math import atan2,sqrt
    from numpy import subtract,cross,dot,rad2deg
    a,b,c,d = Points
    
    wektor_ab = subtract(b,a)
    wektor_bc = subtract(c,b)
    wektor_cd = subtract(d,c)
    
    ab_X_bc = cross(wektor_ab,wektor_bc)
    bc_X_cd = cross(wektor_bc,wektor_cd)
    
    normalna_abc = ab_X_bc/sqrt(dot(ab_X_bc,ab_X_bc))
    normalna_bcd = bc_X_cd/sqrt(dot(bc_X_cd,bc_X_cd))
    
    orto1 = normalna_bcd
    orto3 = wektor_bc
    orto2 = cross(orto3,orto1)
    
    cosinus = dot(normalna_abc,orto1)
    sinus = dot(normalna_abc,orto2)
    
    radiany = -atan2(sinus,cosinus)
    
    return {'rad' : radiany, 'deg' : rad2deg(radiany)}

class BackboneChain():
    
    def __init__(self,chainID=' '):
        self.ChainID        = chainID
        self.Seqences       = {}
        self.Angles         = []
        self.AngleName      = ['fi','psi']
        self.RefPos         = []
        self.RefSeq         = '???'
    
    def next_angle_name(self):
        ret = self.AngleName[0]
        self.AngleName.reverse()
        return ret

    def add_atom(self,new_atom):
        seqID = new_atom["resSeq"]
        if seqID not in self.Seqences:
            self.Seqences[seqID] = []
        SeqAtom = {
            "name"      : new_atom["name"],
            "residue"   : new_atom["resName"],
            "position"  : (float(new_atom["x"]), float(new_atom["y"]), float(new_atom["z"]))
        }
        self.Seqences[seqID].append(SeqAtom)
        
    def next_torques_from(self,points,nextResName):
        angle = {}
        if not self.Angles:
            angle["from"] = self.RefSeq
        else:
            angle["from"] = self.Angles[-1]["to"]
            
        angle["name"] = self.next_angle_name()
        angle["to"]   = nextResName
        angle["rad"]  = CalcDihedralAngle(points)
        
        self.Angles.append(angle)
        
    def calculate_torques(self):
        points = []
        if not self.Angles:
            for seq in self.Seqences.items(): 
                for atm in seq[1]:
                    print('Processing sequence {0}'.format(seq[0]))
                    print('>>Residue {residue} Atom {name} at {position}'.format(**atm))
                    points.append(atm["position"])
                    if len(points) == 3:
                        self.RefPos = points[:]
                        self.RefSeq = atm["residue"][:]
                    elif len(points) >= 4:
                        self.next_torques_from(points[:],atm["residue"][:])
                        points.pop(0)
                #atm in seq
            #seq in self.Sequences
            
        return self.Angles
    
    def print_fi_psi(self):
        print('Chain({0}): {1} angles calculated'.format(self.ChainID, len(self.Angles)))
        for angle in self.Angles:
            print('{from}->{to} {name}={rad}'.format(**angle))

    def quick_info(self,sortBy=None):
        print('Chain {0}'.format(self.ChainID))
        seqKeys = self.Seqences.keys()
        if sortBy == 'SEQ':
            seqKeys = sorted(seqKeys)
            
        for seqID in seqKeys:
            print('  Sequence{0}'.format(seqID))
            for atm in self.Seqences[seqID]:
                print('    {residue}:{name}={position}'.format(**atm))
                
class BackboneStructure():
    
    def __init__(self,file_pdb=None):
        self.bbChains     = []
        self.TorqueAngles = {}
        if file_pdb:
            for bbc in file_pdb.get_backbone():
                self.add_bbChain(bbc[0],bbc[1])

    def add_bbChain(self,chainID,Atoms):
        PeptideAtomNames = set((' N  ',' CA ',' C  '))
        bbc = BackboneChain(chainID)
        for atm in Atoms:
            if atm["name"] in PeptideAtomNames:
                bbc.add_atom(atm)
        self.bbChains.append(bbc)
        
    def calculate_torques(self):
        if not self.TorqueAngles:
            for bbc in self.bbChains:
                print('Calculating dihedral angles for ChainID({0})...'.format(bbc.ChainID))
                self.TorqueAngles[bbc.ChainID] = bbc.calculate_torques()
        return self.TorqueAngles
    
    def print_fi_psi(self):
        for bbc in self.bbChains:
            bbc.print_fi_psi()

    def quick_info(self,sortBy=None):
        if sortBy == 'CHAIN':
            for bbc in sorted(self.bbChains):
                bbc.quick_info()
        else:
            for bbc in self.bbChains:
                bbc.quick_info(sortBy)
                
def CreateBackboneStructure(inputData):
    from FilePDB import FilePDB
    file_pdb = FilePDB(inputData)
    file_pdb.loadData()
    return BackboneStructure(file_pdb)

def test2(param1,param2):
    from FilePDB import FilePDB
    print('START Test2 for {0}; {1}'.format(param1,param2))
    bbc = BackboneChain(param2)
    file_pdb = FilePDB(param1)
    file_pdb.loadData()
    for atm in file_pdb.Atoms:
        if atm["chainID"] == param2:
            bbc.add_atom(atm)        
    bbc.quick_info()
    print('FINISH Test2 for {0}; {1}'.format(param1,param2))

def test3(param1):
    from FilePDB import FilePDB
    print('START Test3 for {0}'.format(param1))
    file_pdb = FilePDB(param1)
    file_pdb.loadData()
    bbStruct = BackboneStructure()
    for bbc in file_pdb.get_backbone():
        bbStruct.add_bbChain(bbc[0],bbc[1])
    bbStruct.quick_info('SEQ')
    print('FINISH Test3 for {0}'.format(param1))
    
def test4(inputData):
    bbs = CreateBackboneStructure(inputData)
    if bbs.calculate_torques():
        bbs.print_fi_psi();
    
if __name__ == 'BackboneChain':
    test4('6e8z')
    