import bpy
from math import radians

from .config import DEFAULT_CONFIG
from .utils import ensure_world, set_world_background


LIGHT_SPECS = {
    "Sun_Moon": {
        "type": "SUN",
        "energy": DEFAULT_CONFIG.sun_energy,
        "rotation": (radians(55.0), 0.0, radians(-35.0)),
    },
    "Divine_Backlight": {
        "type": "AREA",
        "energy": DEFAULT_CONFIG.area_energy,
        "location": (0.0, 24.0, 10.0),
        "rotation": (radians(-90.0), 0.0, radians(180.0)),
        "size": DEFAULT_CONFIG.area_size,
    },
}


def setup_world(scene=None):
    scene = scene or bpy.context.scene
    ensure_world(scene)
    set_world_background(scene, DEFAULT_CONFIG.world_color, DEFAULT_CONFIG.world_strength)
    return scene.world


def ensure_light(name, light_type):
    light_obj = bpy.data.objects.get(name)
    if light_obj and light_obj.type == 'LIGHT':
        return light_obj
    light_data = bpy.data.lights.new(name, type=light_type)
    light_obj = bpy.data.objects.new(name, light_data)
    bpy.context.scene.collection.objects.link(light_obj)
    return light_obj


def setup_lights(scene=None):
    scene = scene or bpy.context.scene
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
