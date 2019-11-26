# reflectance
Reflectance from sio2/si and glass substrates with and without a 2D material on top

This folder contains several subfolders and a python notebook to run a sample case to estimate the refractive index of MoS2 at 400 nm.

Subfolders named with the wavelength of the excitation (in nanometer)
In each folder, there are 8 files.
The ones starting with "train" are training files
The ones starting with "test" are test files for MoS2 reflectance data

The filenames end with XY where X is either Gl or Si, Y is either S or P
Gl: glass substrate
Si: 285 nm SiO2 coated Silicon substrate
S: s-polarized light
P: p-polarized light

Please see the sample notebook to understand how the training data is created.
It assumed a wide range of complex refractive index values for the 2D material which is 0.7 nm thick.
n = [0.1:0.1:6]
k = [0:0.1:5]
