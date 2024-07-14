#
# Imports
#

import classes.BinaryReader
import classes.Colour
import classes.Matrix
import classes.Vector2
import classes.Vector3

#
# Class
#

class Pure3DBinaryReader(classes.BinaryReader.BinaryReader):
	def readPure3DColour(self) -> classes.Colour.Colour:
		valueBytes = self.readBytes(4)

		if self.isLittleEndian:
			valueBytes = bytes(reversed(list(valueBytes)))

		blue = valueBytes[0]

		green = valueBytes[1]

		red = valueBytes[2]

		alpha = valueBytes[3]

		return classes.Colour.Colour(
			{
				"red": red,
				"green": green,
				"blue": blue,
				"alpha": alpha,
			})

	def readPure3DFourCharacterCode(self) -> str:
		rawString = self.readString(4)

		if not self.isLittleEndian:
			rawStringCharacters = list(rawString)

			rawStringCharacters.reverse()

			rawString = "".join(rawStringCharacters)

		return self.trimNull(rawString)

	def readPure3DMatrix(self) -> str:
		matrix : list[int] = []

		for i in range(16):
			matrix.append(self.readFloat())

		return classes.Matrix.Matrix(
			{
				"m11": matrix[0],
				"m12": matrix[1],
				"m13": matrix[2],
				"m14": matrix[3],
				"m21": matrix[4],
				"m22": matrix[5],
				"m23": matrix[6],
				"m24": matrix[7],
				"m31": matrix[8],
				"m32": matrix[9],
				"m33": matrix[10],
				"m34": matrix[11],
				"m41": matrix[12],
				"m42": matrix[13],
				"m43": matrix[14],
				"m44": matrix[15],
			})

	def readPure3DString(self) -> str:
		stringLength = self.readByte()

		string = self.readString(stringLength)

		return self.trimNull(string)

	def readPure3DVector2(self) -> classes.Vector2.Vector2:
		x = self.readFloat()

		y = self.readFloat()

		return classes.Vector2.Vector2(
			{
				"x": x,
				"y": y,
			})

	def readPure3DVector3(self) -> classes.Vector3.Vector3:
		x = self.readFloat()

		y = self.readFloat()

		z = self.readFloat()

		return classes.Vector3.Vector3(
			{
				"x": x,
				"y": y,
				"z": z,
			})
			
	def trimNull(self, string) -> str:
		nullIndex = string.find("\0")

		if nullIndex == -1:
			return string

		return string[:nullIndex]