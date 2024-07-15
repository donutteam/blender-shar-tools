#
# Imports
#

from __future__ import annotations

from classes.chunks.RootChunk import RootChunk

from classes.ChunkRegistry import ChunkRegistry
from classes.Pure3DBinaryReader import Pure3DBinaryReader

from instances.defaultChunkRegistry import defaultChunkRegistry

#
# Constants
#

LITTLE_ENDIAN = 0xFF443350 # P3Dÿ

LITTLE_ENDIAN_COMPRESSED = 0x5A443350 # P3DZ

BIG_ENDIAN = 0x503344FF # ÿD3P

BIG_ENDIAN_COMPRESSED = 0x5033445A # ZD3P

#
# Class
#

class File:
	@staticmethod
	def fromBytes(buffer : bytes, chunkRegistry : ChunkRegistry | None = None) -> RootChunk:
		#
		# Read Buffer
		#

		binaryReader = Pure3DBinaryReader(buffer, True)

		fileIdentifier = binaryReader.readUInt32()

		#
		# Decompress File (if needed)
		#

		# TODO

		#
		# Handle Endianness
		#

		if fileIdentifier == LITTLE_ENDIAN:
			pass
		elif fileIdentifier == BIG_ENDIAN:
			binaryReader.isLittleEndian = False
		else:
			raise Exception("Input bytes are not a P3D file.")

		#
		# Create Root Chunk
		#

		return RootChunk(identifier = fileIdentifier, children = File._readChunkChildren(buffer[12:], chunkRegistry if chunkRegistry is not None else defaultChunkRegistry, binaryReader.isLittleEndian))

	@staticmethod
	def toBytes(chunks : list[Chunk], littleEndian : bool = True) -> bytes:
		pass # TODO

	@staticmethod
	def _readChunk(buffer : bytes, chunkRegistry : ChunkRegistry, isLittleEndian : bool, offset : int | None = None) -> Chunk:
		#
		# Get Offset
		#

		offset = offset if offset is not None else 0

		#
		# Create Binary Reader
		#

		binaryReader = Pure3DBinaryReader(buffer, isLittleEndian)

		binaryReader.seek(offset)

		#
		# Get Chunk Header Data
		#

		identifier = binaryReader.readUInt32()

		dataSize = binaryReader.readUInt32()

		entireSize = binaryReader.readUInt32()

		#
		# Get Chunk Class
		#

		chunkClass = chunkRegistry.getClass(identifier)

		#
		# Get Data
		#

		dataOffset = offset + 12

		rawData : bytes | None = None

		if dataSize > 12:
			extraDataSize = dataSize - 12

			rawData = buffer[dataOffset : dataOffset + extraDataSize]

			dataOffset += extraDataSize

		parsedData = []

		if (rawData is not None):
			parsedData = chunkClass.parseData(rawData, isLittleEndian)

		#
		# Get Children
		#

		children : list[Chunk] = []

		if entireSize > dataSize:
			childrenDataSize = entireSize - dataSize

			childrenBuffer = buffer[dataOffset : dataOffset + childrenDataSize]

			children = File._readChunkChildren(childrenBuffer, chunkRegistry, isLittleEndian)

		#
		# Return
		#

		return chunkClass(identifier, children, *parsedData)

	@staticmethod
	def _readChunkChildren(buffer : bytes, chunkRegistry : ChunkRegistry, isLittleEndian : bool) -> list[Chunk]:
		children : list[Chunk] = []

		offset : int = 0

		while offset < len(buffer):
			chunk = File._readChunk(buffer, chunkRegistry, isLittleEndian, offset)

			children.append(chunk)

			offset += chunk.getEntireSize()

		return children