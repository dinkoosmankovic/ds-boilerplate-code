from .model import Model
import numpy as np

import trimesh
import trimesh.transformations as transforms
import pyrender
import time

class StupidBox(Model):
    def __init__(self) -> None:
        Model.__init__(self)
        self.scene = None
        self.state = 0
        self.__build_model()
        
    def __get_node_by_name(self, name):
        if name is None:
            return None
        
        for n in self.scene.nodes:
            if n.name == name:
                return n
            
    def __compose_transform_matrix(self, translation, rotation):
        M = rotation
        M[0:3, 3] = translation[0:3, 3]
        return M
        
            

    def __build_model(self):
        self.scene = pyrender.Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]))
                
        plane = trimesh.creation.box(extents=np.array([5, 5, 0.001]))
        plane.visual.face_colors = np.array([0.5, 0.5, 0.5, 0.5])
        plane_mesh = pyrender.Mesh.from_trimesh(plane, smooth=False)
        
        self.scene.add_node(
            pyrender.Node(name="plane", mesh=plane_mesh)
        )
        
        axis = trimesh.creation.axis(origin_color=[1., 0, 0])
        axis_mesh = pyrender.Mesh.from_trimesh(axis, smooth=False)
        
        self.scene.add_node(
            pyrender.Node(name="axis", mesh=axis_mesh)
        )
        
        box_1 = trimesh.creation.box(extents=np.array([0.3, 0.3, 0.5]))
        box_1.visual.face_colors = np.array([0, 1., 0, 0.8])
        box_1_mesh = pyrender.Mesh.from_trimesh(box_1, smooth=False)
        box_1_translation = transforms.translation_matrix(np.array([0.5, 1.2, 0.25 + 0.001]))
        box_1_rotation = transforms.rotation_matrix(np.pi/3, [0, 0, 1], box_1_mesh.centroid)
        
        box_1_matrix = self.__compose_transform_matrix(box_1_translation, box_1_rotation)
        
        self.scene.add_node(
            pyrender.Node(name="box_1", mesh=box_1_mesh, matrix=box_1_matrix)
        )
        
        box_2 = trimesh.creation.box(extents=np.array([0.05, 0.05, 0.2]))
        box_2.visual.face_colors = np.array([1., 0, 0, 0.6])
        box_2_mesh = pyrender.Mesh.from_trimesh(box_2, smooth=False)
        
        box_2_translation = transforms.translation_matrix(np.array([0, 0, 0.1 + 0.25]))
        box_2_rotation = transforms.rotation_matrix(3*np.pi/4, [0, 0, 1], box_2_mesh.centroid)
        
        box_2_matrix = np.matmul(self.__get_node_by_name("box_1").matrix, self.__compose_transform_matrix(box_2_translation, box_2_rotation))
        
        self.scene.add_node(
            pyrender.Node(name="box_2", mesh=box_2_mesh, matrix=box_2_matrix)
        )
        
        box_3 = trimesh.creation.box(extents=np.array([0.6, 0.05, 0.05]))
        box_3.visual.face_colors = np.array([0, 0, 1., 0.6])
        box_3_mesh = pyrender.Mesh.from_trimesh(box_3, smooth=False)
        
        box_3_translation = transforms.translation_matrix(np.array([0, 0, 0.1 + 0.025]))
        box_3_rotation = transforms.rotation_matrix(self.state, [0, 0, 1], box_3_mesh.centroid)
        
        box_3_matrix = np.matmul(self.__get_node_by_name("box_2").matrix, self.__compose_transform_matrix(box_3_translation, box_3_rotation))
        
        self.scene.add_node(
            pyrender.Node(name="box_3", mesh=box_3_mesh, matrix=box_3_matrix)
        )       

        

    def show_box(self):
        v = pyrender.Viewer(self.scene, use_raymond_lighting=True)

    def integrate(self, final_time=10, dt=0.1) -> None:
        v = pyrender.Viewer(self.scene, run_in_thread=True,
                            use_raymond_lighting=True)
        t = 0
        while v.is_active or t < final_time:
            self.step(u=0.1, dt=dt)
            v.render_lock.acquire()
            self.__update_model()
            v.render_lock.release()
            t += dt
            time.sleep(dt)
            

    def step(self, u=0, dt=0.1):
        self.state += u
        
    def __update_model(self):
        origin = self.__get_node_by_name("box_3").mesh.centroid
        box_3_translation = transforms.translation_matrix(np.array([0, 0, 0.1 + 0.025]))
        box_3_rotation = transforms.rotation_matrix(self.state, [0, 0, 1], origin)
        
        box_3_matrix = np.matmul(self.__get_node_by_name("box_2").matrix, self.__compose_transform_matrix(box_3_translation, box_3_rotation))
        self.__get_node_by_name("box_3").matrix = box_3_matrix
        
        

    def show_model(self) -> None:
        pass