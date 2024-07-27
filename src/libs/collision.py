#
# Imports
#

import bpy

from classes.chunks.CollisionObjectChunk import CollisionObjectChunk
from classes.chunks.CollisionVolumeChunk import CollisionVolumeChunk
from classes.chunks.CollisionOrientedBoundingBoxChunk import CollisionOrientedBoundingBoxChunk
from classes.chunks.CollisionVectorChunk import CollisionVectorChunk
from classes.chunks.CollisionCylinderChunk import CollisionCylinderChunk
from classes.chunks.CollisionSphereChunk import CollisionSphereChunk

import mathutils
import math

#
# Utility Functions
#

def createCollision(collisionObject: CollisionObjectChunk) -> list[bpy.types.Object]:
	return createFromVolume(collisionObject,collisionObject.getFirstChildOfType(CollisionVolumeChunk))

def createNewCollisionBox():
	bpy.ops.mesh.primitive_cube_add(
		size=2
	)

	obj = bpy.context.active_object

	bpy.context.view_layer.objects.active = None
	obj.collisionProperties.collisionType = "Box"
	return obj

def createNewCollisionCylinder(radius: float, length: float, flatEnd: bool):
	bpy.ops.mesh.primitive_uv_sphere_add(
		radius=1,
	)

	obj = bpy.context.active_object

	bpy.context.view_layer.objects.active = None

	combinedstring = ""
	for i in obj.data.vertices:
		combinedstring += str(i.co.x) + ","
		combinedstring += str(i.co.y) + ","
		combinedstring += str(i.co.z)
		combinedstring += "|"
	obj.collisionProperties.originalCoords = combinedstring

	obj.collisionProperties.collisionType = "Cylinder"
	obj.collisionProperties.radius = radius
	obj.collisionProperties.length = length
	obj.collisionProperties.flatEnd = flatEnd
	return obj

def createNewCollisionSphere(radius: float):
	bpy.ops.mesh.primitive_uv_sphere_add(
		radius=1,
	)

	obj = bpy.context.active_object

	bpy.context.view_layer.objects.active = None

	combinedstring = ""
	for i in obj.data.vertices:
		combinedstring += str(i.co.x) + ","
		combinedstring += str(i.co.y) + ","
		combinedstring += str(i.co.z)
		combinedstring += "|"
	obj.collisionProperties.originalCoords = combinedstring

	obj.collisionProperties.collisionType = "Sphere"
	obj.collisionProperties.radius = radius

	return obj

def createFromVolume(collisionObject: CollisionObjectChunk, collisionVolume: CollisionVolumeChunk) -> list[bpy.types.Object]:
	objects = []

	for child in collisionVolume.children:
		if isinstance(child, CollisionVolumeChunk):
			objects.extend(createFromVolume(collisionObject,child))
		elif isinstance(child, CollisionOrientedBoundingBoxChunk):
			centerChunk, rotationMatrixXChunk, rotationMatrixYChunk, rotationMatrixZChunk = child.getChildrenOfType(CollisionVectorChunk)
			matrix = mathutils.Matrix((
				(rotationMatrixXChunk.vector.x,rotationMatrixYChunk.vector.x,rotationMatrixZChunk.vector.x,),
				(rotationMatrixXChunk.vector.y,rotationMatrixYChunk.vector.y,rotationMatrixZChunk.vector.y,),
				(rotationMatrixXChunk.vector.z,rotationMatrixYChunk.vector.z,rotationMatrixZChunk.vector.z,),
			))

			matrix2 = mathutils.Matrix.LocRotScale(centerChunk.vector,matrix,child.halfExtents)


			obj = createNewCollisionBox()
			for collection in obj.users_collection:
				collection.objects.unlink(obj)

			obj.name = collisionObject.name

			obj.matrix_world = matrix2
			obj.location = obj.location.xzy
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(90),3,"X") @ obj.rotation_euler.to_matrix()).to_euler()
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(180),3,"Y") @ obj.rotation_euler.to_matrix()).to_euler()

			objects.append(obj)
		elif isinstance(child, CollisionCylinderChunk):
			centerChunk, directionChunk = child.getChildrenOfType(CollisionVectorChunk)

			obj = createNewCollisionCylinder(child.cylinderRadius,child.length,child.flatEnd == 1)

			for collection in obj.users_collection:
				collection.objects.unlink(obj)

			obj.name = collisionObject.name

			z_axis = mathutils.Vector((0,0,1))
			obj.matrix_world = mathutils.Matrix.Rotation(
				z_axis.angle(directionChunk.vector),
				4,
				z_axis.cross(directionChunk.vector),
			) @ obj.matrix_world
			obj.location = centerChunk.vector.xzy

			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(90),3,"X") @ obj.rotation_euler.to_matrix()).to_euler()
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(180),3,"Y") @ obj.rotation_euler.to_matrix()).to_euler()


			objects.append(obj)
		elif isinstance(child, CollisionSphereChunk):
			centerChunk = child.getFirstChildOfType(CollisionVectorChunk)
			
			obj = createNewCollisionSphere(child.radius)
			for collection in obj.users_collection:
				collection.objects.unlink(obj)

			obj.name = collisionObject.name

			obj.location = centerChunk.vector.xzy

			objects.append(obj)
		else:
			print("Unknown collision type " + hex(child.identifier))
	
	return objects