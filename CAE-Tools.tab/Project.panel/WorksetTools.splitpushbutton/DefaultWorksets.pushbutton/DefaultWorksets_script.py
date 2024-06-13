from __future__ import print_function
from Autodesk.Revit.DB import Workset, Transaction, BuiltInCategory, FilteredWorksetCollector

doc = __revit__.ActiveUIDocument.Document

WorksetNames = []
LevelNames = []

AllWorksets = FilteredWorksetCollector(doc)
for c in AllWorksets:
	WorksetNames.append(c.Name)

WorksetToAdd = []
WorksetToAdd.append('CAE_Detailing')
WorksetToAdd.append('Shared Views, levels, Grids')
WorksetToAdd.append('zArch')
WorksetToAdd.append('zMech')
WorksetToAdd.append('zStruct')
WorksetToAdd.append('zElec')
WorksetToAdd.append('zMP')
WorksetToAdd.append('zSprinkler')
WorksetToAdd.append('zFraming')
WorksetToAdd.append('zPtube')
WorksetToAdd.append('zPlumbing')
WorksetToAdd.append('CAE_Precon')
WorksetToAdd.append('CAE_Precon_Handoff')
WorksetToAdd.append('CAE_Precon_Equipment')

worksetaddedlist = []

t = Transaction(doc)
t.Start('Create Worksets')
try:
    WorksetList = list(set(WorksetToAdd).difference(set(WorksetNames)))
    if len(WorksetList) > 0:
        for wset in WorksetList:
            Workset.Create(doc, str(wset))
            worksetaddedlist.append(wset)
        print ('Added Workset(s):')
        print (*worksetaddedlist,sep='\n')
    else:
        print ('Worksets already exist')
except:
    pass
t.Commit()
