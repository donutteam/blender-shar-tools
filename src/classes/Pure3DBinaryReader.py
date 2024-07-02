#
# Imports
#

import classes.BinaryReader
import classes.Colour

#
# Class
#

class Pure3DBinaryReader(classes.BinaryReader.BinaryReader):
	def readPure3DColour(self) -> classes.Colour.Colour:
		valueBytes = self.readBytes(4)

		if self.isLittleEndian:
			valueBytes.reverse()

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

	# TODO: readPure3DFourCharacterCode

	# TODO: readPure3DMatrix

	def readPure3DString(self) -> str:
		stringLength = self.readByte()

		string = self.readString(stringLength)

		return stringBytes.decode("utf-8")

	# TODO: readPure3DVector2

	# TODO: readPure3DVector3

	def trimNull(self, string) -> str:
		nullIndex = string.find("\0")

		if nullIndex == -1:
			return string

		return string[:nullIndex]