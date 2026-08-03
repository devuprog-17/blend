import bpy
from math import radians

from .materials import create_material_library


ADDON_PREFIX = "SKM_"


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


def _ensure_collection(name, parent=None):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        if parent is None:
            bpy.context.scene.collection.children.link(coll)
        else:
            parent.children.link(coll)
    return coll


def _link_object(obj, collection):
    if obj.name not in collection.objects:
        collection.objects.link(obj)
    for c in list(obj.users_collection):
        if c != collection:
            c.objects.unlink(obj)


def _apply_material(obj, mat):
    if obj.type != 'MESH':
        return
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def create_architecture(context):
    settings = context.scene.skm_settings
    _clear_scene(context)

    root = _ensure_collection("SKM_Cinematic_Generator")
    architecture = _ensure_collection("Architecture", root)
    cameras = _ensure_collection("Cameras", root)
    lighting = _ensure_collection("Lighting", root)
    fx = _ensure_collection("FX", root)
    _ensure_collection("Reference", root)

    scene = context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    if hasattr(scene.cycles, "preview_samples"):
        scene.cycles.preview_samples = 32
    if hasattr(scene.cycles, "samples"):
        scene.cycles.samples = 128
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
    _link_object(floor, architecture)
    floor.modifiers.new(name="Solidify", type='SOLIDIFY').thickness = 0.4
    bev = floor.modifiers.new(name="Bevel", type='BEVEL')
    bev.width = 0.04
    bev.segments = 3

    # Steps
    step_w = settings.hero_wall_width / 2.0
    step_d = 3.0
    step_h = 0.45
    step_y = 8.0
    for i in range(3):
        bpy.ops.mesh.primitive_cube_add(location=(0, step_y + i * 1.0, (i * step_h) / 2 + 0.15))
        step = context.active_object
        step.name = f"Step_0{i+1}"
        step.scale = (step_w / 2, step_d / 2, step_h / 2)
        _link_object(step, architecture)

    # Platform
    bpy.ops.mesh.primitive_cube_add(location=(0, 13.0, 1.0))
    platform = context.active_object
    platform.name = "Platform_Main"
    platform.scale = (7.0, 3.8, 0.7)
    _link_object(platform, architecture)

    # Hero wall
    bpy.ops.mesh.primitive_cube_add(location=(0, 22.0, 7.5))
    wall = context.active_object
    wall.name = "Hero_Wall"
    wall.scale = (settings.hero_wall_width / 2, 0.6, settings.hero_wall_height / 2)
    _link_object(wall, architecture)

    bpy.ops.mesh.primitive_cube_add(location=(0, 21.45, 7.5))
    frame = context.active_object
    frame.name = "Hero_Wall_Frame"
    frame.scale = (settings.hero_wall_width * 0.37, 0.15, settings.hero_wall_height * 0.36)
    _link_object(frame, architecture)

    # Four pillars
    pillar_positions = [(-7.5, 9.0), (7.5, 9.0), (-7.5, 17.0), (7.5, 17.0)]
    for idx, (x, y) in enumerate(pillar_positions, start=1):
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=settings.pillar_radius, depth=settings.pillar_height, location=(x, y, settings.pillar_height / 2))
        pillar = context.active_object
        pillar.name = f"Pillar_{idx:02d}"
        _link_object(pillar, architecture)
        bev = pillar.modifiers.new(name="Bevel", type='BEVEL')
        bev.width = 0.06
        bev.segments = 3

        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=settings.pillar_radius * 1.25, depth=0.35, location=(x, y, 0.175))
        base = context.active_object
        base.name = f"Pillar_{idx:02d}_Base"
        _link_object(base, architecture)

        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=settings.pillar_radius * 1.12, depth=0.35, location=(x, y, settings.pillar_height + 0.175))
        cap = context.active_object
        cap.name = f"Pillar_{idx:02d}_Cap"
        _link_object(cap, architecture)

    # Camera
    cam_data = bpy.data.cameras.new("Camera_Master")
    cam_obj = bpy.data.objects.new("Camera_Master", cam_data)
    cam_obj.location = (0.0, -28.0, 3.2)
    cam_obj.rotation_euler = (radians(82.0), 0.0, 0.0)
    cam_data.lens = 50
    cam_data.clip_start = 0.1
    cam_data.clip_end = 1000.0
    cameras.objects.link(cam_obj)
    scene.camera = cam_obj

    # Lighting
    sun_data = bpy.data.lights.new("Sun_Moon", type='SUN')
    sun_data.energy = 1.2
    sun_obj = bpy.data.objects.new("Sun_Moon", sun_data)
    sun_obj.rotation_euler = (radians(55.0), 0.0, radians(-35.0))
    lighting.objects.link(sun_obj)

    area_data = bpy.data.lights.new("Divine_Backlight", type='AREA')
    area_data.energy = 250.0
    area_data.shape = 'RECTANGLE'
    area_data.size = 6.0
    area_data.size_y = 6.0
    area_obj = bpy.data.objects.new("Divine_Backlight", area_data)
    area_obj.location = (0.0, 24.0, 10.0)
    area_obj.rotation_euler = (radians(-90.0), 0.0, radians(180.0))
    lighting.objects.link(area_obj)

    # Fog placeholder
    bpy.ops.mesh.primitive_cube_add(location=(0, 8, 3))
    fog = context.active_object
    fog.name = "Fog_Volume"
    fog.scale = (18, 22, 6)
    _link_object(fog, fx)
    fog.display_type = 'WIRE'

    # Assign procedural materials
    mats = create_material_library()
    granite = mats["SKM_Granite"]
    for obj in [floor, platform, wall, frame] + [o for o in architecture.objects if o.name.startswith("Step_") or o.name.startswith("Pillar_")]:
        _apply_material(obj, granite)

    return {
        "architecture": architecture.name,
        "cameras": cameras.name,
        "lighting": lighting.name,
        "fx": fx.name,
    }


def create_materials(context):
    return list(create_material_library().keys())


def setup_lighting(context):
    scene = context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    if hasattr(scene.cycles, "samples"):
        scene.cycles.samples = 128
    if hasattr(scene.cycles, "preview_samples"):
        scene.cycles.preview_samples = 32
    if scene.world is None:
        scene.world = bpy.data.worlds.new("SKM_World")
    world = scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.015, 0.015, 0.02, 1.0)
        bg.inputs[1].default_value = 0.08
    return True


def setup_camera(context):
    scene = context.scene
    cam = scene.camera
    if cam is None:
        cam_data = bpy.data.cameras.new("Camera_Master")
        cam = bpy.data.objects.new("Camera_Master", cam_data)
        context.collection.objects.link(cam)
        scene.camera = cam
    cam.location = (0.0, -28.0, 3.2)
    cam.rotation_euler = (radians(82.0), 0.0, 0.0)
    cam.data.lens = 50
    cam.data.clip_start = 0.1
    cam.data.clip_end = 1000.0
    return cam.name


def generate_complete_scene(context):
    create_architecture(context)
    create_materials(context)
    setup_lighting(context)
    setup_camera(context)
    return True
