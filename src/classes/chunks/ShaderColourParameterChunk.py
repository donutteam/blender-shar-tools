#
# Imports
#

from __future__ import annotations

import typing

from classes.Colour import Colour
from classes.chunks.Chunk import Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class ShaderColourParameterChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, isLittleEndian)

		parameter = binaryReader.readPure3DFourCharacterCode()
		colour = binaryReader.readPure3DColour()

		return [parameter,colour]

	def __init__(self, identifier: chunkIdentifiers.SHADER_COLOUR_PARAMETER, children : list[Chunk] | None = None, parameter: str = "", colour: Colour = Colour(0,0,0,255)) -> None:
		super().__init__(identifier,children)
	
		self.parameter = parameter
		self.colour = colour
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DFourCharacterCode(self.parameter)
		binaryWriter.writePure3DColour(self.colour)