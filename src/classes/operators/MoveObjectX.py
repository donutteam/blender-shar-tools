#
# Imports
#

import bpy

#
# Class
#

class MoveObjectX(bpy.types.Operator):
	bl_idname = "object.move_object_x"
	
	bl_label = "Move All Objects by 1 on the X Axis" 

	bl_options = {
		"REGISTER", 
		"UNDO",
	}

	def execute(self, context):		
		for obj in context.scene.objects:
			obj.location.x += 1.0

		return {"FINISHED"}

def register():
	bpy.utils.register_class(MoveObjectX)

	bpy.types.VIEW3D_MT_object.append(lambda self, context: self.layout.operator(MoveObjectX.bl_idname))

def unregister():
	bpy.utils.unregister_class(MoveObjectX)