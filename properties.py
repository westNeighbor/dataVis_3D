import bpy

class DataVisNodesPropertyGroup(bpy.types.PropertyGroup):
    # update function when the property changes

    # properties
    data_filepath: bpy.props.StringProperty(
        description="Path to data file",
        subtype = 'FILE_PATH',
        default="",
        maxlen=4096
    )
