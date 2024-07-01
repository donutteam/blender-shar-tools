#
# Imports
#

from __future__ import annotations

import typing

#
# Class
#

class ColourOptions(typing.TypedDict):
	blue : int

	green : int

	red : int

	alpha : int

class Colour(ColourOptions):
	def __init__(self, options : ColourOptions) -> None:
		self.red : int = options["red"]

		self.green : int = options["green"]

		self.blue : int = options["blue"]

		self.alpha : int = options["alpha"]