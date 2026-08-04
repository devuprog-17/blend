import bpy


def ensure_collection(name, parent=None):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        if parent is None:
            bpy.context.scene.collection.children.link(coll)
        else:
            parent.children.link(coll)
    return coll


def link_object_to_collection(obj, collection):
    if obj.name not in collection.objects:
        collection.objects.link(obj)
    for c in list(obj.users_collection):
        if c != collection:
            c.objects.unlink(obj)


def remove_unused_data_blocks():
    for collection in (bpy.data.meshes, bpy.data.lights, bpy.data.cameras, bpy.data.materials, bpy.data.curves):
        for block in list(collection):
            if block.users == 0:
                collection.remove(block)


def clear_scene_objects():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    remove_unused_data_blocks()


def new_principled_material(name, base_color=(0.2, 0.2, 0.2, 1.0), roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs[0].default_value = base_color
        bsdf.inputs[6].default_value = metallic
        bsdf.inputs[7].default_value = roughness
    return mat


def apply_material(obj, mat):
    if obj.type != 'MESH':
        return
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
