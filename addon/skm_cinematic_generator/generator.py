import bpy
from math import radians

from .config import DEFAULT_CONFIG
from .materials import create_material_library
from .lighting import setup_lights, setup_world
from .utils import apply_material, ensure_collection, link_object_to_collection


def _clear_scene(context):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.lights):
        if block.users == 0:
            bpy.data.lights.remove(block)
    for block in list(bpy.data.cameras):
        if block.users == 0:
            bpy.data.cameras.remove(block)
    for block in list(bpy.data.materials):
        if block.users == 0:
            bpy.data.materials.remove(block)


def _add_bevel(obj, width=0.04, segments=3):
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = width
    mod.segments = segments
    mod.limit_method = 'ANGLE'
    return mod


def create_architecture(context):
    settings = context.scene.skm_settings
    _clear_scene(context)

    root = ensure_collection("SKM_Cinematic_Generator")
    architecture = ensure_collection("Architecture", root)
    cameras = ensure_collection("Cameras", root)
    ensure_collection("Lighting", root)
    fx = ensure_collection("FX", root)
    ensure_collection("Reference", root)

    scene = context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = DEFAULT_CONFIG.cycles_samples
    scene.cycles.preview_samples = DEFAULT_CONFIG.cycles_preview_samples
    try:
        scene.view_settings.look = 'Filmic'
    except Exception:
        pass
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0

    # Floor
    bpy.ops.mesh.primitive_plane_add(size=settings.sanctum_size, location=(0, 0, 0))
    floor = context.active_object
    floor.name = "Ground_Main"
    link_object_to_collection(floor, architecture)
    floor.modifiers.new(name="Solidify", type='SOLIDIFY').thickness = 0.4
    _add_bevel(floor, 0.04, 3)

    # Steps
    step_w = settings.hero_wall_width / 2.0
    step_d = settings.step_depth
    step_h = settings.step_height
    step_y = 8.0
    for i in range(settings.step_count):
        bpy.ops.mesh.primitive_cube_add(location=(0, step_y + i * 1.0, (i * step_h) / 2 + 0.15))
        step = context.active_object
        step.name = f"Step_{i + 1:02d}"
        step.scale = (step_w / 2, step_d / 2, step_h / 2)
        link_object_to_collection(step, architecture)
        _add_bevel(step, 0.03, 2)

    # Platform
    bpy.ops.mesh.primitive_cube_add(location=(0, 13.0, 1.0))
    platform = context.active_object
    platform.name = "Platform_Main"
    platform.scale = (settings.platform_width / 2.0, settings.platform_depth / 2.0, settings.platform_height / 2.0)
    link_object_to_collection(platform, architecture)
    _add_bevel(platform, 0.04, 3)

    # Hero wall
    bpy.ops.mesh.primitive_cube_add(location=(0, 22.0, settings.wall_height / 2.0 + 0.0))
    wall = context.active_object
    wall.name = "Hero_Wall"
    wall.scale = (settings.wall_width / 2.0, settings.wall_depth / 2.0, settings.wall_height / 2.0)
    link_object_to_collection(wall, architecture)
    _add_bevel(wall, 0.05, 3)

    bpy.ops.mesh.primitive_cube_add(location=(0, 21.45, settings.wall_height / 2.0))
    frame = context.active_object
    frame.name = "Hero_Wall_Frame"
    frame.scale = (settings.wall_width * 0.37, 0.15, settings.wall_height * 0.36)
    link_object_to_collection(frame, architecture)
    _add_bevel(frame, 0.03, 2)

    # Four pillars
    pillar_positions = [(-7.5, 9.0), (7.5, 9.0), (-7.5, 17.0), (7.5, 17.0)]
    for idx, (x, y) in enumerate(pillar_positions, start=1):
        bpy.ops.mesh.primitive_cylinder_add(vertices=settings.pillar_segments, radius=settings.pillar_radius, depth=settings.pillar_height, location=(x, y, settings.pillar_height / 2))
        pillar = context.active_object
        pillar.name = f"Pillar_{idx:02d}"
        link_object_to_collection(pillar, architecture)
        _add_bevel(pillar, 0.06, 3)

        bpy.ops.mesh.primitive_cylinder_add(vertices=settings.pillar_segments, radius=settings.pillar_radius * 1.25, depth=0.35, location=(x, y, 0.175))
        base = context.active_object
        base.name = f"Pillar_{idx:02d}_Base"
        link_object_to_collection(base, architecture)
        _add_bevel(base, 0.02, 2)

        bpy.ops.mesh.primitive_cylinder_add(vertices=settings.pillar_segments, radius=settings.pillar_radius * 1.12, depth=0.35, location=(x, y, settings.pillar_height + 0.175))
        cap = context.active_object
        cap.name = f"Pillar_{idx:02d}_Cap"
        link_object_to_collection(cap, architecture)
        _add_bevel(cap, 0.02, 2)

    # Camera
    cam_data = bpy.data.cameras.new("Camera_Master")
    cam_obj = bpy.data.objects.new("Camera_Master", cam_data)
    cam_obj.location = settings.camera_location
    cam_obj.rotation_euler = tuple(radians(v) for v in settings.camera_rotation_deg)
    cam_data.lens = settings.camera_lens_mm
    cam_data.clip_start = 0.1
    cam_data.clip_end = 1000.0
    cameras.objects.link(cam_obj)
    scene.camera = cam_obj

    # Lighting and world
    setup_world(scene)
    setup_lights(scene)

    # Fog placeholder
    bpy.ops.mesh.primitive_cube_add(location=(0, 8, 3))
    fog = context.active_object
    fog.name = "Fog_Volume"
    fog.scale = (18, 22, 6)
    link_object_to_collection(fog, fx)
    fog.display_type = 'WIRE'

    # Materials
    mats = create_material_library()
    granite = mats["SKM_Granite"]
    sandstone = mats["SKM_Sandstone"]
    bronze = mats["SKM_Bronze"]

    for obj in [floor, platform, wall, frame] + [o for o in architecture.objects if o.name.startswith("Step_") or o.name.startswith("Pillar_")]:
        apply_material(obj, granite)

    if frame.data.materials:
        frame.data.materials[0] = sandstone
    if wall.data.materials:
        wall.data.materials[0] = granite

    return {
        "architecture": architecture.name,
        "cameras": cameras.name,
        "fx": fx.name,
    }


def create_materials(context):
    mats = create_material_library()
    return list(mats.keys())


def setup_lighting(context):
    scene = context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = DEFAULT_CONFIG.cycles_samples
    scene.cycles.preview_samples = DEFAULT_CONFIG.cycles_preview_samples
    setup_world(scene)
    setup_lights(scene)
    return True


def setup_camera(context):
    scene = context.scene
    cam = scene.camera
    if cam is None:
        cam_data = bpy.data.cameras.new("Camera_Master")
        cam = bpy.data.objects.new("Camera_Master", cam_data)
        context.collection.objects.link(cam)
        scene.camera = cam
    cam.location = DEFAULT_CONFIG.camera_location
    cam.rotation_euler = tuple(radians(v) for v in DEFAULT_CONFIG.camera_rotation_deg)
    cam.data.lens = DEFAULT_CONFIG.camera_lens_mm
    cam.data.clip_start = 0.1
    cam.data.clip_end = 1000.0
    return cam.name


def generate_complete_scene(context):
    create_architecture(context)
    create_materials(context)
    setup_lighting(context)
    setup_camera(context)
    return True
