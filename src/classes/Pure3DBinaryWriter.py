#
# Imports
#

import math

import classes.BinaryWriter
import classes.Colour
import classes.Matrix
import classes.Vector2
import classes.Vector3

#
# Class
#

class Pure3DBinaryWriter(classes.BinaryWriter.BinaryWriter):
	def writePure3DColour(self, colour : classes.Colour.Colour) -> None:
		if self.isLittleEndian:
			self.writeByte(colour.blue)

			self.writeByte(colour.green)

			self.writeByte(colour.red)

			self.writeByte(colour.alpha)
		else:
			self.writeByte(colour.alpha)

			self.writeByte(colour.red)

			self.writeByte(colour.green)

			self.writeByte(colour.blue)

	def writePure3DFourCharacterCode(self, value : str) -> None:
		if len(value) > 4:
			raise ValueError("Four character code must be less than or equal to 4 characters.")

		paddedValue = value.ljust(4, "\0")

		if not self.isLittleEndian:
			paddedValueCharacters = list(paddedValue)

			paddedValueCharacters.reverse()

			paddedValue = "".join(paddedValueCharacters)

		self.writeString(paddedValue)

	def writePure3DMatrix(self, matrix : classes.Matrix.Matrix) -> None:
		self.writeFloat(matrix.m11)

		self.writeFloat(matrix.m12)

		self.writeFloat(matrix.m13)

		self.writeFloat(matrix.m14)

		self.writeFloat(matrix.m21)

		self.writeFloat(matrix.m22)

		self.writeFloat(matrix.m23)

		self.writeFloat(matrix.m24)

		self.writeFloat(matrix.m31)

		self.writeFloat(matrix.m32)

		self.writeFloat(matrix.m33)

		self.writeFloat(matrix.m34)

		self.writeFloat(matrix.m41)

		self.writeFloat(matrix.m42)

		self.writeFloat(matrix.m43)

		self.writeFloat(matrix.m44)

	def writePure3DString(self, value : str) -> None:
		if len(value) > 255:
			raise ValueError("String must be less than or equal to 255 characters.")

		valueToWrite = value
		
		if len(value) < 252:
			# Note: This padding is intentionally fucked (doesn't include the length byte)
			#	because Radical was stupid when they were making The Simpsons Hit & Run
			valueToWrite = value.ljust(4 * math.ceil(len(value) / 4), "\0")

		self.writeByte(len(value))

		self.writeString(valueToWrite)

	def writePure3DVector2(self, vector2 : classes.Vector2.Vector2) -> None:
		self.writeFloat(vector2.x)

		self.writeFloat(vector2.y)

	def writePure3DVector3(self, vector2 : classes.Vector3.Vector3) -> None:
		self.writeFloat(vector3.x)

		self.writeFloat(vector3.y)

		self.writeFloat(vector3.z)