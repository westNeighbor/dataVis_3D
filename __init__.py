'''
Copyright (C) 2024 Minghui Zhao
zhaominghui2011@gmail.com

Created by Minghui Zhao

    This is a blender addon to help visualize data in 3D viewport

'''

bl_info = {
    "name": "dataVis",
    "description": "Visualize data in Blender 3D viewport with Geometry Nodes",
    "author": "Minghui Zhao -> zhaominghui2011@gmail.com",
    "version": (1, 0, 0),
    "blender": (4, 1, 0),
    "location": "3D View > Sidebar > dataVis",
    "warning": "",
    "doc_url": "https://github.com/westNeighbor/dataVis_3D",
    "tracker_url": "https://github.com/westNeighbor/dataVis_3D/issues",
    "category": "3D View",
    }

import importlib
import sys
import bpy

from .preferences import *
from .ui import *
from .properties import *
from .operations import *

'''
@bpy.app.handlers.persistent
def subtitle_frame_depsgraph(scene, desp):  # used for scene driven properties live updating!
    """update on depsgraph change"""
    #bpy.context.evaluated_depsgraph_get()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
    return None
'''

@bpy.app.handlers.persistent
def subtitle_frame_frame_pre(scene, desp):  # used for scene driven properties live udpating!
    """update on frame change"""
    #bpy.context.evaluated_depsgraph_get()
    for o in scene.objects:
        if o.type == 'MESH':
            mesh = o.data
            if mesh.attributes.find('hactive_line')!=-1:
                nodegroup = o.modifiers['subtitleGeoNodes'].node_group
                start_frame = nodegroup.nodes['startFrame'].string
                start_frame = [int(x) for x in start_frame.split(sep=' ')]
                start_index = nodegroup.nodes['startIndex'].string
                start_index = [int(x) for x in start_index.split(sep=' ')]
                line_len    = nodegroup.nodes['lineLen'].string
                line_len    = [int(x) for x in line_len.split(sep=' ')]
                ncol = max(line_len) + 1

                settings = scene.subtitleNodes_settings[mesh.name]
                delayframe = settings.subtitle_delayframe
                shift = nodegroup.nodes['StringCurvesTextbody'].inputs['Line Spacing'].default_value
                switch = o.modifiers['subtitleGeoNodes']["Socket_15"]
                direction = nodegroup.nodes['vlayout'].inputs[1].default_value
                if settings.subtitle_layout == 'Horizontal' or settings.subtitle_alignment == 'Filled':
                    for i in range(len(start_index)):
                        if scene.frame_current >= start_frame[i]+delayframe and scene.frame_current < start_frame[i+1]+delayframe:
                            if settings.subtitle_layout == 'Horizontal':
                                if nodegroup.nodes['Combine XYZ'].inputs['X'].default_value != 0.0:
                                    nodegroup.nodes['Combine XYZ'].inputs['Y'].default_value = nodegroup.nodes['Combine XYZ'].inputs['X'].default_value*direction*(-1)
                                    nodegroup.nodes['Combine XYZ'].inputs['X'].default_value = 0.0
                                else:
                                    nodegroup.nodes['Combine XYZ'].inputs['Y'].default_value = switch*i*shift
                            else:
                                nodegroup.nodes['Combine XYZ'].inputs['X'].default_value = 0.0
                                nodegroup.nodes['Combine XYZ'].inputs['Y'].default_value = 0.0
                else:
                    for i in range(len(start_index)):
                        if scene.frame_current >= start_frame[i]+delayframe and scene.frame_current < start_frame[i+1]+delayframe:
                            if nodegroup.nodes['Combine XYZ'].inputs['Y'].default_value != 0.0:
                                nodegroup.nodes['Combine XYZ'].inputs['X'].default_value = nodegroup.nodes['Combine XYZ'].inputs['Y'].default_value*direction*(-1)
                                nodegroup.nodes['Combine XYZ'].inputs['Y'].default_value = 0.0
                            else:
                                nodegroup.nodes['Combine XYZ'].inputs['X'].default_value = switch*i*shift*direction*(-1)

                hactive_line = [False]*(len(mesh.attributes['hactive_line'].data))
                vactive_line = [False]*(len(mesh.attributes['hactive_line'].data))
                for i in range(len(start_index)):
                    if scene.frame_current >= start_frame[i]+delayframe and scene.frame_current < start_frame[i+1]+delayframe:
                        for j in range(start_index[i],start_index[i]+line_len[i]):
                            hactive_line[j] = True
                for i in range(len(start_index)):
                    if scene.frame_current >= start_frame[i]+delayframe and scene.frame_current < start_frame[i+1]+delayframe:
                        for j in range(i*ncol,(i+1)*ncol):
                            vactive_line[j] = True
                attribute = mesh.attributes['hactive_line']
                attribute.data.foreach_set("value",hactive_line)
                attribute = mesh.attributes['vactive_line']
                attribute.data.foreach_set("value",vactive_line)
                o.modifiers['subtitleGeoNodes'].node_group.interface_update(bpy.context)

    return None

def all_handlers():
    """return a list of handler stored in .blend"""

    return_list = []
    for oh in bpy.app.handlers:
        try:
            for h in oh:
                return_list.append(h)
        except:
            pass
    return return_list


def register_handlers(status):
    """register dispatch for handlers"""

    if (status == "register"):

        all_handler_names = [h.__name__ for h in all_handlers()]

        # depsgraph
        #if "audio_frame_depsgraph" not in all_handler_names:
        #    bpy.app.handlers.depsgraph_update_pre.append(audio_frame_depsgraph)

        # frame_change
        if "subtitle_frame_frame_pre" not in all_handler_names:
            bpy.app.handlers.frame_change_pre.append(subtitle_frame_frame_pre)

        return None

    elif (status == "unregister"):

        for h in all_handlers():

            # depsgraph
            #if (h.__name__ == "audio_frame_depsgraph"):
            #    bpy.app.handlers.depsgraph_update_pre.remove(h)

            # frame_change
            if (h.__name__ == "subtitle_frame_frame_pre"):
                bpy.app.handlers.frame_change_pre.remove(h)

    return None


def register():
    # preferences
    #bpy.utils.register_class(InstallDependencies)
    #bpy.utils.register_class(UninstallDepencencies)
    #bpy.utils.register_class(CheckInstallation)
    bpy.utils.register_class(Preferences)

    # properties
    bpy.utils.register_class(DataVisNodesPropertyGroup)
    bpy.types.Scene.dataVis_nodes = bpy.props.PointerProperty(name="dataVis_nodes",type=DataVisNodesPropertyGroup)
    bpy.types.Scene.dataVisNodes_settings = bpy.props.CollectionProperty(name="dataVisNodes_settings",type=DataVisNodesPropertyGroup)

    # operators
    #bpy.utils.register_class(CreateNewSubtitle)
    #bpy.utils.register_class(UpdateSubtitle)

    # ui
    bpy.utils.register_class(DataVisPanel)
    #bpy.types.Scene.show_demo_panel = BoolProperty(default=False)

    # handlers
    register_handlers("register")

def unregister():
    # handlers
    register_handlers("unregister")

    # ui
    bpy.utils.unregister_class(DataVisPanel)

    # operators
    #bpy.utils.unregister_class(CreateNewSubtitle)
    #bpy.utils.unregister_class(UpdateSubtitle)

    # properties
    bpy.utils.unregister_class(DataVisNodesPropertyGroup)
    del bpy.types.Scene.dataVis_nodes
    del bpy.types.Scene.dataVisNodes_settings

    # preferences
    bpy.utils.unregister_class(Preferences)
    #bpy.utils.unregister_class(InstallDependencies)
    #bpy.utils.unregister_class(UninstallDepencencies)
    #bpy.utils.unregister_class(CheckInstallation)

if __name__ == '__main__':
    try:
        unregister()
    except:
        pass
    register()
