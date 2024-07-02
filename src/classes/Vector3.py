#
# Imports
#

from __future__ import annotations

import typing

#
# Class
#

class Vector3Options(typing.TypedDict):
	x : int

	y : int

	z : int

class Vector3(Vector2Options):
	def __init__(self, options: Vector3Options) -> None:
		self.x : int = options["x"]
		
		self.y : int = options["y"]

		self.z : int = options["z"]