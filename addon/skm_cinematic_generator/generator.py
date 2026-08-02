import bpy
from math import radians
from mathutils import Vector


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


def _new_material(name, base_color=(0.2, 0.2, 0.2, 1.0), roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs[0].default_value = base_color
        bsdf.inputs[7].default_value = roughness
        bsdf.inputs[6].default_value = metallic
    return mat


def _apply_material(obj, mat):
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
    reference = _ensure_collection("Reference", root)

    scene = context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    if hasattr(scene.cycles, "preview_samples"):
        scene.cycles.preview_samples = 32
    if hasattr(scene.cycles, "samples"):
        scene.cycles.samples = 128
    if hasattr(scene, "display_settings"):
        try:
            scene.view_settings.look = 'Filmic'
        except Exception:
            pass

    # Floor
    bpy.ops.mesh.primitive_plane_add(size=settings.sanctum_size, location=(0, 0, 0))
    floor = context.active_object
    floor.name = "Ground_Main"
    floor.scale = (1, 1, 1)
    _link_object(floor, architecture)
    solid = floor.modifiers.new(name="Solidify", type='SOLIDIFY')
    solid.thickness = 0.4
    bev = floor.modifiers.new(name="Bevel", type='BEVEL')
    bev.width = 0.04
    bev.segments = 3

    # Steps
    step_w = 12.0
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
    platform.scale = (7.0, 4.0, 0.7)
    _link_object(platform, architecture)

    # Hero wall frame
    bpy.ops.mesh.primitive_cube_add(location=(0, 22.0, 7.5))
    wall = context.active_object
    wall.name = "Hero_Wall"
    wall.scale = (11.5, 0.6, 8.0)
    _link_object(wall, architecture)

    # Inner recessed frame
    bpy.ops.mesh.primitive_cube_add(location=(0, 21.45, 7.5))
    frame = context.active_object
    frame.name = "Hero_Wall_Frame"
    frame.scale = (8.5, 0.15, 5.8)
    _link_object(frame, architecture)

    # Pillars front
    pillar_positions = [(-7.5, 9.0), (7.5, 9.0), (-7.5, 17.0), (7.5, 17.0)]
    for idx, (x, y) in enumerate(pillar_positions, start=1):
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=settings.pillar_radius, depth=settings.pillar_height, location=(x, y, settings.pillar_height / 2))
        pillar = context.active_object
        pillar.name = f"Pillar_{idx:02d}"
        bev = pillar.modifiers.new(name="Bevel", type='BEVEL')
        bev.width = 0.06
        bev.segments = 3
        _link_object(pillar, architecture)

        # simple base and cap
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=settings.pillar_radius * 1.2, depth=0.35, location=(x, y, 0.175))
        base = context.active_object
        base.name = f"Pillar_{idx:02d}_Base"
        _link_object(base, architecture)

        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=settings.pillar_radius * 1.12, depth=0.35, location=(x, y, settings.pillar_height + 0.175))
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

    # Materials
    granite = _new_material("SKM_Granite", (0.06, 0.06, 0.07, 1.0), roughness=0.9, metallic=0.0)
    bronze = _new_material("SKM_Bronze", (0.34, 0.22, 0.12, 1.0), roughness=0.45, metallic=1.0)
    for obj in [floor, step for step in []]:
        pass

    for obj in [floor, platform, wall, frame] + [o for o in architecture.objects if o.name.startswith("Step_") or o.name.startswith("Pillar_")]:
        if obj.type == 'MESH':
            _apply_material(obj, granite)

    # Set active scene frame / unit scale defaults
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0

    return {
        "architecture": architecture.name,
        "cameras": cameras.name,
        "lighting": lighting.name,
        "fx": fx.name,
        "reference": reference.name,
    }


def create_materials(context):
    granite = _new_material("SKM_Granite", (0.06, 0.06, 0.07, 1.0), roughness=0.9, metallic=0.0)
    bronze = _new_material("SKM_Bronze", (0.34, 0.22, 0.12, 1.0), roughness=0.45, metallic=1.0)
    gold = _new_material("SKM_Gold", (0.9, 0.78, 0.35, 1.0), roughness=0.3, metallic=1.0)
    sandstone = _new_material("SKM_Sandstone", (0.35, 0.28, 0.20, 1.0), roughness=0.85, metallic=0.0)
    return [granite.name, bronze.name, gold.name, sandstone.name]


def setup_lighting(context):
    scene = context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    if hasattr(scene.cycles, "samples"):
        scene.cycles.samples = 128
    if hasattr(scene.cycles, "preview_samples"):
        scene.cycles.preview_samples = 32
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
