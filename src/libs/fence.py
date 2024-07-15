#
# Imports
#

from __future__ import annotations

import bpy

from classes.Vector3 import Vector3

#
# Utility Functions
#

def createFence(start : Vector3, end : Vector3, normal : Vector3, name : str | None) -> bpy.types.Object:	
	#
	# Create Curve
	#

	# https://docs.blender.org/api/current/bpy.types.Curve.html
	fenceCurve = bpy.data.curves.new("Fence", "CURVE")

	fenceCurve.dimensions = "2D"

	fenceCurve.extrude = 50

	#
	# Create Spline
	#

	# https://docs.blender.org/api/current/bpy.types.CurveSplines.html
	fenceCurveSpline = fenceCurve.splines.new("POLY")

	fenceCurveSpline.points.add(1) # Only need to add one, splines start with 1 point

	# TODO: Logic to flip the start and end if the normal is backwards?
	#	Calculate a normal from the start and end points
	#	Calculate a dot product with that ^ and the normal in the file?
	#   If it's negative, flip the start and end points

	# https://docs.blender.org/api/current/bpy.types.SplinePoint.html
	fenceCurveSpline.points[0].co = (start.x, start.z, start.y, 1) # Swap Z and Y because Hit & Run uses Y for the vertical axis

	fenceCurveSpline.points[1].co = (end.x, end.z, end.y, 1) # Ditto

	fenceCurveSpline.use_smooth = False

	#
	# Create Object
	#

	name = name if name is not None else "Fence"

	# https://docs.blender.org/api/current/bpy.types.Object.html
	fence = bpy.data.objects.new(name, fenceCurve)

	fence.lock_rotation = [ True, True, False ]

	#
	# Return
	#

	return fence