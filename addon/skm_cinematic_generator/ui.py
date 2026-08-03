import bpy
from bpy.types import Panel


class SKM_PT_main_panel(Panel):
    bl_label = "SKM Cinematic Generator"
    bl_idname = "SKM_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKM'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.skm_settings

        box = layout.box()
        box.label(text="Scene Settings")
        col = box.column(align=True)
        col.prop(settings, "sanctum_size")
        col.prop(settings, "pillar_height")
        col.prop(settings, "pillar_radius")
        col.prop(settings, "hero_wall_width")
        col.prop(settings, "hero_wall_height")

        box = layout.box()
        box.label(text="Generate")
        col = box.column(align=True)
        col.operator("skm.create_sanctum", icon='MESH_CUBE')
        col.operator("skm.setup_materials", icon='MATERIAL')
        col.operator("skm.setup_lighting", icon='LIGHT')
        col.operator("skm.setup_camera", icon='CAMERA_DATA')
        col.operator("skm.generate_scene", icon='PLAY')
