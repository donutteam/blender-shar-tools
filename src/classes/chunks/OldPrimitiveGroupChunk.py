#
# Imports
#

from __future__ import annotations

import typing

import classes.chunks.Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

#
# Class
#

class OldPrimitiveGroupChunkOptions(typing.TypedDict):
	children : list[classes.chunks.Chunk.Chunk] | None
	
	version: int
	
	shaderName: str

	primitiveType: int

	numberOfVertices: int

	numberofIndices: int

	numberOfMatrices: int
	



class OldPrimitiveGroupChunk(classes.chunks.Chunk.Chunk):
	
	primitiveTypes = {
		"TRIANGLE_LIST": 0,
		"TRIANGLE_STRIP": 1,
		"LINE_LIST": 2,
		"LINE_STRIP": 3,
	}

	vertexTypes = {
		"UVS": 1,
		"UVS_2": 2,
		"UVS_3": 3,
		"UVS_4": 4,
		"UVS_5": 5,
		"UVS_6": 6,
		"UVS_7": 7,
		"UVS_8": 8,
		"NORMALS": 1 << 4,
		"COLOURS": 1 << 5,
		"SPECULAR": 1 << 6,
		"MATRICES": 1 << 7,
		"WEIGHTS": 1 << 8,
		"SIZE": 1 << 9,
		"W": 1 << 10,
		"BI_NORMAL": 1 << 11,
		"TANGENT": 1 << 12,
		"POSITION": 1 << 13,
		"COLOUR_2": 1 << 14,
		"COLOUR_COUNT_1": 1 << 15,
		"COLOUR_COUNT_2": 2 << 15,
		"COLOUR_COUNT_3": 3 << 15,
		"COLOUR_COUNT_4": 4 << 15,
		"COLOUR_COUNT_5": 5 << 15,
		"COLOUR_COUNT_6": 6 << 15,
		"COLOUR_COUNT_7": 7 << 15,
		"COLOUR_MASK": 7 << 15,
		"COLOUR_MASK_OFFSET": 15,
	}

	vertexTypeMap = {
		classes.chunks.Chunk.IDENTIFIERS["PACKED_NORMAL_LIST"]: vertexTypes["NORMALS"],
		classes.chunks.Chunk.IDENTIFIERS["NORMAL_LIST"]: vertexTypes["NORMALS"],
		classes.chunks.Chunk.IDENTIFIERS["COLOUR_LIST"]: vertexTypes["COLOURS"],
		classes.chunks.Chunk.IDENTIFIERS["MATRIX_LIST"]: vertexTypes["MATRICES"],
		classes.chunks.Chunk.IDENTIFIERS["MATRIX_PALETTE"]: vertexTypes["MATRICES"],
		classes.chunks.Chunk.IDENTIFIERS["WEIGHT_LIST"]: vertexTypes["WEIGHTS"],
		classes.chunks.Chunk.IDENTIFIERS["POSITION_LIST"]: vertexTypes["POSITION"],
	}

	uvTypeMap = [
		vertexTypes["UVS"],
		vertexTypes["UVS_2"],
		vertexTypes["UVS_3"],
		vertexTypes["UVS_4"],
		vertexTypes["UVS_5"],
		vertexTypes["UVS_6"],
		vertexTypes["UVS_7"],
		vertexTypes["UVS_8"],
	]

	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		version = binaryReader.readUInt32()

		shaderName = binaryReader.readPure3DString()

		primitiveType = binaryReader.readUInt32()

		# Note: This is the Vertex Type, this is not stored
		#      because it is determined when writing the chunk.
		binaryReader.readUInt32()

		numberOfVertices = binaryReader.readUInt32()

		numberOfIndices = binaryReader.readUInt32()

		numberOfMatrices = binaryReader.readUInt32()

		return {
			"version":version,
			"shaderName":shaderName,
			"primitiveType":primitiveType,
			"numberOfVertices":numberOfVertices,
			"numberOfIndices":numberOfIndices,
			"numberOfMatrices":numberOfMatrices,
			"data": options["data"],
		}

	def __init__(self, options : OldPrimitiveGroupChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["OLD_PRIMITIVE_GROUP"],
				"children": options["children"] if "children" in options else None,
			})
		
		self.version = options["version"]
		self.shaderName = options["shaderName"]
		self.primitiveType = options["primitiveType"]
		self.numberOfVertices = options["numberOfVertices"]
		self.numberOfIndices = options["numberOfIndices"]
		self.numberOfMatrices = options["numberOfMatrices"]
	
	def getVertexType(self) -> int:
		vertexType = 0
		uvListCount = 0
	
		for chunk in self.children:
			if chunk.identifier == classes.chunks.Chunk.IDENTIFIERS["UV_LIST"]:
				uvListCount += 1
			else:
				if chunk.identifier in OldPrimitiveGroupChunk.vertexTypeMap:
					chunkVertexType = OldPrimitiveGroupChunk.vertexTypeMap[chunk.identifier]
					vertexType |= chunkVertexType
		
		if uvListCount > 0:
			if uvListCount > 8:
				raise Exception("Old Primitive Groups can only have a maximum of 8 UV Lists.")
			
			vertexType |= OldPrimitiveGroupChunk.uvTypeMap[uvListCount - 1]
		return vertexType

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(self.version)

		binaryWriter.writePure3DString(self.shaderName)

		binaryWriter.writeUInt32(self.primitiveType)

		binaryWriter.writeUInt32(self.getVertexType())

		binaryWriter.writeUInt32(self.numberOfVertices)

		binaryWriter.writeUInt32(self.numberOfIndices)

		binaryWriter.writeUInt32(self.numberOfMatrices)