# Intro to Image Processing - Slide Notes from Chapter 1

## What is Image Processing?

Image processing involves changing the nature of an image in order either to:

1. improve its pictorial information for human interpretation, or
   - Enhancing the edges of an image to make appear sharper
   - Edge sharpening is a vital component of printing
   - Removing noise from an image
     - Noise being random errors in the image
   - Removing blur from an image
2. render it more suitable for autonomous machine perception
   - Obtaining the edges of an image
     - Once we have the edges, we can measure their spread and the area contained within them.
   - We can also use edge-detection algorithms as a first step in edge enhancement.
   - For measurement or counting purposes, we may not be interested in all the detail in an image

## Image Sampling and Acquisition

- **Sampling** refers to the process of digitizing a continuous function
- **Nyquist criterion** states that a continuous function can be reconstructed from its samples, provided that the sampling frequency is at least twice the maximum frequency in the function.

## Images and Digital Images

- Images can be considered as being a two dimensional function $f(x, y)$
- Brightness values can be any real numbers in the range of 0.0 (black) to 1.0 (white)
- $f(x, y)$ take only integer values ranging 1 to 256 each and the brightness values ranging from 0 (black) to 255 (white)
- **Digital images** can be considered as a large array of sampled points from the continuous image
- The points on the image are called **pixels**, and they constitute the digital image.
- The pixels surrounding a pixel constitue its **neighborhood**.

## Some Applications

- Medicine
- Agriculture
- Industry
- Law enforcement

## Aspects of Image Processing

### Image enhancement

- Sharpening or deblurring an out-of-focus image,
- highlighting edges,
- improving image contract or brightening an image,
- removing noise

> [!NOTE]
> An **_out-of-focus image_** is one where the camera failed to align the focus plane with the object's plane, resulting in an image where the edges and fine details are spread out instead of crisp.

### Image restoration

- Removing of blur caused by linear motion,
- Removing of optical distortions, and
  - happens _before_ digitization, due to imperfect optics.
- removing periodic interference
  - happens _during of after_ digitization due to electrical, transmissions, or sampling issues.

### Image segmentation

- Finding lines, circles, or particular shapes in an image, and
- identifying cars, trees, buildings, or roads in an aerial photograph.

A given algorithm may be used for both image enhancement or for image restoration.

## An Image-Processing Task

Generally, an image processing task involves:

- Acquiring the image
  - Image is converted from an optical or analog signal into a digital array of pixels that can be processed.
- Preprocessing
  - Make the data uniform and suitable for analysis or inference.
- Segmentation
  - Partitioning of the image into **meaningful regions** or **objects**:
    - Edge detection
    - Thresholding
    - Region growing
    - Clustering
    - Object detection using deep learning (for ROI extraction)
  - Output is usually a **mask**, **set of regions**, or **bounding boxes** identifying where objects exist.
- Representation and description
  - Represent the _segmented regions_ into a suitable form for recognition, which could involve:
    - Geometric representation
    - Feature vectors
  - Bridges the gap between **_raw pixel regions_** and **_semantic understanding_**.
- Recognition and interpretation
  - Assigning **meaning** to the final output.
    - _Recognition_ -> labelling what each object or region is.
    - _Interpretation_ -> understanding the scene in context.
  - Often involves in modern AI pipelines a **classifier** or **object detection model**
    - Takes the representation from the _recognition and interpretation_ step and output labels, probabilities and bounding boxes.

### Region Growing and Clustering

Both **region growing** and **clustering** aim to group pixels that _belong together_, but they do it in a **very different ways** -- the first grows _locally_ while the later grows globally.

#### Region Growing

It uses one or more _seed points_, which are pixels that we are confident belongs to a certain region, then gradually add neighboring pixels that are similar according to some criterion -- typically **intensity**, **color** or **texture**.

##### How does it work?

1. Pick a seed pixel
   - Chosen manually, or automatically based on **_thresholding_**
2. Check its neighbors
3. If a neighbor's value is close enough to the seed's, it's added to the same region.
4. The process repeats recursively -- the region _grows_ until no more neighboring pixels meet the _similarity condition_.

##### Use Cases

- Medical imaging (e.g., segmenting organs or tumors)
- Satellite imagery (isolating regions such as water, forest, etc.)
- Any case where regions are spatially _coherent_ and _continuous_.

One of the key property of this segmentation method is that is respects **spatial connectivity** -- the regions it forms are always _connected blobs_.

#### Clustering

Clustering uses **_feature similarity_** instead to find pixels that belongs together. It treats all pixels as data points in a multi-dimensional space (like color channels, intensity, or texture features), then groups them by statistical closeness.

##### Example: K-Means clustering

1. Choose `k` clusters
2. Each pixel is represented as a feature vector (e.g. [R, G, B])
3. The algorithm finds `k` centroids in that feature space and assigns each pixels to the nearest one.
4. The result is that pixels with similar colors or intensities are grouped together, even if they are scattered across the image.

##### Use cases

- Color-based segmentation
- Texture classification
- Simplifying images before further analysis (quantization)

This method is **_feature-space segmentation_**, not **_spatial segmentation_**. Spatial consistency can be later enforced if needed, but clustering itself does not guarantee it.

## Types of Images

- Binary image
  - Pixel values are either 0 or 1
- Grayscale image
  - Pixel values range from 0 to 255
- True color or reg-green-blue (RGB) image
  - Use three (3) color channels (RGB)
  - Pixel values from each 8-bit channels range from 0 to 255
- Indexed image
  - Does not store actual color values in each pixel
  - Each pixel stores an index to a **color map** or **palette**
    - Each **color map** entry represents the **RGB color** associated with that index

## Image File Sizes

### 512 x 512 Binary Image

$$
\begin{align}
512 \times 512 \times 1 &= 262144 \text{bits} \\
                        &= 32768 \text{bytes (divided by 8)} \\
                        &= 32.768 \text{Kb} \\
                        &\approx 0.033 \text{Mb}

\end{align}
$$

### Grayscale Image

$$
\begin{align}
512 \times 512 \times 1 &= 262144 \text{bytes} \\
                        &= 262.14 \text{Kb} \\
                        &\approx 0.262 \text{Mb}

\end{align}
$$

### Color Image

$$
\begin{align}
512 \times 512 \times 3 &= 786432 \text{bytes} \\
                        &= 786.43 \text{Kb} \\
                        &\approx 0.786 \text{Mb}

\end{align}
$$

## Image Perception

Human visual system is limited in such way that:

- **Observed intensities** vary as to the background
- We may observe nonexistent intensities as bars in continuously varying gray levels
- Our visual system tends to undershoot or overshoot around the boundary of regions of different intensities.

> [!NOTE]
> Human eye is more sensitive to **_luminance_** than **_chrominance_**.
