#
# Imports
#

import bpy

from classes.chunks.CollisionObjectChunk import CollisionObjectChunk
from classes.chunks.CollisionVolumeChunk import CollisionVolumeChunk
from classes.chunks.CollisionOrientedBoundingBoxChunk import CollisionOrientedBoundingBoxChunk
from classes.chunks.CollisionVectorChunk import CollisionVectorChunk

import mathutils

#
# Utility Functions
#

def createCollision(collisionObject: CollisionObjectChunk) -> list[bpy.types.Object]:
	return createFromVolume(collisionObject,collisionObject.getFirstChildOfType(CollisionVolumeChunk))

def createFromVolume(collisionObject: CollisionObjectChunk, collisionVolume: CollisionVolumeChunk) -> list[bpy.types.Object]:
	objects = []

	for child in collisionVolume.children:
		if isinstance(child, CollisionVolumeChunk):
			objects.extend(createFromVolume(collisionObject,child))
		elif isinstance(child, CollisionOrientedBoundingBoxChunk):
			centerChunk, rotationMatrixXChunk, rotationMatrixYChunk, rotationMatrixZChunk = child.getChildrenOfType(CollisionVectorChunk)
			matrix = mathutils.Matrix((
				(rotationMatrixXChunk.vector.x,rotationMatrixYChunk.vector.x,rotationMatrixZChunk.vector.x,0),
				(rotationMatrixXChunk.vector.y,rotationMatrixYChunk.vector.y,rotationMatrixZChunk.vector.y,0),
				(rotationMatrixXChunk.vector.z,rotationMatrixYChunk.vector.z,rotationMatrixZChunk.vector.z,0),
				(0,0,0,1),
			))
			euler: mathutils.Euler = matrix.to_euler()
			#euler.rotate_axis("Z",180)
			"""bpy.ops.mesh.primitive_cube_add(
				location=(centerChunk.vector.x, centerChunk.vector.z, centerChunk.vector.y),
				rotation=euler.,
				size=2,
				scale=(child.halfExtents.x, child.halfExtents.y, child.halfExtents.z),
			)
			obj = bpy.context.active_object
			for collection in obj.users_collection:
				collection.objects.unlink(obj)
			obj.name = collisionObject.name+"Box"
			objects.append(obj)"""
			obj = bpy.data.objects.new(collisionObject.name+"Box",None)
			obj.empty_display_size = 1
			obj.empty_display_type = "CUBE"
			obj.rotation_euler = mathutils.Euler((euler.x,euler.z,euler.y))
			obj.location = centerChunk.vector.xzy
			obj.scale = child.halfExtents.xzy
			objects.append(obj)
		else:
			print("Unknown collision type " + hex(child.identifier))
	
	return objects