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
				(0,0,0,0),
			))
			bpy.ops.mesh.primitive_cube_add(
				location=(centerChunk.vector.x, centerChunk.vector.z, centerChunk.vector.y),
				rotation=matrix.to_euler(),
				size=2,
				scale=(child.halfExtents.x, child.halfExtents.z, child.halfExtents.y),
			)
			obj = bpy.context.active_object
			for collection in obj.users_collection:
				collection.objects.unlink(obj)
			obj.name = collisionObject.name+"Box"
			objects.append(obj)
		else:
			print("Unknown collision type " + hex(child.identifier))
	
	return objects