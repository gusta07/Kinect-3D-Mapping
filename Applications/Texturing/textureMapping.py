import cv2
import numpy as np



class TextureTool:
    """Textures the 3D surface (.obj file).

    Maps the different pictures taken during the 3D scan to the 3D surface.
    Reads the different matrices used to map a 3D point to its corresponding 2D point.

    Attributes:
        rt_kinect: list containing the different Kinect coordinates.
        intrinsics: matrix containing the intrinsics parameters.
        relative_rotation: matrix containing the relative rotation between the kinect and the external camera.
        relative_translation: matrix containing the relative translation between the kinect and the external camera.
        RT: rotation|translation matrix describing the transformation between the Kinect and the external camera.
        

        The following variables are used to construct the textured .obj file.
        surface_file_name: the .obj file name.
        vertices_index: index of the current vertice being treated.
        uv_index: index of the current (u,v) coordinate being treated.
        uv_texture_coordinates: contains the (u,v) coordinates.
        face_definitions: contains the face definitions.
        vertices_coordinates: contains the vertices coordinates.
        normals_coordinates: contains the normals coordinates.
        index_number_of_vertices: used to obtain the right number of vertices per face.

    """

    def __init__(self):
        """class constructor, initializes the different matrices and parameters"""
        self._init_matrices()
        self._compute_RT()
        self._init_file_content()

    def _init_matrices(self):
        """initializes the different matrices"""
        self._RT_kinect = np.loadtxt("Coordinates/coordinates0.txt")
        self._intrinsics = np.matrix(cv2.cv.Load("../Matrices/Intrinsics-Webcam.xml"))
        self._relative_rotation = np.load("../Matrices/rotation.npy")
        self._relative_translation = np.load("../Matrices/translation.npy")

        
           

    def _compute_RT(self):
        """computes the RT matrix describing the relative transformation between the Kinect and the external camera"""
        RT_relative = np.append(self._relative_rotation,self._relative_translation, axis=1)#append R and T together
        homogeneous = np.matrix("0,0,0,1")   
        RT_relative = np.append(RT_relative, homogeneous, axis = 0)
        self._RT_kinect = np.append(self._RT_kinect, homogeneous, axis = 0) 
        self._RT = RT_relative * self._RT_kinect
        self._RT = np.delete(self._RT,3,0)#delete homogenous (for further computations)
        self._RT_kinect = np.delete(self._RT_kinect,3,0)    

    def _init_file_content(self):
        """initializes the different strings constituing the textured output file."""
        self._surface_file_name = "surface.obj"
        self._vertices_index = 0
        self._uv_index = 0
        self._uv_texture_coordinates = []   #vt
        self._face_definitions = []         #f
        self._vertices_coordinates = []     #v
        self._normals_coordinates = []      #vn

        self._index_number_of_vertices = 0

        #read the number of pictures taken
        self._set_number_of_pictures()
        #create a dictionnary that will map each coordinates/picture to a list of face definitions
        from collections import defaultdict
        self._face_definitions_dictionnary = defaultdict(list)
        #list containing the faces without texture
        self._faces_without_texture = []
    
    def _process_file(self, file_to_process):
        """load the file data in different list to accelerate further computations"""
        for line in file_to_process:
            if line.startswith('v '):
                line = line.lstrip("v ").rstrip("\n")#delete first 'v' and last \n
                self._vertices_coordinates.append(np.matrix(map(float,line.split())))
            if line.startswith('vn '):
                self._normals_coordinates.append(line)

    def _set_number_of_pictures(self):
        """get the number of pictures taken"""
        with open('Coordinates/configuration.txt') as config_file:
            self._number_of_pictures = int(config_file.readline())
                         

    def texture_object(self):
        """textures the 3D surface with the pictures."""
        surface_file = open(self._surface_file_name)
        face = "\nf "
        print "starting the texture mapping, please wait..."
        

        import time
        start = time.time()

        self._process_file(surface_file)


        for i in range(self._number_of_pictures):
            print i
            self._RT_kinect = np.loadtxt("Coordinates/coordinates" + str(i) + ".txt")
            self._compute_RT()
                
            self._vertices_index = 0
        
            for coordinates in self._vertices_coordinates:
                self._vertices_index += 1
                #(u,v,1) computation
                XYZ = np.append(coordinates,np.matrix(1),axis = 1)


                    
                temp_result = self._RT * XYZ.T
                temp_result = self._intrinsics * temp_result
                uv = temp_result / temp_result[2] #to get 1 in (u,v,1)
                

                #if (u,v,1) is in the good range
                if uv[0] >= 0 and uv[0] <= 640 and uv[1] >= 0 and uv[1] <= 480:
                    #normalize
                    u = str(uv[0] / 640).strip('[]')#get rid of the brackets
                    v = str(uv[1] / 480).strip('[]')

                        
                    self._uv_index += 1
                    self._uv_texture_coordinates.append("vt " + u + " " + v + "\n")
                        
                    face += str(self._vertices_index) + "/" + str(self._uv_index) + "/" + str(self._vertices_index) + " " 
                    self._index_number_of_vertices += 1 

                      
                    
                    if self._index_number_of_vertices % 3 == 0:
                        #create the face to delete
                        face_to_delete = "\nf " + str(self._vertices_index-2) + "//" + str(self._vertices_index-2) + " " + str(self._vertices_index-1) + "//" + str(self._vertices_index-1) + " " + str(self._vertices_index) + "//" + str(self._vertices_index) + " "
                        


                        if i > 0:
                            try:
                                self._faces_without_texture.remove(face_to_delete)
                            except ValueError:
                                pass  # do nothing!
                        
                            
                        

                        
                        self._face_definitions_dictionnary[i].append(face)
                        face = "\nf "  
                        

                else:
                    face += str(self._vertices_index) + "//" + str(self._vertices_index) + " "
                    self._index_number_of_vertices += 1 
                    if self._index_number_of_vertices % 3 == 0:
                        if i < 1:#if i >= 1 , that face has already been treated at least once
                            self._faces_without_texture.append(face)
                        face = "\nf "  
                            

                    


                
            

            
                    

        surface_file.close()


        #create textured .obj file
        self._create_textured_file()
        print "done!"
        end = time.time()
        print (end - start) / 60

    def _create_textured_file(self):
        """write all the data in the final textured file"""
        Textured_Mesh = open("textured_surface.obj","w")
        Textured_Mesh.write("mtllib texture.mtl\n")

        for line in self._vertices_coordinates:
            Textured_Mesh.write("v " + str(line).strip('[]') + '\n')
        for line in self._uv_texture_coordinates:
            Textured_Mesh.write(line)
        for line in self._normals_coordinates:
            Textured_Mesh.write(line)

        for line in self._faces_without_texture:
            Textured_Mesh.write(line)

        for i in range(self._number_of_pictures):
            Textured_Mesh.write("\nusemtl texture" + str(i) + "\n")
        
            for line in self._face_definitions_dictionnary[i]:
                Textured_Mesh.write(line)

        Textured_Mesh.close()




test = TextureTool()
test.texture_object()


