# Blender Audio Tools

This Blender addon provides functionality for the export of information out
of audio.

I wrote this addon as I seeked a way to do audio visualisation in Blender.

The currently only a spectrum export is possible, but more features will follow.

## How to install

Go to the releases tab on the right and download the zip from the latest release.
Then open Blender, go to `Edit` then to `Preferences`. Inside the Preferences 
go to the `Addons` tab and click `Install` button located in the top right corner.
Now select the zip file you just downloaded and confirm.

After that the Addon `Audio Visualization Tools` will appear.
Check it in order to enable the Addon.

## Usage

If you go to the UV or Image Editor and open the right Panel (`N` by default)
you will see a new tab added.
The tab is called `Audio Tools`.

In this tabs you will currently only find one Panel called "Generate Audio Spectrum"

### Generate Audio Spectrum

This Tool exports a frequency spectrum from an Audio File as an image sequence.

Upon opening the panel you will see a lot of options.

The first Option `Audio File` expects the path to your desired audio file as an input.
If the Audio File cannot be read by Blender then a warning will be displayed.

Next up are the options `Window Size` and `Zero Extension`. These two options
control the behaviour of the Fourier Transform.
Below these two options the total size is displayed.
It is the sum of the window size and zero extension.
If the total size is not a power of two (e.g. 512, 1024, 2048, 4096, etc.) then
there is a warning displayed. Additionally the warning will tell you how much needs to
be added or removed to get to the nearest power of two.

The window size controls the spectral accuracy of the Fourier transform. Higher values
will give you a much more accurate and detailed result. This however comes at the cost
of time accuracy, meaning that for higher values future and past events will 'bleed' into
the current spectrum.

The zero extension controls the smoothness of the result. Higher values will increase the
resolution and optimally smooth out the results. Increase this is if you want to increase
the resolution without loosing time accuracy.

Next up are various options for the resulting Image Sequence:

`Output FPS`: This sets the FPS of the resulting image sequence. Usually you want this to be the
project FPS.

`Keep Previous`: This option sets how man previous results should be stored in the image. The past
spectra will be pushed down the y axis. If there is no need to for effects that factor in previous
outputs then you can leave this at 0.

`Use Log Frequency Scale`: This checkbox sets the scaling of the output. It is checked by default.
If unchecked the frequency that is assigned to the pixel will increase linearly with x. If the box is checked
then the assigned frequency will grow exponentially with x. This represents better how we perceive pitch and
is thus commonly used in spectral visualizers for musical purposes. For most musical purposes you want to keep
that box checked, unless you need to accurately access very specific frequencies.

`Keep DC Offset`: This option is only available when a linear frequency scale is used. If checked the
value at frequency 0 (DC Offset) will be kept. If not it will be dropped in the output making the final
resolution of the image even.

The next sub box only applies if the logarithmic scaling is enabled.

`Logscale`: This option selects the exponent base. Common choices are 10 and 2. But any option is okay
as long as its above 1.

`Min. Frequency`: This sets the frequency on x=0. 20 is the default as its considered the threshold of hearing.
Must be above 0.

`Max. Frequency`: This sets the frequency on x=1. 21050 is the default as it is the highest possible frequency
of a Audio File with a 42.1kHz samplerate. For musical purposes 2500, 5000 or 10000 can be good choices as well.

`Resolution`: This sets the resolution on the X-Axis of the final image output.

After that the box for visual options come:

`Normalize`: If true the audio will be normalized before the generation. That means the audio file
will be rescaled so that the loudest part has exactly 0dB.

`Bass Rolloff`: If true frequencies near the left edge will be faded to zero. This is usually looks better.

`Time Smoothing`: If true the current spectrum will be averaged with the previous spectrum. This prevents
1 frame movements and creates a more visually smooth appearance.

`Volume Gain`: How many dB should be added after the normalization step. This is sometimes necessary
as the normalized audio might still be to weak.

`Use dbFS scaling`: If true the output will use the dBFS loudness scale instead of the linear one.
dB better models how we perceive loudness, so its the better choice for musical purposes.

`Min. dB`: This option is only enabled if dbFS scaling is used. Must be lower than 0. In theory signals can go as low as -∞dB, however
in practice there has to be a cutoff point. -60dB is considered the threshold of hearing, however lower or higher
settings might be appropriate for your specific case. 0 in the image will represent the cutoff while 1 will present 0dB.

`db Boost per Octave`: Sometimes when generating the spectrum the higher frequencies might seem weak compared to the bass.
This setting will correct this and increase the strength of higher frequencies. Each octave will get an additional dB boost
as selected in this option. Leave at 0 if no boosting is necessary.

Next up are the final export options:

`Output dir`: Selects the directory where the images should be saved.

`Auto Generate Name`: If true the name of the image sequence will be automatically generated. Option for the lazy people.

`Image name`: If autogeneration is false, then you need to enter the name of the resulting sequence. If a sequence with
the same name exists then it will be overwritten in the export process.

And lastly there is the export button.

When pressing the button the export will start. The UI will be grayed out in the meantime and the progressbar below will track the
progress. To cancel the export press ESC.

## License

This project is licensed under the GPLv3.
The full license text can be seen in `gplv3.md`.
