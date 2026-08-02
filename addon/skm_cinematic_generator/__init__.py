bl_info = {
    "name": "SKM Cinematic Generator",
    "author": "OpenAI",
    "version": (0, 1, 0),
    "blender": (5, 2, 0),
    "location": "View3D > Sidebar > SKM",
    "description": "Generate a cinematic sanctum for Singanal Ka Maharaj.",
    "category": "Object",
}

import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty
from bpy.types import Operator, Panel, PropertyGroup


class SKMSettings(PropertyGroup):
    sanctum_size: FloatProperty(
        name="Sanctum Size",
        default=60.0,
        min=10.0,
        max=500.0,
        description="Overall floor size in meters",
    )
    pillar_height: FloatProperty(
        name="Pillar Height",
        default=8.0,
        min=1.0,
        max=50.0,
        description="Pillar height in meters",
    )
    pillar_radius: FloatProperty(
        name="Pillar Radius",
        default=0.55,
        min=0.1,
        max=10.0,
        description="Pillar radius in meters",
    )
    hero_wall_width: FloatProperty(
        name="Hero Wall Width",
        default=18.0,
        min=1.0,
        max=100.0,
        description="Hero wall width in meters",
    )
    hero_wall_height: FloatProperty(
        name="Hero Wall Height",
        default=15.0,
        min=1.0,
        max=100.0,
        description="Hero wall height in meters",
    )


class SKM_OT_generate_scene(Operator):
    bl_idname = "skm.generate_scene"
    bl_label = "Generate Complete Scene"
    bl_description = "Generate a complete cinematic sanctum blockout"

    def execute(self, context):
        from . import generator
        generator.generate_complete_scene(context)
        return {'FINISHED'}


class SKM_OT_create_sanctum(Operator):
    bl_idname = "skm.create_sanctum"
    bl_label = "Create Sanctum"

    def execute(self, context):
        from . import generator
        generator.create_architecture(context)
        return {'FINISHED'}


class SKM_OT_setup_materials(Operator):
    bl_idname = "skm.setup_materials"
    bl_label = "Create Materials"

    def execute(self, context):
        from . import generator
        generator.create_materials(context)
        return {'FINISHED'}


class SKM_OT_setup_lighting(Operator):
    bl_idname = "skm.setup_lighting"
    bl_label = "Setup Lighting"

    def execute(self, context):
        from . import generator
        generator.setup_lighting(context)
        return {'FINISHED'}


class SKM_OT_setup_camera(Operator):
    bl_idname = "skm.setup_camera"
    bl_label = "Setup Camera"

    def execute(self, context):
        from . import generator
        generator.setup_camera(context)
        return {'FINISHED'}


class SKM_PT_main_panel(Panel):
    bl_label = "SKM Cinematic Generator"
    bl_idname = "SKM_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKM'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.skm_settings
        layout.prop(settings, "sanctum_size")
        layout.prop(settings, "pillar_height")
        layout.prop(settings, "pillar_radius")
        layout.prop(settings, "hero_wall_width")
        layout.prop(settings, "hero_wall_height")
        layout.separator()
        layout.operator("skm.create_sanctum", icon='MESH_CUBE')
        layout.operator("skm.setup_materials", icon='MATERIAL')
        layout.operator("skm.setup_lighting", icon='LIGHT')
        layout.operator("skm.setup_camera", icon='CAMERA_DATA')
        layout.operator("skm.generate_scene", icon='PLAY')


classes = (
    SKMSettings,
    SKM_OT_generate_scene,
    SKM_OT_create_sanctum,
    SKM_OT_setup_materials,
    SKM_OT_setup_lighting,
    SKM_OT_setup_camera,
    SKM_PT_main_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.skm_settings = bpy.props.PointerProperty(type=SKMSettings)


def unregister():
    del bpy.types.Scene.skm_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
