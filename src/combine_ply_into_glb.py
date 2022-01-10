# exports each selected object into its own file

import bpy
import os

print(f" bpy = {bpy}")

def delete_all_mesh():
    # Select objects by type
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            o.select_set(True)
        else:
            o.select_set(False)

    # Call the operator only once
    bpy.ops.object.delete()

def run(bloat):

    print(f"running with bloat = {bloat}")

    files = """
    data_rgb_0_to_10_color.ply
    data_rgb_10_to_20_color.ply
    data_rgb_20_to_30_color.ply
    data_rgb_30_to_40_color.ply
    data_rgb_40_to_50_color.ply
    data_rgb_50_to_60_color.ply
    data_rgb_60_to_70_color.ply
    data_rgb_70_to_80_color.ply
    data_rgb_80_to_90_color.ply
    data_rgb_90_to_100_color.ply
    """.split();

    for f in files:
        fp = f"data_b{bloat}/{f}"
        bpy.ops.import_mesh.ply(filepath=fp)


    # Save and re-open the file to clean up the data blocks
    #bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    #bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)
    bpy.ops.export_scene.gltf(filepath=f"models/rgb_b{bloat}.glb", export_draco_mesh_compression_enable=True,export_draco_color_quantization=0,export_colors=True)


if __name__ == '__main__':

    for bloat in "0 1 2 5".split():
        #bpy.ops.wm.window_close()
        bpy.ops.wm.window_new_main()
        delete_all_mesh()
        run(bloat)


    bpy.ops.wm.quit_blender()

