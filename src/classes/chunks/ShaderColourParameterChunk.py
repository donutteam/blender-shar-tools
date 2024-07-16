#
# Imports
#

from __future__ import annotations

from classes.Colour import Colour
from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class ShaderColourParameterChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		parameter = binaryReader.readPure3DFourCharacterCode()
		colour = binaryReader.readPure3DColour()

		return [ parameter, colour ]

	def __init__(self, identifier: int = chunkIdentifiers.SHADER_COLOUR_PARAMETER, children : list[Chunk] = [], parameter: str = "", colour: Colour = Colour(0, 0, 0, 255)) -> None:
		super().__init__(identifier,children)
	
		self.parameter = parameter
		self.colour = colour
		

	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DFourCharacterCode(self.parameter)
		binaryWriter.writePure3DColour(self.colour)
