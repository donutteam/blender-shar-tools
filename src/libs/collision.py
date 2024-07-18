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
			#break
		elif isinstance(child, CollisionOrientedBoundingBoxChunk):
			centerChunk, rotationMatrixXChunk, rotationMatrixYChunk, rotationMatrixZChunk = child.getChildrenOfType(CollisionVectorChunk)
			print("[CollisionOrientedBoundingBoxChunk]")
			print("\t",rotationMatrixXChunk.vector,sep="")
			print("\t",rotationMatrixYChunk.vector,sep="")
			print("\t",rotationMatrixZChunk.vector,sep="")
			matrix = mathutils.Matrix((
				#(rotationMatrixXChunk.vector.x,rotationMatrixXChunk.vector.y,rotationMatrixXChunk.vector.z,),
				#(rotationMatrixYChunk.vector.x,rotationMatrixYChunk.vector.y,rotationMatrixYChunk.vector.z,),
				#(rotationMatrixZChunk.vector.x,rotationMatrixZChunk.vector.y,rotationMatrixZChunk.vector.z,),
				(rotationMatrixXChunk.vector.x,rotationMatrixYChunk.vector.x,rotationMatrixZChunk.vector.x,),
				(rotationMatrixXChunk.vector.y,rotationMatrixYChunk.vector.y,rotationMatrixZChunk.vector.y,),
				(rotationMatrixXChunk.vector.z,rotationMatrixYChunk.vector.z,rotationMatrixZChunk.vector.z,),
			))
			print("Matrix:")
			print("0|11\t",round(matrix[0][0],5),sep="")
			print("1|12\t",round(matrix[0][1],5),sep="")
			print("2|13\t",round(matrix[0][2],5),sep="")
			print("3|21\t",round(matrix[1][0],5),sep="")
			print("4|22\t",round(matrix[1][1],5),sep="")
			print("5|23\t",round(matrix[1][2],5),sep="")
			print("6|31\t",round(matrix[2][0],5),sep="")
			print("7|32\t",round(matrix[2][1],5),sep="")
			print("8|33\t",round(matrix[2][2],5),sep="")
			print("---")
			for i in ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX']:
				print(i,matrix.to_euler(i))
			print("---")
			euler: mathutils.Euler = matrix.to_euler("YXZ")
			conv = mathutils.Euler((-euler.x,-euler.y,-euler.z))
			print("CON",conv)
			print("CON DEG",math.degrees(conv.x),math.degrees(conv.y),math.degrees(conv.z))
			"""
			#euler = get_euler_angles_from_rotation(matrix.to_quaternion())
			#euler: mathutils.Euler = matrix.to_euler()
			#euler.rotate_axis("Z",180)
			bpy.ops.mesh.primitive_cube_add(
				#location=centerChunk.vector,#(centerChunk.vector.x, centerChunk.vector.z, centerChunk.vector.y),
				#rotation=conv,
				size=1,
			)
			#matrix2 = mathutils.Matrix.Diagonal((child.halfExtents * 2).to_4d()) @ matrix @ mathutils.Matrix.Translation(centerChunk.vector)
			matrix2 = mathutils.Matrix.LocRotScale(centerChunk.vector,matrix,child.halfExtents * 2)
			obj = bpy.context.active_object
			obj.matrix_world = matrix2
			obj.location = obj.location.xzy
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(90),3,"X") @ obj.rotation_euler.to_matrix()).to_euler()
			#obj.rotation_mode = "XYZ"
			#obj.rotation_euler = mathutils.Euler((obj.rotation_euler.x,obj.rotation_euler.y,obj.rotation_euler.z),"XZY").to_matrix().to_euler("XYZ")
			#obj.location = centerChunk.vector
			#obj.rotation_mode = "QUATERNION"
			#obj.rotation_quaternion = mathutils.Quaternion.
			
			#obj.scale = child.halfExtents
			for collection in obj.users_collection:
				collection.objects.unlink(obj)
			obj.name = collisionObject.name+"Box"
			objects.append(obj)"""


			obj = bpy.data.objects.new(collisionObject.name+"Box",None)
			obj.empty_display_size = 1
			obj.empty_display_type = "CUBE"

			matrix2 = mathutils.Matrix.LocRotScale(centerChunk.vector,matrix,child.halfExtents)
			obj.matrix_world = matrix2
			obj.location = obj.location.xzy
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(90),3,"X") @ obj.rotation_euler.to_matrix()).to_euler()


			
			objects.append(obj)
		else:
			print("Unknown collision type " + hex(child.identifier))
	
	return objects