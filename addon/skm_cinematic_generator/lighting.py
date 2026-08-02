import bpy
from math import radians


LIGHT_SPECS = {
    "Sun_Moon": {
        "type": "SUN",
        "energy": 1.2,
        "rotation": (radians(55.0), 0.0, radians(-35.0)),
    },
    "Divine_Backlight": {
        "type": "AREA",
        "energy": 250.0,
        "location": (0.0, 24.0, 10.0),
        "rotation": (radians(-90.0), 0.0, radians(180.0)),
        "size": 6.0,
    },
}


def setup_world(scene=None):
    if scene is None:
        scene = bpy.context.scene
    world = scene.world
    if world is None:
        world = bpy.data.worlds.new("SKM_World")
        scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    bg = nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.015, 0.015, 0.02, 1.0)
        bg.inputs[1].default_value = 0.08
    return world


def ensure_light(name, light_type):
    light_obj = bpy.data.objects.get(name)
    if light_obj and light_obj.type == 'LIGHT':
        return light_obj
    light_data = bpy.data.lights.new(name, type=light_type)
    light_obj = bpy.data.objects.new(name, light_data)
    bpy.context.scene.collection.objects.link(light_obj)
    return light_obj


def setup_lights(scene=None):
    if scene is None:
        scene = bpy.context.scene
    setup_world(scene)
    for name, spec in LIGHT_SPECS.items():
        light_obj = ensure_light(name, spec["type"])
        light_data = light_obj.data
        light_data.energy = spec["energy"]
        if spec["type"] == "AREA":
            light_data.shape = 'RECTANGLE'
            light_data.size = spec["size"]
            light_data.size_y = spec["size"]
            light_obj.location = spec["location"]
        light_obj.rotation_euler = spec["rotation"]
    return True
