#
# Imports
#

from __future__ import annotations

import typing

import bpy

import classes.Vector3

#
# Utility Functions
#

class CreateFenceOptions(typing.TypedDict):
	start : classes.Vector3.Vector3

	end : classes.Vector3.Vector3

	normal : classes.Vector3.Vector3

	name : str | None

def createFence(options : CreateFenceOptions) -> bpy.types.Object:
	#
	# Options
	#

	start = options.get("start")

	end = options.get("end")

	normal = options.get("normal")

	name = options.get("name", "Fence")
	
	#
	# Create Curve
	#

	# https://docs.blender.org/api/current/bpy.types.Curve.html
	fenceCurve = bpy.data.curves.new("Fence", "CURVE")

	fenceCurve.dimensions = "2D"

	fenceCurve.extrude = 50 # TODO: Is this what makes it have verticallity?

	#
	# Create Spline
	#

	# https://docs.blender.org/api/current/bpy.types.CurveSplines.html
	fenceCurveSpline = fenceCurve.splines.new("POLY")

	fenceCurveSpline.points.add(1) # Only need to add one, splines start with 1 point

	# TODO: This might need more advanced logic for normals

	# https://docs.blender.org/api/current/bpy.types.SplinePoint.html
	fenceCurveSpline.points[0].co = (start.x, start.z, start.y, 1) # Swap Z and Y because Hit & Run uses Y for the vertical axis

	fenceCurveSpline.points[1].co = (end.x, end.z, end.y, 1) # Ditto

	fenceCurveSpline.use_endpoint_u = True

	fenceCurveSpline.use_smooth = False

	#
	# Create Object
	#

	# https://docs.blender.org/api/current/bpy.types.Object.html
	fence = bpy.data.objects.new(name, fenceCurve)

	fence.lock_rotation = [ True, True, False ]

	#
	# Return
	#

	return fence