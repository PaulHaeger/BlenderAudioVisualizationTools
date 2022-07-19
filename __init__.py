import bpy
from bpy.props import PointerProperty

from . spectrumexportproperties import SpectrumExportProperties
from . spectrumexport import SpectrumExport
from . spectrumexportpanel import SpectrumExportPanel

# Configuration Values

bl_info = {
    "name": "Audio Visualization Tools",
    "blender": (3, 2, 1),
    "category": "Sound",
    }


def register():
    bpy.utils.register_class(SpectrumExport)
    bpy.utils.register_class(SpectrumExportPanel)
    bpy.utils.register_class(SpectrumExportProperties)
    bpy.types.Scene.spectrum_export_props = PointerProperty(type=SpectrumExportProperties)


def unregister():
    bpy.types.Scene.spectrum_export_props = None
    bpy.utils.unregister_class(SpectrumExport)
    bpy.utils.unregister_class(SpectrumExportPanel)
    bpy.utils.unregister_class(SpectrumExportProperties)


if __name__ == "__main__":
    register()
