import bpy

class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label(text='This is 3D viewport data visualization addon.')
        layout.label(text='')
#        layout.label(text=' ')
#        layout.label(text='You can set a default font for the subtitle/lyric, ')
#        layout.label(text='otherwise it is the blend default "Bfont Regular" font')
#        layout.prop(context.scene.subtitle_nodes, "subtitle_fontpath",text="Subtitle Font",placeholder="Bfont Regular",icon="FILE_FONT")
