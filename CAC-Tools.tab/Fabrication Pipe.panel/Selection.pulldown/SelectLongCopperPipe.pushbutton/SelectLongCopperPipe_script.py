import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, BuiltInCategory, BuiltInParameter
from pyrevit import revit, DB, UI


#define the active Revit application and document
DB = Autodesk.Revit.DB
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
curview = doc.ActiveView
fec = FilteredElementCollector
app = doc.Application
RevitVersion = app.VersionNumber
RevitINT = float (RevitVersion)

selection = revit.get_selection()

# Creating collector instance and collecting all the fabrication hangers from the model
pipe_collector = FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_FabricationPipework) \
                   .WhereElementIsNotElementType() \
                   .ToElements()


elementlist = []
t = Transaction(doc, 'Select Pipes')
#Start Transaction
t.Start()
for pipe in pipe_collector:
    CID = pipe.ItemCustomId
    if CID == 2041:
        pipelen = pipe.Parameter[BuiltInParameter.FABRICATION_PART_LENGTH].AsDouble()
        pipemat = pipe.Parameter[BuiltInParameter.FABRICATION_PART_MATERIAL].AsValueString()  #Copper: Hard Copper  #Cast Iron: Cast Iron
        if pipelen > 20.0 and pipemat == 'Copper: Hard Copper':
            elementlist.append(pipe.Id)
selection.set_to(elementlist)
#End Transaction
t.Commit()

