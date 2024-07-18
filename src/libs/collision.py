#
# Imports
#

import bpy

from classes.chunks.CollisionObjectChunk import CollisionObjectChunk
from classes.chunks.CollisionVolumeChunk import CollisionVolumeChunk
from classes.chunks.CollisionOrientedBoundingBoxChunk import CollisionOrientedBoundingBoxChunk
from classes.chunks.CollisionVectorChunk import CollisionVectorChunk

import mathutils
import math

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
				(rotationMatrixXChunk.vector.x,rotationMatrixYChunk.vector.x,rotationMatrixZChunk.vector.x,),
				(rotationMatrixXChunk.vector.y,rotationMatrixYChunk.vector.y,rotationMatrixZChunk.vector.y,),
				(rotationMatrixXChunk.vector.z,rotationMatrixYChunk.vector.z,rotationMatrixZChunk.vector.z,),
			))

			matrix2 = mathutils.Matrix.LocRotScale(centerChunk.vector,matrix,child.halfExtents)
										  
			obj = bpy.data.objects.new(collisionObject.name+"Box",None)
			obj.empty_display_size = 1
			obj.empty_display_type = "CUBE"
			obj.matrix_world = matrix2
			obj.location = obj.location.xzy
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(90),3,"X") @ obj.rotation_euler.to_matrix()).to_euler()
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(180),3,"Y") @ obj.rotation_euler.to_matrix()).to_euler()

			objects.append(obj)
		else:
			print("Unknown collision type " + hex(child.identifier))
	
	return objects