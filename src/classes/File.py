#
# Imports
#

from __future__ import annotations

import typing

import classes.chunks.RootChunk

import classes.ChunkRegistry
import classes.Pure3DBinaryReader

import instances.defaultChunkRegistry

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

class FileFromBytesOptions(typing.TypedDict):
	bytes : bytes

	chunkRegistry : classes.ChunkRegistry.ChunkRegistry | None

class FileToBytesUsingChunksOptions(typing.TypedDict):
	addExportInfo : bool | None

	littleEndian : bool | None

	chunks : list[classes.chunks.Chunk.Chunk]

class FileToBytesUsingRootChunkOptions(typing.TypedDict):
	addExportInfo : bool | None

	littleEndian : bool | None

	rootChunk : classes.chunks.RootChunk.RootChunk

class FileReadChunkOptions(typing.TypedDict):
	bytes : bytes

	chunkRegistry : classes.ChunkRegistry.ChunkRegistry

	isLittleEndian : bool

	offset : int | None

class FileReadChunkChildrenOptions(typing.TypedDict):
	bytes : bytes

	chunkRegistry : classes.ChunkRegistry.ChunkRegistry

	isLittleEndian : bool

class File:
	@staticmethod
	def fromBytes(options : FileFromBytesOptions):
		#
		# Read Buffer
		#

		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["bytes"], True)

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
			binaryReader.isLittleEndian = false
		else:
			raise Exception("Input bytes are not a P3D file.")

		#
		# Create Root Chunk
		#

		return classes.chunks.RootChunk.RootChunk(
			{
				"identifier": fileIdentifier,

				# Note: If the consumer is calling this method, it's likely that
				#	the file has been loaded from disk, so it's not a new file.
				"isNewFile": False,

				"children": File._readChunkChildren(
					{
						"bytes": options["bytes"][12:],
						"chunkRegistry": options["chunkRegistry"] if "chunkRegistry" in options else instances.defaultChunkRegistry.defaultChunkRegistry,
						"isLittleEndian": binaryReader.isLittleEndian,
					})
			})

	@staticmethod
	def toBytes(options : FileToBytesUsingChunksOptions | FileToBytesUsingRootChunkOptions) -> bytes:
		pass # TODO

	@staticmethod
	def _generateExportInfo() -> None: # TODO: Replace with classes.chunks.ExportInfoChunk.ExportInfoChunk
		pass # TODO

	@staticmethod
	def _readChunk(options : FileReadChunkOptions) -> classes.chunks.Chunk:
		#
		# Get Offset
		#

		offset = options["offset"] or 0

		#
		# Create Binary Reader
		#

		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["bytes"], options["isLittleEndian"])

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

		chunkClass = options["chunkRegistry"].getClass(identifier)

		#
		# Get Data
		#

		dataOffset = offset + 12

		data : bytes | None = None

		if dataSize > 12:
			extraDataSize = dataSize - 12

			data = options["bytes"][dataOffset : dataOffset + extraDataSize]

			dataOffset += extraDataSize

		parsedData = {}

		if (data is not None):
			binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, options["isLittleEndian"])

			parsedData = chunkClass.readData(binaryReader)

		#
		# Get Children
		#

		children : list[classes.chunks.Chunk.Chunk] = []

		if entireSize > dataSize:
			childrenDataSize = entireSize - dataSize

			childrenBytes = options["bytes"][dataOffset : dataOffset + childrenDataSize]

			children = File._readChunkChildren(
				{
					"bytes": childrenBytes,
					"chunkRegistry": chunkRegistry,
					"isLittleEndian": options["isLittleEndian"]
				})

		#
		# Return
		#

		return chunkClass(
			{
				"identifier": identifier,
				"data": parsedData,
				"children": children,

				**parsedData,
			})


	@staticmethod
	def _readChunkChildren(options : FileReadChunkChildrenOptions) -> list[classes.chunks.Chunk]:
		children : list[classes.chunks.Chunk.Chunk] = []

		offset : int = 0

		while offset < len(options["bytes"]):
			chunk = File._readChunk(
				{
					"bytes": options["bytes"],
					"chunkRegistry": options["chunkRegistry"],
					"isLittleEndian": options["isLittleEndian"],
					"offset": offset,
				})

			children.append(chunk)

			offset += chunk.getEntireSize()

		return children