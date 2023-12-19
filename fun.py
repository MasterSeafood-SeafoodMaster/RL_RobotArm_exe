import bpy
import numpy as np
import math
import random
import os

def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()
    l1=math.Vector(point)
    l2=math.Vector(loc_camera)

    direction = l1-l2
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()


class Render:
    def __init__(self):
        ## Scene information
        # Define the scene information
        self.scene = bpy.data.scenes['Scene']
        # Define the information relevant to the <bpy.data.objects>
        self.camera = bpy.data.objects['Camera']

        self.axis = bpy.data.objects['Axis']
        self.light_1 = bpy.data.objects['Light0']
        self.light_2 = bpy.data.objects['Light1']
        
        self.shelf = bpy.data.objects['shelf_c']
        self.table = bpy.data.objects['table_c']
        
        self.boxes=[]
        for i in range(9):
            r=bpy.data.objects['b'+str(i)]
            self.boxes.append(r)

        self.images_filepath = 'C:/Users/cfouo/Desktop/yolov8/dataset/images'
        self.labels_filepath = 'C:/Users/cfouo/Desktop/yolov8/dataset/labels'

    def set_camera(self):
        self.axis.rotation_euler = (0, 0, 0)
        self.axis.location = (0, 0, 0)
        #self.camera.location = (0, 0, 0.05)

    
    def save_img(self, file_name):
        bpy.context.scene.render.filepath = os.path.join(self.images_filepath, file_name)
        bpy.ops.render.render(write_still = True)
        
    def camera_view_bounds_2d(self, mesh_object):
        scene=self.scene
        camera_object=self.camera
        matrix = camera_object.matrix_world.normalized().inverted()
        dg = bpy.context.evaluated_depsgraph_get()
        ob = mesh_object.evaluated_get(dg) #this gives us the evaluated version of the object. Aka with all modifiers and deformations applied.
        mesh = ob.to_mesh()
        #mesh = mesh_object.to_mesh(scene, True, 'RENDER')
        mesh.transform(mesh_object.matrix_world)
        mesh.transform(matrix)
        frame = [-v for v in camera_object.data.view_frame(scene=scene)[:3]]

        lx = []
        ly = []

        for v in mesh.vertices:
            co_local = v.co
            z = -co_local.z

            if z <= 0.0:
                continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

            min_x, max_x = frame[1].x, frame[2].x
            min_y, max_y = frame[0].y, frame[1].y

            x = (co_local.x - min_x) / (max_x - min_x)
            y = (co_local.y - min_y) / (max_y - min_y)

            lx.append(x)
            ly.append(y)
        
        mesh_object.to_mesh_clear()

        if not lx or not ly:
            #print(lx, ly)
            return None

        min_x = np.clip(min(lx), 0.0, 1.0)
        min_y = np.clip(min(ly), 0.0, 1.0)
        max_x = np.clip(max(lx), 0.0, 1.0)
        max_y = np.clip(max(ly), 0.0, 1.0)

        if min_x == max_x or min_y == max_y:
            #print(lx, ly)
            #print(min_x, max_x, min_y, max_y)
            return None

        render = scene.render
        fac = render.resolution_percentage * 0.01
        dim_x = render.resolution_x * fac
        dim_y = render.resolution_y * fac
        
        min_x = int(min_x*640)
        min_y = int(480-min_y*480)
        max_x = int(max_x*640)
        max_y = int(480-max_y*480)
        min_y, max_y = max_y, min_y
        
        
        return (min_x, min_y, max_x, max_y)
    
    def save_txt(self, file_name):
        
        fn=os.path.join(self.labels_filepath, file_name)
        fs=""
        for b in self.boxes:
            xyxy=self.camera_view_bounds_2d(b)
            if xyxy:
                min_x, min_y, max_x, max_y=xyxy
                xc=(min_x+max_x)/(2*640)
                yc=(min_y+max_y)/(2*480)
                yw=(max_x-min_x)/640
                yh=(max_y-min_y)/480                
                
                s=f'0 {xc} {yc} {yw} {yh}\n'
                fs+=s
                
        with open(fn, 'w') as file: pass
        if len(fs): 
            with open(fn, 'a') as file: file.write(fs)


if __name__ == '__main__':
    r = Render()
    r.set_camera()
    r.shelf.location = (0, 0, 10)
    
    for i in range(100):
        r.light_1.data.energy = random.randint(0, 100)
        r.light_2.data.energy = random.randint(0, 100)
        
        angle = random.uniform(0, 360)
        x = 0.2 * math.cos(math.radians(angle))
        y = 0.2 * math.sin(math.radians(angle))
        
        #r.axis.rotation_euler = (0, 0, math.radians(90+angle))
        r.axis.location = (x, y, 0)
        
        
        look_at(r.camera, (0, 0, 0))
        
        In=f"cube{i}.jpg"
        Tn=f"cube{i}.txt"
        r.save_img(In)
        r.save_txt(Tn)    
        print(i)
    