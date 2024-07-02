#
# Imports
#

import struct

import data.dataSizes

#
# Class
#

class BinaryReader:
	def __init__(self, data : bytes, isLittleEndian : bool) -> None:
		self._data = memoryview(data)

		self.isLittleEndian = isLittleEndian

		self._position = 0

		self._byteOrderString = "little" if self.isLittleEndian else "big"

		self._byteOrderSymbol = "<" if self.isLittleEndian else ">"

	def getPosition(self) -> int:
		return self._position

	def getLength(self) -> int:
		return len(self._data)

	def readBytes(self, size : int) -> bytes:
		self.checkSize(size)

		valueBytes = self._data[self._position : self._position + size].tobytes()

		self._position += size

		return valueBytes

	def readFloat32(self) -> float:
		self.checkSize(data.dataSizes.FLOAT32)

		valueBytes = self.readBytes(data.dataSizes.FLOAT32)

		value = struct.unpack(self._byteOrderSymbol + "f", valueBytes)[0]

		self._position += data.dataSizes.FLOAT32

		return value

	# TODO: readFloat64 (idk how python handles 64-bit floats)

	def readSByte(self) -> int:
		self.checkSize(data.dataSizes.SBYTE)

		valueBytes = self.readBytes(data.dataSizes.SBYTE)

		value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = True)

		self._position += data.dataSizes.SBYTE

		return value

	def readInt16(self) -> int:
		self.checkSize(data.dataSizes.INT16)

		valueBytes = self.readBytes(data.dataSizes.INT16)

		value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = True)

		self._position += data.dataSizes.INT16

		return value

	def readInt32(self) -> int:
		self.checkSize(data.dataSizes.INT32)

		valueBytes = self.readBytes(data.dataSizes.INT32)

		value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = True)

		self._position += data.dataSizes.INT32

		return value

	# TODO: readInt64 (idk how python handles 64-bit integers)

	def readString(self, length : int) -> str:
		valueBytes = self.readBytes(length)

		value = valueBytes.decode("utf-8")

		return value

	def readByte(self) -> int:
		self.checkSize(data.dataSizes.BYTE)

		valueBytes = self.readBytes(data.dataSizes.BYTE)

		value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = False)

		self._position += data.dataSizes.BYTE

		return value

	def readUint16(self) -> int:
		self.checkSize(data.dataSizes.UINT16)

		valueBytes = self.readBytes(data.dataSizes.UINT16)

		value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = False)

		self._position += data.dataSizes.UINT16

		return value

	def readUint32(self) -> int:
		self.checkSize(data.dataSizes.UINT32)

		valueBytes = self.readBytes(data.dataSizes.UINT32)

		value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = False)

		self._position += data.dataSizes.UINT32

		return value

	# TODO: readUint64 (idk how python handles 64-bit integers)

	def seek(self, position : int) -> None:
		if position < 0 or position >= self.getLength():
			raise ValueError("Seek position out of range.")
		
		self._position = position

	def seekOffset(self, offset : int) -> None:
		self.seek(self._position + offset)

	def checkSize(self, neededBytes : int) -> None:
		availableBytes = self.getLength() - self._position

		if neededBytes > availableBytes:
			raise ValueError(f"Operation requires an additional { neededBytes } bytes but only { availableBytes } bytes are available.")