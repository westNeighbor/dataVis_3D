import bpy

class DataVisNodesPropertyGroup(bpy.types.PropertyGroup):
    # update function when the property changes

    # properties
    data_filepath: bpy.props.StringProperty(
        description="Path to data file",
        subtype = 'FILE_PATH',
        default="/Users/mhzhao/blenders/dev_addons/dataVis_3D/test.csv",
        maxlen=4096
    )

