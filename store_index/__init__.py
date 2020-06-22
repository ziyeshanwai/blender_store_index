# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "store_index",
    "author" : "liyouwang",
    "description" : "store selected index to specific path",
    "blender" : (2, 83, 0),
    "version" : (0, 0, 1),
    "location" : "View3D > Mesh",
    "warning" : "",
    "category" : "Mesh"
}

import bpy
import os
import bmesh
import pickle

def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))

class store_index(bpy.types.Operator):

    bl_idname = "strore_index"
    bl_label = "stroreindex"
    bl_options = {'REGISTER', 'UNDO'}
    file_path = bpy.props.StringProperty(
        name = "filepath",
        description = "the index to store",
        default=os.getcwd()
    )
    generate_name = bpy.props.StringProperty(
        name = "name",
        description = "the index to store name",
        default='default_name'
    )

    @classmethod
    def poll(self, context):
        return context.mode == 'EDIT'

    def execute(self, context):
        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        verts_index = [v.index for v in bm.verts if v.select]
        save_pickle_file(os.path.join(self.file_path, "{}.pkl".format(self.generate_name)) , verts_index)
        return {'FINISHED'}
    
    def invoke(self,context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "file_path", text='file_path: ', icon='CURVE_NCIRCLE', slider=False, expand=True)
        layout.prop(self, "generate_name", text='generate_name: ', icon='CURVE_NCIRCLE', slider=False, expand=True)
        layout.separator()

def toggle_automerge_button(self, context):
    op = self.layout.operator(
        "wm.context_toggle",
        text="Toggle Automerge",
        icon='PLUGIN')
    op.data_path = "scene.tool_settings.use_mesh_automerge"

def menu_func(self, context):
    self.layout.operator(store_index.bl_idname)

def register():

    bpy.utils.register_class(store_index)

def unregister():

    bpy.utils.unregister_class(store_index)


