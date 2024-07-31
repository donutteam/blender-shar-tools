#
# Imports
#

import bpy
import mathutils

#
# Class
#

def update_collision_properties(self,context):
	obj: bpy.types.Object = getattr(self,"id_data",None)
	
	mesh: bpy.types.Mesh = obj.data

	if obj.collisionProperties.collisionType == "Cylinder":
		for i in mesh.polygons:
			i.use_smooth = not obj.collisionProperties.flatEnd
		
		obj.scale = mathutils.Vector((1,1,1))
		
		originalcoords = obj.collisionProperties.originalCoords.split("|")
		for i,v in enumerate(mesh.vertices):
			original = originalcoords[i].split(",")
			newx = float(original[0])
			newy = float(original[1])
			newz = float(original[2])

			newx *= obj.collisionProperties.radius
			newy *= obj.collisionProperties.radius
			newz *= obj.collisionProperties.radius
			if newz < 0:
				if obj.collisionProperties.flatEnd:
					newz = 0
				newz -= obj.collisionProperties.length
			if newz > 0:
				if obj.collisionProperties.flatEnd:
					newz = 0
				newz += obj.collisionProperties.length

			v.co.x = newx
			v.co.y = newy
			v.co.z = newz
	
	if obj.collisionProperties.collisionType == "Sphere":
		for i in mesh.polygons:
			i.use_smooth = True

		originalcoords = obj.collisionProperties.originalCoords.split("|")
		for i,v in enumerate(mesh.vertices):
			original = originalcoords[i].split(",")
			newx = float(original[0])
			newy = float(original[1])
			newz = float(original[2])

			newx *= obj.collisionProperties.radius
			newy *= obj.collisionProperties.radius
			newz *= obj.collisionProperties.radius

			v.co.x = newx
			v.co.y = newy
			v.co.z = newz


class CollisionProperties(bpy.types.PropertyGroup):
	collisionType: bpy.props.StringProperty(
		name="Collision Type",
		default="" # Empty string means isn't a collision
	)
	radius: bpy.props.FloatProperty(
		name="Radius",
		update=update_collision_properties
	)
	length: bpy.props.FloatProperty(
		name="Length",
		update=update_collision_properties
	)
	flatEnd: bpy.props.BoolProperty(
		name="Flat End",
		default=False,
		update=update_collision_properties
	)
	originalCoords: bpy.props.StringProperty()

class CollisionPropertiesPanel(bpy.types.Panel):
	bl_idname = "OBJECT_PT_shar_collision_properties"

	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "SHAR Blender Tools"
	bl_label = "Collision"

	def draw(self, context):
		layout = self.layout

		obj = context.object

		if obj and obj.collisionProperties and obj.collisionProperties.collisionType != "":
			layout.label(text=obj.collisionProperties.collisionType)
			if obj.collisionProperties.collisionType == "Box":
				layout.prop(obj,"scale")
			elif obj.collisionProperties.collisionType == "Cylinder":
				layout.prop(obj.collisionProperties,"radius")
				layout.prop(obj.collisionProperties,"length")
				layout.prop(obj.collisionProperties,"flatEnd")
			elif obj.collisionProperties.collisionType == "Sphere":
				layout.prop(obj.collisionProperties,"radius")

def register():
	bpy.utils.register_class(CollisionProperties)

	bpy.types.Object.collisionProperties = bpy.props.PointerProperty(type=CollisionProperties)

	bpy.utils.register_class(CollisionPropertiesPanel)

def unregister():
	bpy.utils.unregister_class(CollisionPropertiesPanel)

	bpy.utils.unregister_class(CollisionProperties)

	del bpy.types.Object.collisionProperties