import bpy
import bmesh
import numpy as np
import os

def go():
    bpy.ops.object.select_all()
    bpy.ops.object.delete()
    #data = np.loadtxt('C:/Users/dylan/Documents/Python Scripts/Mazes/txtfiles.txt', delimiter=' ', dtype=str)
    data = np.loadtxt('C:/Users/dylan/Documents/Python Scripts/Mazes/txtfile.txt', delimiter=' ', dtype=str)
    print(data)
    data = data.astype(dtype=int)
    x = 0
    for row in range(0, data.shape[0]):
        for col in range(0, data.shape[1]):
            if data[row, col] == 1:
                x+=1
                bpy.ops.mesh.primitive_cube_add(size=1, location=(row, 0, col))
                bpy.ops.transform.resize(value=(1, 2, 1))                
             
    bpy.ops.object.select_all()
    try:
        for obj in bpy.data.collections['Maze'].all_objects : obj.select_set(False)
    except (KeyError):
        print('no collection named Maze')
    bpy.ops.object.delete()
    files = os.listdir('C:/Users/dylan/Documents/Python Scripts/Mazes/3D')
    file_count = len(files) + 1
    string = 'C:/Users/dylan/Documents/Python Scripts/Mazes/3D/maze' + str(file_count) + '.obj'
    target_file = os.path.join('C:/Users/dylan/Documents/Python Scripts/Mazes/3D/', string)

    bpy.ops.export_scene.obj(filepath=target_file)   