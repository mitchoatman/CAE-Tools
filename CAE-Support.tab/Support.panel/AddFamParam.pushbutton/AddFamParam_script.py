import os
import clr

# Load Windows Forms safely
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import OpenFileDialog, DialogResult
from pyrevit import forms
from Autodesk.Revit.DB import Transaction

doc = __revit__.ActiveUIDocument.Document

if not doc.IsFamilyDocument:
    forms.alert("This script must be run inside an open Family Editor document (.rfa).", exitscript=True)

app = doc.Application
RevitVersion = app.VersionNumber
RevitINT = float(RevitVersion)

def Shared_Params():
    dialog = OpenFileDialog()
    dialog.Filter = "Shared Parameter Files (*.txt)|*.txt"
    dialog.Title = "Select Shared Parameter File"
    
    if dialog.ShowDialog() != DialogResult.OK:
        return
        
    fullPath = dialog.FileName
    
    t = Transaction(doc, 'Add Custom Type/Instance Parameters to Family')
    t.Start()
    
    app.SharedParametersFilename = fullPath
    spFile = app.OpenSharedParameterFile()
    
    if not spFile:
        forms.alert("Failed to open the selected shared parameter file.", exitscript=True)
        t.RollBack()
        return
    
    family_mgr = doc.FamilyManager
    
    # Define exact parameters with their individual Group and Instance settings (True = Instance, False = Type)
    parameters_to_add = [
        {"name": "CAE_Global_Element_Service Type", "group": "CAE Global Parameters", "is_instance": False},
        {"name": "CAE_Annotation_Equipment_Type", "group": "CAE Annotation Parameters", "is_instance": False},
        {"name": "CAE_Annotation_Equipment_Number", "group": "CAE Annotation Parameters", "is_instance": True},
        {"name": "CAE_Global_Building_Area", "group": "CAE Global Parameters", "is_instance": True},
        {"name": "CAE_Global_Building_Level", "group": "CAE Global Parameters", "is_instance": True},
        {"name": "CAE_Global_Pick", "group": "CAE Global Parameters", "is_instance": True},
        {"name": "CAE_Annotation_Pipe Accessory_Number", "group": "CAE Annotation Parameters", "is_instance": True},
        {"name": "CAE_Annotation_Pipe Accessory_Type", "group": "CAE Annotation Parameters", "is_instance": False}
    ]
    
    # Handle Group Type based on Revit version
    if RevitINT > 2024:
        from Autodesk.Revit.DB import GroupTypeId
        text_group = GroupTypeId.Text
    else:
        from Autodesk.Revit.DB import BuiltInParameterGroup
        text_group = BuiltInParameterGroup.PG_TEXT
        
    # Create a lookup for groups in the shared parameter file
    sp_groups = {g.Name: g for g in spFile.Groups}
    
    # Loop through configuration and add each parameter with its specific type/instance setting
    for item in parameters_to_add:
        g_name = item["group"]
        p_name = item["name"]
        is_inst = item["is_instance"]
        
        if g_name in sp_groups:
            dG = sp_groups[g_name]
            for eD in dG.Definitions:
                if eD.Name == p_name:
                    existing_param = family_mgr.get_Parameter(eD.Name)
                    if not existing_param:
                        # AddParameter(ExternalDefinition, ParameterGroup, isInstance)
                        family_mgr.AddParameter(eD, text_group, is_inst)
                    break
    
    t.Commit()
    forms.alert("Shared parameters successfully added with mixed Type and Instance settings!", title="Success")

Shared_Params()