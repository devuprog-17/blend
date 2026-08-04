from .utils import new_principled_material


MATERIAL_SPECS = {
    "SKM_Granite": {
        "base_color": (0.06, 0.06, 0.07, 1.0),
        "roughness": 0.92,
        "metallic": 0.0,
    },
    "SKM_Sandstone": {
        "base_color": (0.32, 0.27, 0.20, 1.0),
        "roughness": 0.88,
        "metallic": 0.0,
    },
    "SKM_Bronze": {
        "base_color": (0.35, 0.22, 0.12, 1.0),
        "roughness": 0.48,
        "metallic": 1.0,
    },
    "SKM_Gold": {
        "base_color": (0.92, 0.78, 0.35, 1.0),
        "roughness": 0.28,
        "metallic": 1.0,
    },
    "SKM_Ember": {
        "base_color": (0.70, 0.25, 0.06, 1.0),
        "roughness": 0.55,
        "metallic": 0.0,
    },
}


def create_material_library():
    mats = {}
    for name, spec in MATERIAL_SPECS.items():
        mats[name] = new_principled_material(
            name,
            base_color=spec["base_color"],
            roughness=spec["roughness"],
            metallic=spec["metallic"],
        )
    return mats


def get_material(name):
    mats = create_material_library()
    return mats.get(name)
