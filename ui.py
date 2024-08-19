import bpy

class DataVisPanel(bpy.types.Panel):
    bl_idname = "DATAVIS_PT_Panel"
    bl_label = "data vis in 3D viewport"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Data Vis"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = True # False for no animation.

        scene = context.scene
        propData = scene.dataVis_nodes

        # choose subtitle/lyric file
        layout.label(text="Load data")
        layout.prop(propData,"data_filepath",text="Data File",placeholder="select the data file")
