#
# Imports
#

import classes.chunks.Chunk
import classes.chunks.Fence2Chunk
import classes.chunks.FenceChunk
import classes.chunks.HistoryChunk

import classes.ChunkRegistry
import classes.chunks.ImageChunk
import classes.chunks.ImageDataChunk
import classes.chunks.IndexListChunk
import classes.chunks.MeshChunk
import classes.chunks.OldPrimitiveGroupChunk
import classes.chunks.PositionListChunk
import classes.chunks.ShaderChunk
import classes.chunks.ShaderColourParameterChunk
import classes.chunks.ShaderFloatParameterChunk
import classes.chunks.ShaderIntegerParameterChunk
import classes.chunks.ShaderTextureParameterChunk
import classes.chunks.TextureChunk
import classes.chunks.UVListChunk

#
# Default Chunk Registry
#

defaultChunkRegistry = classes.ChunkRegistry.ChunkRegistry()

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["HISTORY"], classes.chunks.HistoryChunk.HistoryChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["FENCE"], classes.chunks.FenceChunk.FenceChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["FENCE_2"], classes.chunks.Fence2Chunk.Fence2Chunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["MESH"], classes.chunks.MeshChunk.MeshChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["OLD_PRIMITIVE_GROUP"], classes.chunks.OldPrimitiveGroupChunk.OldPrimitiveGroupChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["POSITION_LIST"], classes.chunks.PositionListChunk.PositionListChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["INDEX_LIST"], classes.chunks.IndexListChunk.IndexListChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["TEXTURE"], classes.chunks.TextureChunk.TextureChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["IMAGE"], classes.chunks.ImageChunk.ImageChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["IMAGE_DATA"], classes.chunks.ImageDataChunk.ImageDataChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["UV_LIST"], classes.chunks.UVListChunk.UVListChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["SHADER"], classes.chunks.ShaderChunk.ShaderChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["SHADER_COLOUR_PARAMETER"], classes.chunks.ShaderColourParameterChunk.ShaderColourParameterChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["SHADER_FLOAT_PARAMETER"], classes.chunks.ShaderFloatParameterChunk.ShaderFloatParameterChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["SHADER_INTEGER_PARAMETER"], classes.chunks.ShaderIntegerParameterChunk.ShaderIntegerParameterChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["SHADER_TEXTURE_PARAMETER"], classes.chunks.ShaderTextureParameterChunk.ShaderTextureParameterChunk)