#
# Imports
#

from __future__ import annotations

import typing

#
# Class
#

class Vector2Options(typing.TypedDict):
	x : int

	y : int

class Vector2(Vector2Options):
	def __init__(self, options: Vector2Options) -> None:
		self.x : int = options["x"]
		
		self.y : int = options["y"]