import bpy


def setup_world():
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    world=scene.world or bpy.data.worlds.new('World')
    scene.world=world
    world.use_nodes=True
    bg=world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs[0].default_value=(0.01,0.01,0.02,1.0)
        bg.inputs[1].default_value=0.15
    return world


def create_basic_lights():
    return setup_world()
