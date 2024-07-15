#
# Imports
#

from __future__ import annotations

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

def menu_item():
	self.layout.operator(MoveObjectX.bl_idname)

def register():
	bpy.utils.register_class(MoveObjectX)

	bpy.types.VIEW3D_MT_object.append(menu_item)

def unregister():
	bpy.utils.unregister_class(MoveObjectX)

	bpy.types.VIEW3D_MT_object.remove(menu_item)