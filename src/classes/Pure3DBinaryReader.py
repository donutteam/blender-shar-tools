#
# Imports
#

from __future__ import annotations

from classes.BinaryReader import BinaryReader
from classes.Colour import Colour
from classes.Matrix import Matrix
from classes.Vector2 import Vector2
from classes.Vector3 import Vector3

#
# Class
#

class Pure3DBinaryReader(BinaryReader):
	def readPure3DColour(self) -> Colour:
		valueBytes = self.readBytes(4)

		if self.isLittleEndian:
			valueBytes.reverse()

		blue = valueBytes[0]

		green = valueBytes[1]

		red = valueBytes[2]

		alpha = valueBytes[3]

		return Colour(red, green, blue, alpha)

	def readPure3DFourCharacterCode(self) -> str:
		rawString = self.readString(4)

		if not self.isLittleEndian:
			rawStringCharacters = list(rawString)

			rawStringCharacters.reverse()

			rawString = "".join(rawStringCharacters)

		return self.trimNull(rawString)

	def readPure3DMatrix(self) -> str:
		matrix : list[float] = []

		for i in range(16):
			matrix.append(self.readFloat())

		return Matrix(*matrix)

	def readPure3DString(self) -> str:
		stringLength = self.readByte()

		string = self.readString(stringLength)

		return self.trimNull(string)

	def readPure3DVector2(self) -> Vector2:
		x = self.readFloat()

		y = self.readFloat()

		return Vector2(x, y)

	def readPure3DVector3(self) -> Vector3:
		x = self.readFloat()

		y = self.readFloat()

		z = self.readFloat()

		return Vector3(x, y, z)
			
	def trimNull(self, string) -> str:
		nullIndex = string.find("\0")

		if nullIndex == -1:
			return string

		return string[:nullIndex]