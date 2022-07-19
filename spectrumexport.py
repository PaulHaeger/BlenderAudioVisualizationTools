"""
This module contains the operator for the audio spectrum export.
"""
import bpy
import os
import numpy as np

from aud import Sound

from . audio_helpers import collect_samples_safe, blackman_harris_window


class SpectrumExport(bpy.types.Operator):
    """Export Audio Spectrum to Image Sequence"""

    bl_category = "Audio Tools"
    bl_idname = "file.export_spectrum"
    bl_label = "Export Audio Spectrum"

    _timer: None
    data: None
    time_elapsed: 0.0
    sound_length: 0.0
    samplerate: 0
    n_frames_total: 0
    min_gain: 0.0
    inc: 0.0
    n_digits: 0
    fft_offset: 0
    fft_out_width: 0
    name_temp: ''
    fname: ''
    number_format: ''
    full_path: ''
    final_out: None
    img_mat: None
    filetype: ''

    def modal(self, context, event):
        scene = context.scene
        props = scene.spectrum_export_props
        try:
            if event.type in {'ESC'}:
                self.cancel(context)
                props.isRunning = False
                return {'CANCELLED'}

            if event.type == 'TIMER':
                id_start = self.id
                # Do 30 Frames per chunk
                while(self.time_elapsed <= self.sound_length and self.id < id_start + 30):
                    output = bpy.data.images.new(self.name_temp,
                                                 self.final_res,
                                                 props.hist+1
                                                 )
                    # Do processing
                    # Move old entries back in history
                    if props.hist:
                        # We keep historic entries
                        self.img_mat[1:, :, :] = self.img_mat[0:-1, :, :]

                    # Calculate new center
                    center_idx = int(self.time_elapsed * self.samplerate)

                    # Get the to be processed samples
                    to_process = collect_samples_safe(self.data,
                                                      center_idx,
                                                      props.window_size,
                                                      dtype=np.float32)
                    # Apply window
                    blackman_harris_window(to_process)

                    # Calculate the spectrum
                    spectrum = np.fft.rfft(to_process,
                                           props.window_size + props.zero_extension
                                           )
                    spectrum /= props.window_size

                    freqs = np.abs(spectrum)
                    phases = np.angle(spectrum)/(2*np.pi)

                    nyquist = self.samplerate//2
                    if np.abs(props.boostPerOctave) > 1e-2:
                        # Apply boost
                        # b = db/octave
                        # a = gain = 10^(b/20)
                        # f = a^(log2(x)); x = frequency
                        freqs *= self.gain_per_octave**np.log2(np.linspace(0, nyquist, num=len(freqs))+1)

                    if props.use_db:
                        # Convert Data to db
                        freqs_idx = freqs > self.min_gain
                        freqs[freqs_idx] = 20*np.log10(freqs[freqs_idx])
                        freqs[~freqs_idx] = props.minimum_db

                        # Rescale from min_db-0 to 0-1
                        freqs -= props.minimum_db

                        freqs /= -props.minimum_db

                    if props.logscale:
                        # Frequencies in logspace
                        min_v = np.log(props.min_freq)/np.log(props.logbase)
                        max_v = np.log(props.max_freq)/np.log(props.logbase)
                        # Calculate evaluating positions
                        x = np.logspace(min_v,
                                        max_v,
                                        num=self.final_res,
                                        base=props.logbase
                                        )

                        # Create Array of original sample positions
                        xp = np.linspace(0, nyquist, num=len(freqs))

                        # Interpoliate data
                        res_f = np.interp(x, xp, freqs, left=0, right=0)
                        freqs = res_f

                        res_p =  np.interp(x, xp, phases, left=0, right=0)
                        phases = res_p

                    if props.bassRollOff:
                        # Apply rolloff
                        rolloffLen = int(self.final_res*.08)
                        if rolloffLen > 0:
                            # Rolloff is an upside down parabola -(x-1)^2+1
                            # Quadratic looks better than linear
                            freqs[0:rolloffLen] *= 1 - (np.linspace(-1, 0, num=rolloffLen)**2)

                    if props.time_smoothing:
                        # Apply time smoothing
                        # Average phases and frequencies
                        temp = freqs.copy()
                        freqs[self.fft_offset:] *= .5
                        freqs[self.fft_offset:] += .5 * self.pingpong[:, 0]
                        self.pingpong[:, 0] = temp[self.fft_offset:]
                        temp = phases.copy()
                        phases[self.fft_offset:] *= .5
                        phases[self.fft_offset:] += .5 * self.pingpong[:, 1]
                        self.pingpong[:, 1] = temp[self.fft_offset:]

                    # Save spectrum data in red
                    self.img_mat[0, :, 0] = freqs[self.fft_offset:]

                    # Save phase data in green
                    self.img_mat[0, :, 1] = phases[self.fft_offset:]

                    # Write pixel data
                    output.pixels.foreach_set(self.img_mat.ravel())
                    output.update()

                    # Save data to filepath

                    path = f"{self.full_path}{self.number_format.format(self.id)}.{self.filetype}"
                    # Remove old file if it exists
                    try:
                        os.remove(path)
                    except FileNotFoundError:
                        pass

                    output.filepath_raw = path

                    output.file_format = "PNG"
                    output.save()
                    bpy.data.images.remove(output)

                    # Advance time
                    self.time_elapsed += self.inc
                    self.id += 1

                # Update Progress bar
                props.progress = int((self.id-1)/self.n_frames_total*100)
                context.area.tag_redraw()
                context.area.tag_redraw()

                if self.time_elapsed > self.sound_length:
                    # We are finished
                    # Remove temp file

                    # Point to the first Element
                    self.final_out.filepath = f"{self.full_path}{self.number_format.format(1)}.{self.filetype}"
                    self.final_out.colorspace_settings.name = "Non-Color"
                    self.final_out.reload()
                    # Set to image sequence
                    self.final_out.source = "SEQUENCE"
                    props.isRunning = False
                    return {'FINISHED'}

            return {'PASS_THROUGH'}

        except:
            # Encoutered fatal error
            self.cancel(context)
            props.isRunning = False
            raise

    def execute(self, context):
        scene = context.scene
        props = scene.spectrum_export_props
        # Retrieve input.
        audiopath = bpy.path.abspath(props.input_sound_name)
        sound = Sound(audiopath)
        self.samplerate, channels = sound.specs

        # Calculate audio time in seconds
        self.sound_length = sound.length/self.samplerate

        # Read the samples
        self.data = sound.data()

        # Sum data to mono
        self.data = np.mean(self.data, axis=1)

        if props.normalize:
            # Normalize Data
            smax = np.max(np.abs(self.data))
            if smax > 1e-9:
                self.data /= smax

        self.data *= 10**(props.gain/20)

        self.min_gain = 10**(props.minimum_db/20)

        # Calculate time increment per second
        self.inc = 1/props.fps

        # Calculate total amount of required frames
        self.n_frames_total = int(self.sound_length/self.inc) + 1

        # Calculate amount of digits needed to represent all framenumbers
        self.n_digits = int(np.floor(np.log10(self.n_frames_total))) + 1

        self.fft_offset = 0 if props.keep_dc_offset or props.logscale else 1
        self.fft_out_width = (props.window_size + props.zero_extension)//2 + (1-self.fft_offset)
        self.final_res = self.fft_out_width if not props.logscale else props.n_output

        filename_sanitized = bpy.path.clean_name(
                                bpy.path.basename(props.input_sound_name)
                                ) + "_fft"

        if not props.autoGenerateName:
            filename_sanitized = bpy.path.clean_name(props.image_name)

        buffer_name = f"{filename_sanitized}"
        self.full_path = f"{props.write_path}/{buffer_name}_"
        self.number_format = "{0:0"+str(self.n_digits)+"d}"
        self.filetype = "png"

        os.makedirs(props.write_path, exist_ok=True)

        # Create output image buffer, also used for creating the files
        self.name_temp = f"{filename_sanitized}_spectrum_temp"
        self.fname = f"{filename_sanitized}"
        self.gain_per_octave = 10**(props.boostPerOctave/20)

        if self.name_temp in bpy.data.images.keys():
            # Remove image to make sure we are using the right dimensions
            bpy.data.images.remove(bpy.data.images[self.name_temp])

        # Create final output image if not exists
        if self.fname not in bpy.data.images.keys():
            self.final_out = bpy.data.images.new(self.fname,
                                                 self.final_res,
                                                 props.hist+1
                                                 )
        else:
            self.final_out = bpy.data.images[self.fname]

        self.id = 1

        # Allocate pixel matrix
        self.img_mat = np.zeros((props.hist+1, self.final_res, 4),
                                dtype=np.float32
                                )
        self.time_elapsed = 0

        if props.time_smoothing:
            self.pingpong = np.zeros((self.final_res, 4),
                                     dtype=np.float32
                                     )

        props.isRunning = True
        props.progress = 0

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
