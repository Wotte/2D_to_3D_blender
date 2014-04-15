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
from tkinter import *
from PIL import ImageTk, Image
import bpy
import bmesh
from math import floor

############################################################################################
# Class for create the 3d object                                                           #
class create_object():
        #Property Images
        def __init__(self,dir_front,dir_profil,RGB):
            self.dir_front = dir_front
            self.dir_profil = dir_profil
            self.RGB = RGB
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
        
            self.mylayers = [False]*20
            self.mylayers[0] = True
            self.listNumPixX2 = range(0,self.largeur2+2)
            self.listNumPixX = range(0,self.largeur+2)
            self.listNumPixY = range(0,self.hauteur+2)
            self.numPix1 = 0
            self.numPixMax1 = (self.hauteur+2)*(self.largeur+2)
            self.couleurPix2 = self.imageBord1.load()
            self.couleurPix1 = self.imageBord2.load()
            self.add_cube = bpy.ops.mesh.primitive_cube_add
            self.contour = False
            self.ok = False
            self.first = True
            self.ok2 = False
            #global listNumPixX2, contour, ok, couleurPix2, font, add_cube, mylayers, first, ok2
        
        def contour2(self,y1,x1):
            #global ok
            for h in self.listNumPixX2:
                if self.couleurPix2[h,y1] == self.font:
                    pass
                elif self.contour == True:
                    self.add_cube(radius=0.1,location=(x1-((x1-1)*0.8), h-((h-1)*0.8),\
                     y1-((y1-1)*0.8)), layers=self.mylayers)
                    self.ok = True
                elif self.couleurPix2[h+1,y1] == self.font or self.couleurPix2[h-1,y1] == self.font or\
                 self.couleurPix2[h,y1+1] == self.font or self.couleurPix2[h,y1-1] == self.font:
                    self.add_cube(radius=0.1,location=(x1-((x1-1)*0.8), h-((h-1)*0.8)\
                    , y1-((y1-1)*0.8)), layers=self.mylayers)
                    self.ok = True
                else:
                    pass
                if self.ok == True:
                        colorP = ( round(((self.couleurPix2[h,y1][0])/255),4),\
                        round(((self.couleurPix2[h,y1][1])/255),4),round(((self.couleurPix2[h,y1][2])/255),4) )
                        colorF = ( round(((self.couleurPix1[x1,y1][0])/255),4),\
                        round(((self.couleurPix1[x1,y1][1])/255),4),round(((self.couleurPix1[x1,y1][2])/255),4) )
                        if len(bpy.data.materials.values()) == 0:
                            mat = bpy.data.materials.new('Material')
                            mat.diffuse_color = colorP
                            bpy.context.object.data.materials.append(mat)
                        else:
                            
                            for m in bpy.data.materials:
                                
                                R = round(m.diffuse_color.r ,4)
                                G = round(m.diffuse_color.g ,4)
                                B = round(m.diffuse_color.b ,4)
                                
                                if colorP[0] == R and colorP[1] == G and colorP[2] == B:
                                    bpy.ops.object.material_slot_add()
                                    bpy.context.object.material_slots[0].material = m
                                    break
                                
                            else :
                                mat = bpy.data.materials.new('Material0')
                                mat.diffuse_color = colorP
                                bpy.context.object.data.materials.append(mat)
                            
                        self.ok = False
                    
        def start(self):
            while self.numPix1 != self.numPixMax1:
                for t in self.listNumPixY:#t=y1
                    for g in self.listNumPixX:#g=x1
                        self.first = True
                        if self.couleurPix1[g,t] == self.font:
                            self.numPix1 += 1
                        else:
                            if self.couleurPix1[g+1,t] == self.font or self.couleurPix1[g-1,t] == self.font \
                            or self.couleurPix1[g,t+1] == self.font or self.couleurPix1[g,t-1] == self.font:
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


############################################################################################
# Class for create the priority window                                                     #
class win_priority():
        def __init__(self, dir_front):
                self.nbr = 20
                self.list_tags = []
                self.dir_front = dir_front
                self.im = Image.open(r'{}'.format(self.dir_front))
                self.imr = self.im.resize((self.im.size[0]*self.nbr,self.im.size[1]*self.nbr))
                
                self.root = Tk()
                self.root.title('Priority')
                self.can = Canvas(root, width = imr.size[0], height =imr.size[1], bg ='gray')

                self.img = ImageTk.PhotoImage(self.imr)
                self.can.create_image((self.imr.size[0]/2)+2,(self.imr.size[1]/2)+2,image = self.img, tags = 'image')
                
        def resize_grid(self):
            self.imr = self.im.resize((self.im.size[0]*self.nbr,self.im.size[1]*self.nbr))
            for x in range(self.im.size[0]):
                for y in range(self.im.size[1]):
                    for nb in range(self.nbr):
                        self.imr.putpixel((x*self.nbr+nb,y*self.nbr),(0,0,0))
                        self.imr.putpixel((x*self.nbr,y*self.nbr+nb),(0,0,0))
            self.can.configure(width = self.imr.size[0], height =self.imr.size[1])
            self.img = ImageTk.PhotoImage(self.imr)
            self.can.gettags
            self.can.delete('image')
            self.can.create_image((self.imr.size[0]/2)+2,(self.imr.size[1]/2)+2,image = self.img, tags = 'image')
    
            for nb in self.list_tags:
                xt = floor(float(nb[0]))*self.nbr+((3*self.nbr)/5)
                yt = floor(float(nb[1]))*self.nbr+((3*self.nbr)/5)
                if self.can.find_withtag(''+str(xt)+str(yt)):
                    print(self.list_tags)
                    print(nb)
                    self.can.delete(''+str(xt)+str(yt))
                    self.list_tags.remove([nb[0],nb[1]])
                    self.list_tags.remove([nb[0],nb[1]])
                    print(self.list_tags)
        
                self.can.create_text(xt, yt, font=("Purisa",self.nbr-8), text= 'O', tags =''+str(xt)+str(yt))
                self.list_tags.append([x,y])
            #global imr, img, canevas

        def pointeur(self, event):
            x =(event.x/self.nbr)
            y =(event.y/self.nbr)
            xt = floor(float(x))*self.nbr+((3*self.nbr)/5)
            yt = floor(float(y))*self.nbr+((3*self.nbr)/5)
            print(x*self.nbr,y*self.nbr)
            if self.can.find_withtag(''+str(xt)+str(yt)):
                self.can.delete(''+str(xt)+str(yt))
            else:
                self.can.create_text(xt, yt, font=("Purisa",self.nbr-8), text= 'O', tags =''+str(xt)+str(yt))
                self.list_tags.append([x,y])
            self.chaine.configure(text = "Clic détecté en X =" + str(floor(float(x))) +\
                                ", Y =" + str(floor(float(y))))

        def image_resize(self,event):
                if event.delta<0:
                        self.nbr += 2
                if event.delta>0:
                        self.nbr -= 2
                self.resize_grid()
        def start(self):
                self.resize_grid()
                self.can.bind('<Button-1>', self.pointeur)
                self.root.bind('<MouseWheel>', self.image_resize)
                self.can.pack()
                self.chaine = Label(self.root)
                self.chaine.pack()
                self.root.mainloop()

#                                                                End of win_priority class #
############################################################################################

########## For Panel ##############
bpy.types.Scene.Front_Image = bpy.props.StringProperty(name = 'Front_Image',subtype="FILE_PATH")
bpy.types.Scene.Profil_Image = bpy.props.StringProperty(name = 'Profil_Image',subtype="FILE_PATH")
bpy.types.Scene.Name = bpy.props.StringProperty(subtype="FILE_NAME")
bpy.types.Scene.Effect = bpy.props.BoolProperty(name = 'effect')
bpy.types.Scene.Font = bpy.props.IntVectorProperty(name = 'RGB',min=0,max=255)
##### Class panel #####
class tool_props_panel(bpy.types.Panel):
    bl_label = "2D to 3D properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"
    def draw(self, context):
        self.layout.prop(bpy.context.scene, 'Name')
        self.layout.prop(bpy.context.scene, 'Front_Image')
        self.layout.operator('win.priority', text = 'Priority').bu_priority
        self.layout.prop(bpy.context.scene, 'Profil_Image')
        self.layout.prop(bpy.context.scene, 'Font')
        self.layout.prop(bpy.context.scene, 'Effect')
        self.layout.operator('2dto.3d', text = 'Create').bu_ok
        
##### Class for open the priority window if click on button 'create' #####
class bu_win_priority(bpy.types.Operator):
        bl_idname = "win.priority"
        bl_label = "Window priority"
        bu_priority = bpy.props.StringProperty()
        def execute(self, context):
            dir_front = bpy.data.scenes["Scene"].Front_Image
            win = win_priority(dir_front)
            return{'FINISHED'}
        
##### Class for create 3d object if click on button 'priority'
class create_3d_object(bpy.types.Operator):
    bl_idname = "2dto.3d"
    bl_label = "2D to 3D"
    bu_ok = bpy.props.StringProperty()
    def execute(self, context):
        ##### Get values of panel #####
        dir_front = bpy.data.scenes["Scene"].Front_Image
        dir_profil = bpy.data.scenes["Scene"].Profil_Image
        RGB = bpy.data.scenes["Scene"].Font
        
        ##### Call the create_object class #####
        ob_3d = create_object(dir_front,dir_profil,RGB)
        ob_3d.start()

        ##### Extra #####
        if bpy.data.scenes["Scene"].Effect==True:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.subdivide(number_cuts=5,smoothness=0, fractal=0.5)
            bpy.ops.mesh.subdivide(number_cuts=1,smoothness=1)
            bpy.ops.object.editmode_toggle()
        bpy.context.object.name = bpy.context.scene.Name
        return{'FINISHED'}
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
 register()

