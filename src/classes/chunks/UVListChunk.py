#
# Imports
#

from __future__ import annotations

import typing

from classes.chunks.Chunk import Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class UVListChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, isLittleEndian)

		numberOfUVs = binaryReader.readUInt32()

		channel = binaryReader.readUInt32()
		
		uvs = []
		
		for i in range(numberOfUVs):
			uvs.append(binaryReader.readPure3DVector2())

		return [channel,uvs]

	def __init__(self, identifier: chunkIdentifiers.UV_LIST, children : list[Chunk] | None = None, channel: int = 0, uvs: list[mathutils.Vector] = []) -> None:
		super().__init__(identifier,children)
	
		self.channel = channel
		self.uvs = uvs
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.uvs))

		binaryWriter.writeUInt32(self.channel)

		for uv in self.uvs:
			binaryWriter.writePure3DVector2(uv)