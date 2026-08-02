bl_info = {
    "name": "SKM Cinematic Generator",
    "author": "OpenAI",
    "version": (0, 2, 0),
    "blender": (5, 2, 0),
    "location": "View3D > Sidebar > SKM",
    "description": "Generate a cinematic sanctum for Singanal Ka Maharaj.",
    "category": "Object",
}

import bpy

from .config import DEFAULT_CONFIG
from .operators import (
    SKM_OT_create_sanctum,
    SKM_OT_generate_scene,
    SKM_OT_setup_camera,
    SKM_OT_setup_lighting,
    SKM_OT_setup_materials,
)
from .ui import SKM_PT_main_panel


class SKMSettings(bpy.types.PropertyGroup):
    sanctum_size: bpy.props.FloatProperty(
        name="Sanctum Size",
        default=DEFAULT_CONFIG.sanctum_size,
        min=10.0,
        max=500.0,
    )
    pillar_height: bpy.props.FloatProperty(
        name="Pillar Height",
        default=DEFAULT_CONFIG.pillar_height,
        min=1.0,
        max=50.0,
    )
    pillar_radius: bpy.props.FloatProperty(
        name="Pillar Radius",
        default=DEFAULT_CONFIG.pillar_radius,
        min=0.1,
        max=10.0,
    )
    hero_wall_width: bpy.props.FloatProperty(
        name="Hero Wall Width",
        default=DEFAULT_CONFIG.wall_width,
        min=1.0,
        max=100.0,
    )
    hero_wall_height: bpy.props.FloatProperty(
        name="Hero Wall Height",
        default=DEFAULT_CONFIG.wall_height,
        min=1.0,
        max=100.0,
    )


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
    if hasattr(bpy.types.Scene, "skm_settings"):
        del bpy.types.Scene.skm_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
