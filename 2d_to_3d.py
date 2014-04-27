bl_info = {
 "name": "2D to 3D",
 "author": "Anthony Lefebvre (Wotte)",
 "version": (0, 1),
 "blender": (2, 5, 9),
 "location": "View3D > Object > 2D to 3D",
 "description": "Convert 2D images to 3D",
 "warning": "",
 "wiki_url": "",
 "tracker_url": "",
 "category": "Object"}
#### Import module ####
import time
from PIL import Image
import bpy
import bmesh
from math import floor

############################################################################################
# Class for create the 3d object                                                           #
class create_object():
        def __init__(self,dir_front,dir_profil,RGB,rad):
            self.dir_front = dir_front
            self.dir_profil = dir_profil
            self.RGB = RGB
            self.rad = rad
            self.font = (self.RGB[0],self.RGB[1],self.RGB[2])
            self.im1 = Image.open(r'{}'.format(self.dir_front))
            self.im2 = Image.open(r'{}'.format(self.dir_profil))
            self.largeur, self.hauteur = self.im1.size
            self.largeur2, self.hauteur2 = self.im2.size
            self.imageBord1=Image.new( "RGB" ,(self.largeur+2, self.hauteur+2))
            self.imageBord2=Image.new( "RGB" ,(self.largeur2+2, self.hauteur2+2))
            #########Create edge for image##########
            #Front Image
            for y in range (self.hauteur) :
                for x in range (self.largeur) :
                    p1=self.im1.getpixel((x,y))
                    self.imageBord1.putpixel((x+1 , y+1 ) ,p1)
            for x in range(self.largeur+2):
                self.imageBord1.putpixel((x,0),self.font)
            for x in range(self.largeur+2):
                self.imageBord1.putpixel((x,self.hauteur+1),self.font)
            for y in range(self.hauteur+2):
                self.imageBord1.putpixel((0,y),self.font)
            for y in range(self.hauteur+2):
                self.imageBord1.putpixel((self.largeur+1,y),self.font)
            
            #Profil Image
            for y in range (self.hauteur2) :
                for x in range (self.largeur2) :
                    p2=self.im2.getpixel((x,y))
                    self.imageBord2.putpixel((x+1 , y+1 ) ,p2)
            for x in range(self.largeur2+2):
                self.imageBord2.putpixel((x,0),self.font)
            for x in range(self.largeur2+2):
                self.imageBord2.putpixel((x,self.hauteur2+1),self.font)
            for y in range(self.hauteur2+2):
                self.imageBord2.putpixel((0,y),self.font)
            for y in range(self.hauteur2+2):
                self.imageBord2.putpixel((self.largeur2+1,y),self.font)
            ##############End of create edge##################
            self.nbpos = 8*self.rad
        
            self.mylayers = [False]*20
            self.mylayers[0] = True
            self.listNumPixX2 = range(0,self.largeur2+2)
            self.listNumPixX = range(0,self.largeur+2)
            self.listNumPixY = range(0,self.hauteur+2)
            self.numPix1 = 0
            self.numPixMax1 = (self.hauteur+2)*(self.largeur+2)
            self.couleurPix1 = self.imageBord1.load()
            self.couleurPix2 = self.imageBord2.load()
            self.add_cube = bpy.ops.mesh.primitive_cube_add
            self.contour = False
            self.ok = False
            self.ok2 = False
            self.ok3 = True
            self.first = False
            font = self.font
            global font
        def contour2(self,y1,x1):
            listNumPixX2 = self.listNumPixX2
            couleurPix2 = self.couleurPix2
            contour = self.contour
            couleurPix1 = self.couleurPix1
            nbpos = self.nbpos
            rad = self.rad
            self.first = True
            for h in listNumPixX2:
                if couleurPix2[h,y1] == font:
                    pass
                elif contour == True:
                    self.add_cube(radius=rad,location=(((x1-(x1-1))+(nbpos/4)*x1), ((h-(h-1))+(nbpos/4)*h), ((y1-(y1-1))+(nbpos/4)*y1)), layers=self.mylayers)
                    self.ok = True
                elif couleurPix2[h+1,y1] == font or couleurPix2[h-1,y1] == font or couleurPix2[h,y1+1] == font or couleurPix2[h,y1-1] == font:
                    self.add_cube(radius=rad,location=(((x1-(x1-1))+(nbpos/4)*x1), ((h-(h-1))+(nbpos/4)*h), ((y1-(y1-1))+(nbpos/4)*y1)), layers=self.mylayers)
                    self.ok = True
                else:
                    pass
                if self.ok == True:
                        colorP = ( round(((couleurPix2[h,y1][0])/255),4),round(((couleurPix2[h,y1][1])/255),4),round(((couleurPix2[h,y1][2])/255),4) )
                        colorF = ( round(((couleurPix1[x1,y1][0])/255),4),round(((couleurPix1[x1,y1][1])/255),4),round(((couleurPix1[x1,y1][2])/255),4) )
                        if len(bpy.data.materials.values()) == 0:
                            mat = bpy.data.materials.new('Material')
                            if self.first == True:
                                    print('ok')
                                    mat.diffuse_color = colorF
                                    
                            else:
                                    mat.diffuse_color = colorP
                            bpy.context.object.data.materials.append(mat)
                            self.first = False
                        else:
                            if self.first == True :
                                    print('ok')
                                    for m in bpy.data.materials:
                                
                                        R = round(m.diffuse_color.r ,4)
                                        G = round(m.diffuse_color.g ,4)
                                        B = round(m.diffuse_color.b ,4)
                                
                                        if colorF[0] == R and colorF[1] == G and colorF[2] == B:
                                            bpy.ops.object.material_slot_add()
                                            bpy.context.object.material_slots[0].material = m
                                            self.ok3 = False
                                            break
                                    if self.ok3 == True:
                                        mat = bpy.data.materials.new('Material0')
                                        mat.diffuse_color = colorF
                                        bpy.context.object.data.materials.append(mat)
                                    self.first = False
                                    self.ok3 = True
                            else :
                                    for m in bpy.data.materials:
                                
                                        R = round(m.diffuse_color.r ,4)
                                        G = round(m.diffuse_color.g ,4)
                                        B = round(m.diffuse_color.b ,4)
                                
                                        if colorP[0] == R and colorP[1] == G and colorP[2] == B:
                                            bpy.ops.object.material_slot_add()
                                            bpy.context.object.material_slots[0].material = m
                                            break
                                    if self.ok3 == True:
                                        mat = bpy.data.materials.new('Material0')
                                        mat.diffuse_color = colorP
                                        bpy.context.object.data.materials.append(mat)
                                    
                                    self.ok3 = True
                            
                        self.ok = False
                    
        def start(self):
            while self.numPix1 != self.numPixMax1:
                couleurPix1 = self.couleurPix1
                for t in self.listNumPixY:#t=y1
                    for g in self.listNumPixX:#g=x1
                        if couleurPix1[g,t] == font:
                            self.numPix1 += 1
                        else:
                            if couleurPix1[g+1,t] == font or couleurPix1[g-1,t] == font or couleurPix1[g,t+1] == font or couleurPix1[g,t-1] == font:
                                self.contour = True
                            self.numPix1 += 1
                            self.contour2(t,g)
                            self.contour = False


            bpy.ops.object.select_by_type(extend=False, type='MESH')
            bpy.ops.object.join()
            bpy.context.object.location.x = 0
            bpy.context.object.location.y = 0
            bpy.context.object.location.z = 0
            bpy.context.object.rotation_euler[0] = 3.14159

#                                                               End of create_object class #
############################################################################################



########## For Panel ##############
Scene = bpy.types.Scene
props = bpy.props
Scene.Front_Image = props.StringProperty(name = 'Front_Image',subtype="FILE_PATH")
Scene.Profil_Image = props.StringProperty(name = 'Profil_Image',subtype="FILE_PATH")
Scene.Name = props.StringProperty(subtype="FILE_NAME")
Scene.Radius = props.FloatProperty(name = 'Radius', max=0.1, min=0.0001, default=0.05, step=0.1,precision=4)
Scene.Effect = props.BoolProperty(name = 'effect')
Scene.Remove_Doubles_Faces = props.BoolProperty(name = 'Remove_doubles')
Scene.Font = props.IntVectorProperty(name = 'RGB',min=0,max=255)
##### Class panel #####
class tool_props_panel(bpy.types.Panel):
    bl_label = "2D to 3D properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"
    def draw(self, context):
        prop = self.layout.prop
        scene = bpy.context.scene
        prop(scene, 'Name')
        prop(scene, 'Front_Image')
        prop(scene, 'Profil_Image')
        prop(scene, 'Font')
        prop(scene, 'Radius')
        prop(scene, 'Effect')
        prop(scene, 'Remove_Doubles_Faces')
        self.layout.operator('2dto.3d', text = 'Create').bu_ok
        
        
##### Class for create 3d object if click on button 'create'
class create_3d_object(bpy.types.Operator):
    bl_idname = "2dto.3d"
    bl_label = "2D to 3D"
    bu_ok = bpy.props.StringProperty()
    def execute(self, context):
        tp1 = time.clock()
        ##### Get values of panel #####
        dir_front = bpy.data.scenes["Scene"].Front_Image
        dir_profil = bpy.data.scenes["Scene"].Profil_Image
        RGB = bpy.data.scenes["Scene"].Font
        rad = bpy.data.scenes["Scene"].Radius
        
        ##### Call the create_object class #####
        ob_3d = create_object(dir_front,dir_profil,RGB,rad)
        ob_3d.start()

        ##### Extra #####
        if bpy.data.scenes["Scene"].Remove_Doubles_Faces==True:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.remove_doubles()
            #bpy.ops.mesh.select_all(action='TOGGLE')
            #bpy.ops.mesh.select_interior_faces()
            #bpy.ops.mesh.delete(type='ONLY_FACE')
            bpy.ops.object.editmode_toggle()
        if bpy.data.scenes["Scene"].Effect==True:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.subdivide(number_cuts=5,smoothness=0, fractal=0.5)
            bpy.ops.mesh.subdivide(number_cuts=1,smoothness=1)
            bpy.ops.object.editmode_toggle()
        bpy.context.object.name = bpy.context.scene.Name
        tp2 = time.clock()
        print(tp2-tp1)
        return{'FINISHED'}
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
 register()

