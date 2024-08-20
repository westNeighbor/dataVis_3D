# all data operations
"""
data align
"""

import bpy
import math
import os
import bmesh
################################################################
# helper functions BEGIN
################################################################

def load_file(file_path):
    toc = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                if file_path.lower().endswith('.csv'):
                    # row by row
                    entry  = line.split(',')
                    toc.append(entry)

    return toc
################################################################
# helper functions END
################################################################

class dataVis_OT_data_select(bpy.types.Operator):
    bl_idname = "data_vis.data_select"
    bl_label = "Select data to show and animate"
    bl_description = "Select data to show and animate"

    data_element: bpy.props.StringProperty(name="Data Element")

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=750)

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        wm = context.window_manager
        props = scene.dataVis_nodes

        if props.data_filepath:
            toc = load_file(props.data_filepath)
            for line in toc:
                row = layout.row(align=True)
                for element in line:
                    self.data_element = element
                    row.prop(self,"data_element",text="")

classes = (
    dataVis_OT_data_select,
)
register, unregister = bpy.utils.register_classes_factory(classes)
