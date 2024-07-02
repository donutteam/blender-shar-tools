#
# Imports
#

import struct

import data.dataSizes

#
# Class
#

class BinaryWriter:
	def __init__(self, isLittleEndian : bool = true, byteArraySize : int = 65536):
		self.isLittleEndian : bool = isLittleEndian

		self.expandSize : int = byteArraySize

		self._byteArray : bytearray = bytearray(byteArraySize)

		self._length : int = 0

		self._position : int = 0

	def getByteArray(self) -> bytearray:
		return self._byteArray[:]

	def getPosition(self) -> int:
		return self._position

	def getLength(self) -> int:
		return self._length

	def seek(self, pos : int) -> None:
		if (pos < 0 or pos >= self._length):
			raise IndexError("Position out of bounds")

		self._position = pos

	def seekOffset(self, offset : int) -> None:
		self.seek(self._position + offset)

	def writeBytes(self, data : bytes) -> None:
		self._checkSize(len(data))

		for i in range(len(data)):
			self._byteArray[self._position + i] = data[i]

		self._position += len(data)

		self._length = max(self._length, self._position)

	def writeSByte(self, value : int) -> None:
		self._checkSize(data.dataSizes.SBYTE)

		valueBytes = value.to_bytes(data.dataSizes.SBYTE, byteorder = "little", signed = True)

		self.writeBytes(valueBytes)

	def writeInt16(self, value : int) -> None:
		self._checkSize(data.dataSizes.INT16)

		valueBytes = value.to_bytes(data.dataSizes.INT16, byteorder = "little", signed = True)

		self.writeBytes(valueBytes)

	def writeInt32(self, value : int) -> None:
		self._checkSize(data.dataSizes.INT32)

		valueBytes = value.to_bytes(data.dataSizes.INT32, byteorder = "little", signed = True)

		self.writeBytes(valueBytes)

	def writeInt64(self, value : int) -> None:
		self._checkSize(data.dataSizes.INT64)

		valueBytes = value.to_bytes(data.dataSizes.INT64, byteorder = "little", signed = True)

		self.writeBytes(valueBytes)

	def writeByte(self, value : int) -> None:
		self._checkSize(data.dataSizes.BYTE)

		valueBytes = value.to_bytes(data.dataSizes.BYTE, byteorder = "little", signed = False)

		self.writeBytes(valueBytes)

	def writeUInt8(self, value : int) -> None:
		self._checkSize(data.dataSizes.UINT8)

		valueBytes = value.to_bytes(data.dataSizes.UINT8, byteorder = "little", signed = False)

		self.writeBytes(valueBytes)

	def writeUInt16(self, value : int) -> None:
		self._checkSize(data.dataSizes.UINT16)

		valueBytes = value.to_bytes(data.dataSizes.UINT16, byteorder = "little", signed = False)

		self.writeBytes(valueBytes)

	def writeUInt32(self, value : int) -> None:
		self._checkSize(data.dataSizes.UINT32)

		valueBytes = value.to_bytes(data.dataSizes.UINT32, byteorder = "little", signed = False)

		self.writeBytes(valueBytes)

	def writeUInt64(self, value : int) -> None:
		self._checkSize(data.dataSizes.UINT64)

		valueBytes = value.to_bytes(data.dataSizes.UINT64, byteorder = "little", signed = False)

		self.writeBytes(valueBytes)

	def writeFloat(self, value : float) -> None:
		self._checkSize(data.dataSizes.FLOAT32)

		valueBytes = struct.pack("<f", value)

		self.writeBytes(valueBytes)

	def writeDouble(self, value : float) -> None:
		self._checkSize(data.dataSizes.FLOAT64)

		valueBytes = struct.pack("<d", value)

		self.writeBytes(valueBytes)

	def writeString(self, value : str) -> None:
		valueBytes = value.encode("utf-8")

		# Note: writeBytes updates the length and position
		self.writeBytes(valueBytes)

	def _checkSize(self, size : int) -> None:
		requiredSize = size + self._position

		if (requiredSize >= len(self._byteArray)):
			self._expand(size)

	def _expand(self, requiredSize : int) -> None:
		newSize = len(self._byteArray) + self.expandSize

		while (len(self._byteArray) < requiredSize):
			self._byteArray.extend(bytearray(self.expandSize))