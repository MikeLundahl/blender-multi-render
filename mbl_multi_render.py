import bpy

bl_info = {
  "name": "Multi Render",
  "author": "Mike Lundahl <contact@madebylundahl.com>",
  "description": "Renders filtered objects to their own image file",
  "blender": (3, 1, 2),
  "version": (1, 0, 0),
  "category": "3D View"
}

class OBJECT_OT_multi_render(bpy.types.Operator):
    bl_idname = "object.multi_render"
    bl_label = "OBJECT_OT_multi_render"
    bl_options = {'REGISTER', 'UNDO'}

    my_filter: bpy.props.StringProperty(name="String Value")

    def execute(self, context):
      self.report(
          {'INFO'}, 'Render started, rendering ' + self.my_filter
      )
      print("Render started")
      initRender(self.my_filter)
      return {'FINISHED'}

class VIEW3D_PT_multi_render(bpy.types.Panel):

  bl_label = "Multi Render"
  bl_idname = "VIEW3D_PT_panel_multi_render"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category  = 'MBL utils'

  def draw(self, context):
    layout = self.layout

    row = layout.row()
    row.prop(context.scene, 'filter_check')
    
    props = self.layout.operator('object.multi_render', text='RENDER')
    props.my_filter = context.scene.filter_check

def register():
  bpy.types.Scene.filter_check = bpy.props.StringProperty(name="Filter")
  bpy.utils.register_class(OBJECT_OT_multi_render)
  bpy.utils.register_class(VIEW3D_PT_multi_render)

def unregister():
  bpy.utils.unregister_class(OBJECT_OT_multi_render)
  bpy.utils.unregister_class(VIEW3D_PT_multi_render)


def selectObjects(the_object_name):
  bpy.ops.object.select_pattern(pattern="*" + the_object_name + "*", case_sensitive=True, extend=False)
  return bpy.context.selected_objects

def deselectUnselectedObjects():
  bpy.ops.object.select_all(action='INVERT')
  selected_objects = bpy.context.selected_objects
  hideAllEditableObjects(selected_objects)

def renderObject():
  print('Rendering image')
  bpy.ops.render.render(animation=False, write_still=True, use_viewport=True, layer="gold", scene="")
    
def setOutput(index, the_object_name, base_path):
  bpy.context.scene.render.filepath = base_path + the_object_name + str(index) + ".png"
    
def hideAllEditableObjects(objects):
  for o in objects:
    if o.type == 'MESH':
      o.hide_viewport = True
      o.hide_render = True

def unhideAndRender(objects, object_names, base_path):
  for index, o in enumerate(objects):
    print("Rendering ", str(index + 1), "of ", str(len(objects)))
    setOutput(index, object_names, base_path)
    o.hide_viewport = False
    o.hide_render = False
    renderObject()
    o.hide_viewport = True
    o.hide_render = True
        
def unhideAllObjects(objects):
  for o in objects:
    o.hide_viewport = False
    o.hide_render = False

def resetOutput(base_path):
  bpy.context.scene.render.filepath = base_path

def initRender(the_objects):
  base_path = bpy.context.scene.render.filepath

  print("Render initiated")
  selected_objects = selectObjects(the_objects)
  deselectUnselectedObjects()
  hideAllEditableObjects(selected_objects)
  unhideAndRender(selected_objects, the_objects, base_path)
  unhideAllObjects(selected_objects)
  resetOutput(base_path)

  print("Rendering finished!")
