"""
This module contains the necessary properties for the audio export
"""
import bpy
from bpy.props import BoolProperty, FloatProperty, IntProperty, StringProperty

class SpectrumExportProperties(bpy.types.PropertyGroup):
    """
    This class keeps a multitude of properties for the spectrum export.
    """

    input_sound_name: StringProperty(name="Sound File",
                                     description="Path of the sound file.",
                                     subtype="FILE_PATH")

    window_size: IntProperty(name="Window Size",
                             description="Number of samples that are used for the spectrum generation. Higher values will result in higer resolution at the expense of time accuracy.",
                             default=1024,
                             min=32) #1024

    zero_extension: IntProperty(name="Window Zero Extension",
                                description="Adds zeros after the samples. Higher values will create images in higher resolution with interpoliated values.",
                                default=1024,
                                min=0)

    fps: FloatProperty(name="FPS",
                       description="How many FPS the generated sequence will have.",
                       default=30,
                       min=1)

    hist: IntProperty(name="Keep Previous",
                      description="How many previous spectra should be saved. Results will be shifted down 1 on the y-axis.",
                      default=0,
                      min=0)

    keep_dc_offset: BoolProperty(name="Keep DC Offset",
                                 default=False)

    write_path: StringProperty(name="Sequence Write Path",
                               description="Filepath the generated images will be written to.",
                               default="./fftimg/",
                               subtype="DIR_PATH")

    use_db: BoolProperty(name="Use dB instead of Gain",
                                   description="Values will be in dbFS scaling instead of linear one. This is the correct choice for most musical applications.",
                                   default=True) # Output dbFS values instead of gain values

    minimum_db: FloatProperty(name="Minimum dB",
                              description="This value will be intensitiy 0 in the image.",
                              default=-18,
                              max=-3) # Zero in the image will represent this dbFS level

    logscale: BoolProperty(name="Logarithmic Frequency Scaling",
                           description="If true the frequencies displayed in a logplot fashion. This is the right choice for most musical application.",
                           default=True)

    logbase: IntProperty(name="Log Base",
                         description="Sets the log base for the logarithmic scaling.",
                         default=10,
                         min=2)

    min_freq: FloatProperty(name="Mininmal Frequecy",
                            description="Sets the smallest frequency to be displayed. Only works if Logarithmic Scale is on.",
                            default=20,
                            min=1)

    max_freq: FloatProperty(name="Maximal Frequecy",
                            description="Sets the highest frequency to be displayed. Only works if Logarithmic Scale is on.",
                            default=21050,
                            min=1,
                            max=100000)

    normalize: BoolProperty(name="Normalize Audio",
                           description="If true the absolute of the highest sample in the audio will be 1. Everything will be scaled accordingly.",
                           default=True)

    n_output: IntProperty(name="Output Resolution", description="Number of Pixels, only has an effect in logscale", default=2048)

    gain: FloatProperty(name="Audio Gain",
                       description="Audio gain after normalization in dB.",
                       default=0,
                       min=-60,
                       max=100)

    progress: FloatProperty(name="Progress",
                            subtype="PERCENTAGE",
                            soft_min=0,
                            soft_max=100,
                            precision=0)

    isRunning: BoolProperty(name="Is Running", default=False)

    autoGenerateName: BoolProperty(name="Autogenerate Name",
                                   description="If true the output name will be auto generated.",
                                   default=False)

    image_name: StringProperty(name="Name of the sequence",
                               description="Name of the sequence if not auto generated.",
                               )

    bassRollOff: BoolProperty(name="Apply Rolloff",
                                   description="If true there will be a rolloff applied at the left border.",
                                   default=True)

    time_smoothing: BoolProperty(name="Time Smoothing",
                                   description="If true the position will be averaged to make the motion smoother.",
                                   default=False)

    boostPerOctave: FloatProperty(name="High Frequency Boost",
                                  description="Sets how much dB per octave should be added. This can be used to make higer frequencies stronger if they are too weak",
                                  default=0)
