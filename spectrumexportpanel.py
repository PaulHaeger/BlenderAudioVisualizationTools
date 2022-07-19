"""
This module contains the UI for the spectrum export.
"""
import bpy
import aud
import numpy as np


class SpectrumExportPanel(bpy.types.Panel):
    """
    This class represents the panel UI for the spectrum export.
    """
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Audio Tools"
    bl_label = "Generate Audio Spectrum"
    bl_idname = "OPTIONS_PT_export_spectrum_panel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.spectrum_export_props

        box = layout.box()
        box.label(text="Settings")
        box.prop(props, "input_sound_name", text="Audio File")
        isReadable = False
        if props.input_sound_name:
            # Audio Filepath entered
            try:
                audiopath = bpy.path.abspath(props.input_sound_name)
                s = aud.Sound(audiopath)

                # Attempt read
                samplerate, channels = s.specs

                # Calculate audio time in seconds
                sound_length = s.length/samplerate
                # Calculate time increment per second
                inc = 1/props.fps

                # Calculate total amount of required frames
                n_frames_total = int(sound_length/inc) + 1
                isReadable = True
            except aud.error:
                # File not readable
                pass

            if not isReadable:
                row = box.row()
                row.label(text="Warning, unable to read audio file.",
                          icon="ERROR"
                          )

        # FFT Window settings
        row = box.row()
        row.prop(props, "window_size", text="Window Size")
        row = box.row()
        row.prop(props, "zero_extension", text="Zero Extension")
        row = box.row()
        # Calculate total window size
        total = props.window_size + props.zero_extension
        row.label(text=f"Total: {total}")
        row = box.row()

        # Check if the window size is a power of two
        tlog2 = np.log2(total)
        is_power_of_two = bool(abs(np.log2(total) - np.round(np.log2(total))) < 1e-7)

        if not is_power_of_two:
            # Not a power of two
            # Suggest how to get to the nearest power of two
            row.label(text="Warning: Total is not a power of two.",
                      icon="ERROR")
            # Calculate next values
            low = 2**np.floor(tlog2)
            high = 2**np.ceil(tlog2)
            if total - low < high - total:
                # The nearest power of two is reached by decreasing
                text = f"remove {int(total - low)}"
            else:
                # Nearest is reached by increasing
                text = f"add {int(high - total)}"

            row = box.row()
            row.label(text=f"To get the nearest power of two {text}.")

        # Scale and Sequence export settings
        row = box.row()
        row.prop(props, "fps", text="Output FPS")
        row.prop(props, "hist", text="Keep Previous")
        row = box.row()
        col = row.column()
        col.prop(props, "logscale", text="Use Log Frequency Scale")
        col = row.column()
        col.prop(props, "keep_dc_offset", text="Keep DC Offset")
        col.enabled = not props.logscale

        box2 = box.box()
        box2.enabled = props.logscale
        box2.label(text="Logscale Settings")
        row = box2.row()
        row.prop(props, "logbase", text="Logscale")
        row.prop(props, "min_freq", text="Min. Frequency")
        row.prop(props, "max_freq", text="Max. Frequency")
        row = box2.row()
        row.prop(props, "n_output", text="Resolution")
        if isReadable and samplerate//2 < props.max_freq:
            row = box2.row()
            row.label(text=f"Warning, any frequency above {samplerate//2} will be zero.",
                      icon="ERROR")

        # Create Box labled 'Visual'
        box2 = box.box()
        box2.label(text="Visual")
        row = box2.row()
        # Add scaling and smoothing options
        row.prop(props, "normalize", text="Normalize")
        row.prop(props, "bassRollOff", text="Bass Rolloff")
        row.prop(props, "time_smoothing", text="Time Smoothing")
        row = box2.row()
        row.prop(props, "gain", text="Volume Gain")
        row = box2.row()
        row.prop(props, "use_db", text="Use dbFS scaling")
        if props.use_db:
            row.prop(props, "minimum_db", text="Min. dB")
        row = box2.row()
        row.prop(props, "boostPerOctave", text="dB Boost per Octave")

        # Output information about the final output
        if isReadable:
            row = box.row()
            output_size = (total)//2 + (props.keep_dc_offset)
            if props.logscale:
                output_size = props.n_output
            row.label(text=f"The sequence will have {n_frames_total}\
 {output_size}x{props.hist+1} images")

        # Export Settings
        row = box.row()
        row.prop(props, "write_path", text="Output dir")
        row = box.row()
        col = row.column()
        col.prop(props, "autoGenerateName", text="Auto Generate Name")
        col = row.column()
        col.prop(props, "image_name", text="Image Name")
        col.enabled = not props.autoGenerateName
        valid_name = (props.image_name and not props.autoGenerateName) or props.autoGenerateName

        # Finally ad operator
        row = box.row()
        row.operator("file.export_spectrum", text="Generate")
        row.enabled = is_power_of_two and isReadable and valid_name
        row = box.row()
        row.prop(props, "progress", text="Progress")
        row.enabled = False

        # Gray out if running
        box.enabled = not props.isRunning
