import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, BuiltInCategory, FabricationConfiguration
from pyrevit import revit, DB, UI, forms
import sys


#define the active Revit application and document
DB = Autodesk.Revit.DB
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
curview = doc.ActiveView
fec = FilteredElementCollector
app = doc.Application
RevitVersion = app.VersionNumber
RevitINT = float (RevitVersion)
Config = FabricationConfiguration.GetFabricationConfiguration(doc)

selection = revit.get_selection()

def get_parameter_value_by_name_asvaluestring(element, parameterName):
    return element.LookupParameter(parameterName).AsValueString()

def get_parameter_value_by_name_asstring(element, parameterName):
    return element.LookupParameter(parameterName).AsString()

# Creating collector instance and collecting all the fabrication hangers from the model
part_collector = FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_FabricationPipework) \
                   .UnionWith(FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_FabricationHangers)) \
                   .UnionWith(FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_FabricationDuctwork)) \
                   .WhereElementIsNotElementType() \
                   .ToElements()

# collector for size only
hanger_collector = FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_FabricationHangers) \
                   .WhereElementIsNotElementType() \
                   .ToElements()
pipeduct_collector = FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_FabricationPipework) \
                   .UnionWith(FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_FabricationDuctwork)) \
                   .WhereElementIsNotElementType() \
                   .ToElements()

if part_collector:

    servicetypenamelist = []
    CIDlist = []
    Namelist = []
    SNamelist = []
    SNameABBRlist = []
    STRATUSAssemlist = []
    Sizelist = []
    ValveNumlist = []
    LineNumlist = []
    STRATUSStatuslist = []

    for elem in part_collector:
        ST = Config.GetServiceTypeName(elem.ServiceType)
        servicetypenamelist.append(ST)

    for elem in part_collector:
        CID = elem.ItemCustomId
        CIDlist.append(CID)

    for elem in part_collector:
        NAME = get_parameter_value_by_name_asvaluestring(elem, 'Family')
        Namelist.append(NAME)

    for elem in part_collector:
        SNAME = get_parameter_value_by_name_asstring(elem, 'Fabrication Service Name')
        SNamelist.append(SNAME)

    for elem in part_collector:
        SNAMEABBR = get_parameter_value_by_name_asstring(elem, 'Fabrication Service Abbreviation')
        SNameABBRlist.append(SNAMEABBR)

    for elem in part_collector:
        SAssembly = get_parameter_value_by_name_asstring(elem, 'STRATUS Assembly')
        STRATUSAssemlist.append(SAssembly)

    for elem in part_collector:
        SStatus = get_parameter_value_by_name_asstring(elem, 'STRATUS Status')
        STRATUSStatuslist.append(SStatus)

    for elem in part_collector:
        ValveNumber = get_parameter_value_by_name_asstring(elem, 'FP_Valve Number')
        ValveNumlist.append(ValveNumber)

    for elem in part_collector:
        LineNumber = get_parameter_value_by_name_asstring(elem, 'FP_Line Number')
        LineNumlist.append(LineNumber)

# Size filter only
    for elem in hanger_collector:
            SIZE = get_parameter_value_by_name_asstring(elem, 'Size of Primary End')
            Sizelist.append(SIZE)
    for elem in pipeduct_collector:
            PRTSIZE = get_parameter_value_by_name_asstring(elem, 'Size')
            Sizelist.append(PRTSIZE)

    try:

        GroupOptions = {'CID': sorted(set(CIDlist)),
                        'ServiceType': sorted(set(servicetypenamelist)),
                        'Name': sorted(set(Namelist)),
                        'Service Name': sorted(set(SNamelist)),
                        'Service Abbreviation': sorted(set(SNameABBRlist)),
                        'Size': sorted(set(Sizelist)),
                        'STRATUS Assembly': sorted(set(STRATUSAssemlist)),
                        'Line Number': sorted(set(LineNumlist)),
                        'STRATUS Status': sorted(set(STRATUSStatuslist)),
                        'Valve Number': sorted(set(ValveNumlist))}

        res = forms.SelectFromList.show(GroupOptions,group_selector_title='Property Type:', multiselect=True, button_name='Select Item(s)', exitscript = True)

        elementlist = []
        elementlistsz = []
        for fil in res:
            for elem in part_collector:
                if Config.GetServiceTypeName(elem.ServiceType) == fil:
                    elementlist.append(elem.Id)
                if elem.ItemCustomId == fil:
                    elementlist.append(elem.Id)
                if get_parameter_value_by_name_asvaluestring(elem, 'Family') == fil:
                    elementlist.append(elem.Id)
                if get_parameter_value_by_name_asstring(elem, 'Fabrication Service Name') == fil:
                    elementlist.append(elem.Id)
                if get_parameter_value_by_name_asstring(elem, 'Fabrication Service Abbreviation') == fil:
                    elementlist.append(elem.Id)
                if get_parameter_value_by_name_asstring(elem, 'STRATUS Assembly') == fil:
                    elementlist.append(elem.Id)
                if get_parameter_value_by_name_asstring(elem, 'STRATUS Status') == fil:
                    elementlist.append(elem.Id)
                if get_parameter_value_by_name_asstring(elem, 'FP_Valve Number') == fil:
                    elementlist.append(elem.Id)
                if get_parameter_value_by_name_asstring(elem, 'FP_Line Number') == fil:
                    elementlist.append(elem.Id)
# Size filter only
        for fil in res:
            for elem in hanger_collector:
                if get_parameter_value_by_name_asstring(elem, 'Size of Primary End') == fil:
                    elementlist.append(elem.Id)
        for fil in res:
            for elem in pipeduct_collector:
                if get_parameter_value_by_name_asstring(elem, 'Size') == fil:
                    elementlist.append(elem.Id)
        selection.set_to(elementlist)


    except:
        sys.exit()
else:
    forms.alert('No Fabrication parts in view.', exitscript=True)