import bpy

bl_info = {
  "name": "Multi Render",
  "author": "Mike Lundahl <contact@madebylundahl.com>",
  "description": "Renders filtered objects to their own image file",
  "blender": (3, 1, 2),
  "version": (1, 2, 0),
  "category": "3D View"
}

class OBJECT_OT_multi_render(bpy.types.Operator):
    bl_idname = "object.multi_render"
    bl_label = "OBJECT_OT_multi_render"
    bl_options = {'REGISTER', 'UNDO'}

    my_filter: bpy.props.StringProperty(name="String Value")
    my_filter_freeze: bpy.props.StringProperty(name="String Value")
    my_ray_visibility: bpy.props.BoolProperty(name="Boolean Value")

    def execute(self, context):
      self.report(
          {'INFO'}, 'Render finished!'
      )
      print("Render started")
      initRender(self.my_filter, self.my_filter_freeze, self.my_ray_visibility)
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
    
    row_freeze = layout.row()
    row_freeze.prop(context.scene, 'filter_freeze')
    
    row_ray_viz = layout.row()
    row_ray_viz.prop(context.scene, 'ray_vis')
    
    props = self.layout.operator('object.multi_render', text='RENDER')
    props.my_filter = context.scene.filter_check
    props.my_filter_freeze = context.scene.filter_freeze
    props.my_ray_visibility = context.scene.ray_vis

def register():
  bpy.types.Scene.filter_check = bpy.props.StringProperty(name="Filter")
  bpy.types.Scene.filter_freeze = bpy.props.StringProperty(name="Freeze")
  bpy.types.Scene.ray_vis = bpy.props.BoolProperty(
      name="Ray Visibility",
      description="Hides from camera but keeps visible in ray calculations, like reflections, shadows etc.",
    )
  bpy.utils.register_class(OBJECT_OT_multi_render)
  bpy.utils.register_class(VIEW3D_PT_multi_render)

def unregister():
  bpy.types.Scene.filter_check = bpy.props.StringProperty(name="Filter")
  bpy.types.Scene.filter_freeze = bpy.props.StringProperty(name="Freeze")
  bpy.types.Scene.ray_vis = bpy.props.BoolProperty(
    name="Ray_vis",
    description="Hides from camera but keeps visible in ray calculations, like reflections, shadows etc.",
    default = False
  )
  bpy.utils.unregister_class(OBJECT_OT_multi_render)
  bpy.utils.unregister_class(VIEW3D_PT_multi_render)


def selectObjects(the_object_name):
  bpy.ops.object.select_pattern(pattern="*" + the_object_name + "*", case_sensitive=True, extend=False)
  return bpy.context.selected_objects

def deselectUnselectedObjects(ray_visibility):
  bpy.ops.object.select_all(action='INVERT')
  selected_objects = bpy.context.selected_objects
  hideAllEditableObjects(selected_objects, ray_visibility)

def renderObject():
  print('Rendering image')
  bpy.ops.render.render(animation=False, write_still=True, use_viewport=True, layer="gold", scene="")
    
def setOutput(index, the_object_name, base_path):
  bpy.context.scene.render.filepath = base_path + the_object_name + str(index) + ".png"
    
def hideAllEditableObjects(objects, ray_visibility):
  for o in objects:
    if o.type == 'MESH':
      if ray_visibility:
        o.visible_camera = False
      else:
        o.hide_viewport = True
        o.hide_render = True

def unhideAndRender(objects, object_names, base_path, selected_freezed_objects, freeze_objects, ray_visibility):
  for index, o in enumerate(objects):
    print("Rendering ", str(index + 1), "of ", str(len(objects)))
    setOutput(index, object_names, base_path)

    if ray_visibility:
      o.visible_camera = True
    else:
      o.hide_viewport = False
      o.hide_render = False
    
    if len(freeze_objects) >= 1 and len(selected_freezed_objects) >= 1:
      unhide_freezed(selected_freezed_objects, ray_visibility)
    
    renderObject()

    if ray_visibility:
      o.visible_camera = False
    else:
      o.hide_viewport = True
      o.hide_render = True

def unhide_freezed(objects, ray_visibility):
  print("Unhiding freezed")
  for index, o in enumerate(objects):
    if ray_visibility:
      o.visible_camera = True
    else:
      o.hide_viewport = False
      o.hide_render = False

def unhideAllObjects(objects, ray_visibility):
  for o in objects:
    if ray_visibility:
      o.visible_camera = True
    else:
      o.hide_viewport = False
      o.hide_render = False

def resetOutput(base_path):
  bpy.context.scene.render.filepath = base_path

def initRender(the_objects, freeze_objects, ray_visibility):
  base_path = bpy.context.scene.render.filepath

  print("Render initiated")
  print("Freeze filter: ", freeze_objects)
  selected_objects = selectObjects(the_objects)
  selected_freezed_objects = selectObjects(freeze_objects)
  
  deselectUnselectedObjects(ray_visibility)
  hideAllEditableObjects(selected_objects, ray_visibility)

  unhideAndRender(selected_objects, the_objects, base_path, selected_freezed_objects, freeze_objects, ray_visibility)
  unhideAllObjects(selected_objects, ray_visibility)
  resetOutput(base_path)

  print("Rendering finished!")
