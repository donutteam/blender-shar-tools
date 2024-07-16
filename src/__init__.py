#
# Blender Add-on Metadata
#

bl_info = {
	"name": "The Simpsons Hit & Run Tools",
	"description": "A collection of tools to help mod The Simpsons Hit & Run.",
	"author": "Donut Team",
	"version": (1, 0, 0),
	"blender": (4, 1, 1),
	"location": "TODO",
	"doc_url": "https://donutteam.com", # TODO: Actual documentation URL
	"tracker_url": "https://github.com/donutteam/blender-shar-tools/issues",
	"category": "Import-Export",
}

#
# Add Add-on Directory to Path
#

import os
import sys

sys.path.append(os.path.dirname(__file__))

#
# Imports
#

import bpy

import classes.operators.ImportPure3DFileOperator

import classes.properties.FenceProperties
import classes.properties.ShaderProperties
import classes.properties.PathProperties

#
# Initialisation
#

def register():
	print("Registered The Simpsons Hit & Run Tools.")

	classes.operators.ImportPure3DFileOperator.register()

	classes.properties.FenceProperties.register()
	classes.properties.PathProperties.register()
	classes.properties.ShaderProperties.register()

def unregister():
	print("Unregistered The Simpsons Hit & Run Tools.")

	classes.operators.ImportPure3DFileOperator.unregister()\

	classes.properties.FenceProperties.unregister()
	classes.properties.PathProperties.unregister()
	classes.properties.ShaderProperties.unregister()
