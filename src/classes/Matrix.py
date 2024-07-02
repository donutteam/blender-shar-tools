#
# Imports
#

from __future__ import annotations

import typing

#
# Class
#

class MatrixOptions(typing.TypedDict):
	m11 : float

	m12 : float

	m13 : float

	m14 : float

	m21 : float

	m22 : float

	m23 : float

	m24 : float

	m31 : float

	m32 : float

	m33 : float

	m34 : float

	m41 : float

	m42 : float

	m43 : float

	m44 : float

class Matrix:
	def __init__(self, options: MatrixOptions) -> None:
		self.m11 : float = options["m11"]

		self.m12 : float = options["m12"]

		self.m13 : float = options["m13"]

		self.m14 : float = options["m14"]

		self.m21 : float = options["m21"]

		self.m22 : float = options["m22"]

		self.m23 : float = options["m23"]

		self.m24 : float = options["m24"]

		self.m31 : float = options["m31"]

		self.m32 : float = options["m32"]

		self.m33 : float = options["m33"]

		self.m34 : float = options["m34"]

		self.m41 : float = options["m41"]

		self.m42 : float = options["m42"]

		self.m43 : float = options["m43"]

		self.m44 : float = options["m44"]