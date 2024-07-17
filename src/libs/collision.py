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
				(rotationMatrixXChunk.vector.x,rotationMatrixXChunk.vector.y,rotationMatrixXChunk.vector.z,0),
				(rotationMatrixYChunk.vector.x,rotationMatrixYChunk.vector.y,rotationMatrixYChunk.vector.z,0),
				(rotationMatrixZChunk.vector.x,rotationMatrixZChunk.vector.y,rotationMatrixZChunk.vector.z,0),
				(0,0,0,1),
			))
			obj = bpy.data.objects.new(collisionObject.name+"Box",None)
			obj.empty_display_size = 1
			obj.empty_display_type = "CUBE"
			obj.rotation_euler = matrix.to_euler()
			obj.location = centerChunk.vector.xzy
			obj.scale = child.halfExtents.xzy
			objects.append(obj)
		else:
			print("Unknown collision type " + hex(child.identifier))
	
	return objects