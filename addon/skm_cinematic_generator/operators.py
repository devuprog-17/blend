import bpy
from bpy.types import Operator

from . import generator


class SKM_OT_generate_scene(Operator):
    bl_idname = "skm.generate_scene"
    bl_label = "Generate Complete Scene"
    bl_description = "Generate a complete cinematic sanctum scene"

    def execute(self, context):
        try:
            generator.generate_complete_scene(context)
        except Exception as exc:
            self.report({'ERROR'}, f"SKM scene generation failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, "SKM scene generated")
        return {'FINISHED'}


class SKM_OT_create_sanctum(Operator):
    bl_idname = "skm.create_sanctum"
    bl_label = "Create Sanctum"
    bl_description = "Create the sanctum architecture blockout"

    def execute(self, context):
        try:
            generator.create_architecture(context)
        except Exception as exc:
            self.report({'ERROR'}, f"Sanctum creation failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, "Sanctum created")
        return {'FINISHED'}


class SKM_OT_setup_materials(Operator):
    bl_idname = "skm.setup_materials"
    bl_label = "Create Materials"
    bl_description = "Create procedural materials"

    def execute(self, context):
        try:
            generator.create_materials(context)
        except Exception as exc:
            self.report({'ERROR'}, f"Material creation failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, "Materials created")
        return {'FINISHED'}


class SKM_OT_setup_lighting(Operator):
    bl_idname = "skm.setup_lighting"
    bl_label = "Setup Lighting"
    bl_description = "Create camera lighting setup"

    def execute(self, context):
        try:
            generator.setup_lighting(context)
        except Exception as exc:
            self.report({'ERROR'}, f"Lighting setup failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, "Lighting created")
        return {'FINISHED'}


class SKM_OT_setup_camera(Operator):
    bl_idname = "skm.setup_camera"
    bl_label = "Setup Camera"
    bl_description = "Create and position cinematic camera"

    def execute(self, context):
        try:
            generator.setup_camera(context)
        except Exception as exc:
            self.report({'ERROR'}, f"Camera setup failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, "Camera created")
        return {'FINISHED'}


class SKM_OT_setup_render(Operator):
    bl_idname = "skm.setup_render"
    bl_label = "Setup Render"
    bl_description = "Configure Cycles render settings for preview and final output"

    def execute(self, context):
        try:
            generator.setup_render(context)
        except Exception as exc:
            self.report({'ERROR'}, f"Render setup failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, "Render settings configured")
        return {'FINISHED'}
