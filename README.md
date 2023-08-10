# Cartoonifier

## Description
This is a simple cartoonifier that uses OpenCV to apply cartoon effects to images. Images are taken from the webcam or from a file. The cartoonifier uses bilateral filtering, edge detection, and color quantization to achieve the cartoon effect.

## Usage
To run the cartoonifier with the default settings, simply run the script with no arguments. The script will use the webcam to capture images and apply the cartoon effect to them. To use a file instead of the webcam, use the `-i` flag and specify the path to the file. To see all available options, use the `-h` flag.
```
python cartoonifier.py [-h] [-i PATH]
```

## Requirements
Python installed with the following packages:
- numpy
- opencv-python
- argparse