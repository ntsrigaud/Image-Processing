# Intro to Image Processing - Slide Notes from Chapter 2

## Vector vs Raster Images

- We may store image information in two different ways:
  - **Vector images**
    - Collection of lines or vectors
    - Can be magnified to any desired size without losing any _sharpness_
    - Not good for natural scenes representation
  - **Raster images**
    - Collection of dots
- The great bulk of image file formats store images as raster information

> [!NOTE]
> Even though **vector images** are more memory efficient for simple contents, a file can become heavier than a raster version once you try to represent complex, photo-realistic scenes.

### Key Differences

- **Scalability**
  - Vectors scale indefinitely; rasters don't.
- **Editing**
  - Vectors are editable at an object level;
  - Rasters are editable per pixel.
- **Rendering**
  - Rasters display exactly as stored;
  - Vectors must be _rendered_ before display or printing.
    - Rendering -> Conversion into pixels
- **Performance**
  - Raster images are typically faster to display at native resolution; vectors require rasterization before display (cost depends on scene complexity)
  - Vectors need processing power to interpret shapes.
- **Color representation**
  - Raster formats directly store color values per pixel;
  - Vectors use fills, strokes, and gradients mathematically defined.

> [!NOTE]
> When considering which format to use, it is less about which is _better_ and more about which one is _more efficient_ for your task.

### Image Files and Formats

- **Bitmap** (raster image)
  - Digital representation of an image in the form of grid of pixels
  - Common in digital imaging, GUIs, and photography
  - Pixel data and corresponding brightness
- **Vectors**
  - Image data stored as vectors
  - Store only key points
  - Often used in processing programs

### A Simple Raster Format

As well as containing all pixel information, an image file must contain some **header information**. This usually includes:

- Size of the image
- Some documentation
- A color map
- Compression used

> [!NOTE]
> **PGM format** was designed to be a _generic format_ used for conversion between other formats.

### GIF and PNG

#### GIF

- Colors are stored using a color map
  - GIF specification allows a maximum of 256 colors per image
- GIF uses an indexed palette (up to 256 colors); grayscale or 1‑bit images can be represented via palette entries (no native grayscale colorspace)
- Pixel data is compressed using **_LZW (Lempel-Ziv-Welch) compression_**
- Allows multiple images per file
  - Can be used to create animated GIFs

> [!NOTE]
> **LZW compression** is a _lossless data compression_ that reduces file size by replacing repeated sequences of data with shorter codes. It is commonly used in GIF and TIFF, and works by building a dictionary of sequences as it processes the input data.

#### PNG

- Designed to replace GIF
  - Overcome some of GIF's disadvantages
- Does not rely on any patented algorithms
- Supports more image types than GIF
- Supports grayscale, true color, and indexed images
- Uses lossless DEFLATE (**zlib**) compression; actual compression depends on image content and may not always reduce file size

### JPEG

- JPEG algorithm uses _lossy compression_
  - Not all the original data can be recovered

### TIFF

- One of the most _comprehensive_ image formats
- Can store multiple images per file
- Allows different compression routines and different byte orderings
- Allows binary, grayscale, true color, indexed images, and opacity or transparency
- An excellent format for data exchange

### DICOM

- Digital Imaging and Communications in Medicine (DICOM)
- Like GIF, may hold multiple images per file
- May be considered as slices or frames of a _3D object_
- DICOM specification is huge and complex
  - Published drafts available on the Web
