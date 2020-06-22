# https://blender.stackexchange.com/q/57306/3710
# https://blender.stackexchange.com/q/79779/3710

#
# modified for blender 2.80 
# last modification: 2019-09-12 -- add custom-preferences panel -- Emanuel Rumpf --

bl_info = {
    "name": "aifa tool",
    "description": "",
    "author": "liyouwang",
    "version": (0, 0, 1),
    "blender": (2, 83, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

"""
This is an addon - template for blender 2.80 
Use it as base for new addons.
--
Some changes made for blender 2.80 version (from 2.79):
- Properties are annotations now, assigned with : not =
- bl_region_type now is "UI" not "TOOLS"
- Registration procedure changed: 
  Use bpy.utils.register_class() not register_module()

More information see: python api blender 2.80
"""

import bpy
import bmesh
import os
import pickle

def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))

from bpy.utils import ( register_class, unregister_class )
from bpy.props import ( StringProperty,
                        BoolProperty,
                        IntProperty,
                        FloatProperty,
                        FloatVectorProperty,
                        EnumProperty,
                        PointerProperty,
                       )
from bpy.types import ( Panel,
                        AddonPreferences,
                        Operator,
                        PropertyGroup,
                      )



# this must match the addon name, use '__package__'
# when defining this in a submodule of a python package.
addon_name = __name__      # when single file 
#addon_name = __package__   # when file in package 


# ------------------------------------------------------------------------
#   settings in addon-preferences panel 
# ------------------------------------------------------------------------


# panel update function for PREFS_PT_MyPrefs panel 
def _update_panel_fnc (self, context):
    #
    # load addon custom-preferences 
    print( addon_name, ': update pref.panel function called' )
    #
    main_panel =  OBJECT_PT_my_panel
    #
    main_panel .bl_category = context .preferences.addons[addon_name] .preferences.tab_label
    # re-register for update 
    unregister_class( main_panel )
    register_class( main_panel )


class PREFS_PT_MyPrefs( AddonPreferences ):
    ''' Custom Addon Preferences Panel - in addon activation panel -
    menu / edit / preferences / add-ons  
    '''

    bl_idname = addon_name

    tab_label: StringProperty(
            name="Tab Label",
            description="Choose a label-name for the panel tab",
            default="New Addon",
            update=_update_panel_fnc
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="Tab Label:")
        col.prop(self, "tab_label", text="")





# ------------------------------------------------------------------------
#   properties visible in the addon-panel 
# ------------------------------------------------------------------------

class PG_MyProperties (PropertyGroup):

    file_path : StringProperty(
        name="output path",
        description=":",
        default="",
        maxlen=1024,
        )

    file_name : StringProperty(
        name="output name",
        description=":",
        default="",
        maxlen=1024,
        )

# ------------------------------------------------------------------------
#   operators
# ------------------------------------------------------------------------

class OT_STOREINDEXOperator (bpy.types.Operator):
    bl_idname = "wm.store_index"
    bl_label = "store index"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool  # this get other class propty

        print("string value:", mytool.file_path)
        print("string value:", mytool.file_name)
        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        verts_index = [v.index for v in bm.verts if v.select]
        save_pickle_file(os.path.join(mytool.file_path, "{}.pkl".format(mytool.file_name)) , verts_index)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#   addon - panel -- visible in objectmode
# ------------------------------------------------------------------------

class OBJECT_PT_my_panel (Panel):
    bl_idname = "OBJECT_PT_my_panel"
    bl_label = "AIFA TOOL"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tool"  # note: replaced by preferences-setting in register function  


#   def __init(self):
#       super( self, Panel ).__init__()
#       bl_category = bpy.context.preferences.addons[__name__].preferences.category 

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        layout.prop( mytool, "file_path")
        layout.prop( mytool, "file_name")
        layout.operator( "wm.store_index")

# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------

classes = (
    PG_MyProperties,
    OT_STOREINDEXOperator,
    OBJECT_PT_my_panel, 
    PREFS_PT_MyPrefs, 
)

def register():
    #
    for cls in classes:
        register_class(cls)
    #
    bpy.types.Scene.my_tool = PointerProperty(type=PG_MyProperties)

    #

def unregister():
    #
    for cls in reversed(classes):
        unregister_class(cls)
    #
    del bpy.types.Scene.my_tool  # remove PG_MyProperties 




if __name__ == "__main__":
    register()