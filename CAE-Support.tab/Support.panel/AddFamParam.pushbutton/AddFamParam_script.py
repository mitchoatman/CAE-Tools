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
    
    t = Transaction(doc, 'Add Specific Type Parameters to Family')
    t.Start()
    
    app.SharedParametersFilename = fullPath
    spFile = app.OpenSharedParameterFile()
    
    if not spFile:
        forms.alert("Failed to open the selected shared parameter file.", exitscript=True)
        t.RollBack()
        return
    
    family_mgr = doc.FamilyManager
    
    # Define exact list of parameter names you want to load
    target_parameters = [
        "CAE_Global_Building_Area",
        "CAE_Global_Building_Level",
        "CAE_Global_Element_Service Type",
        "CAE_Global_Pick"
    ]
    
    def add_specific_family_parameters(group_name, group_type, allowed_names):
        for dG in spFile.Groups:
            if dG.Name == group_name:
                for eD in dG.Definitions:
                    if eD.Name in allowed_names:
                        existing_param = family_mgr.get_Parameter(eD.Name)
                        if not existing_param:
                            # AddParameter(ExternalDefinition, ParameterGroup, isInstance) -> False for Type
                            family_mgr.AddParameter(eD, group_type, False)
    
    # Handle Group Type based on Revit version
    if RevitINT > 2024:
        from Autodesk.Revit.DB import GroupTypeId
        text_group = GroupTypeId.Text
        add_specific_family_parameters('CAE Global Parameters', text_group, target_parameters)
    else:
        from Autodesk.Revit.DB import BuiltInParameterGroup
        text_group = BuiltInParameterGroup.PG_TEXT
        add_specific_family_parameters('CAE Global Parameters', text_group, target_parameters)
    
    t.Commit()
    forms.alert("Selected shared parameters successfully added to the family as Type parameters!", title="Success")

Shared_Params()