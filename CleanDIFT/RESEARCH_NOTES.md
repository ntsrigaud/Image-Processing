# CleanDIFT: Diffusion Features without Noise (Paper research and study)

## Quick Start - Demonstration Notebook

This repository contains a comprehensive demonstration of CleanDIFT for the Image Processing course final project presentation.

### What's Included

- **`cleandift.ipynb`**: Complete demonstration notebook with:
  - CleanDIFT introduction and motivation
  - Semantic correspondence matching demo
  - Depth estimation demo
  - Performance analysis vs traditional DIFT
  - Architecture insights and quantitative results

### Key Features Demonstrated

- **No noise required** - works with clean images
- **50x faster** - single forward pass vs ensemble methods
- **No hyperparameter tuning** - timestep-independent features
- **State-of-the-art** - 52% PCK on SPair-71K (semantic correspondence)
- **Multi-task** - same features for correspondence, depth, segmentation

---

# Background: DIFT and CleanDIFT

## DIFT

- Diffusion models learn powerful representations valuable for taks such as:
  - Semantic correspondence detection
  - Depth estimation
  - Semantic segmentation
  - Classification
- Without any supervision, Diffusion Features can find **correspondences** on real images across _instances_, _categories_, and even _domains_.
  - Finding correspondences between images is a fundamental problem in computer vision.
- DIFT extract the **correspondence** out of diffusion networks as image features, and use them to establish correspondence between real images.
  - **Diffusion neural networks** (diffusion models), are a type of generative model used primarily for taasks like image generation.
    - Works by progressively adding noise to data and then learning to reverse the process to create new, high-quality samples that resemble the original data.
- No fine-tuning or correspondence supervision.
- Establish reasonable and accurate _semantic correspondence_.
- Easily propagate edits from one image to others across different instances, categories and domains without any correspondence supervision.
- Competitive performance on geometric correspondence using **_small timestep $t$_**.
- Strong performance on temporal correspondence tasks.
- **Require noisy input images**.
  - Destroy information
  - Introduces the noise level as a hyperparameter that needs to be tuned for each task.

> [!NOTE]
> **Semantic correspondence** is a core computer vision task that establishes pixel-level correspondences across _instances within the same category_.

> [!NOTE]
> **Depth estimation** in diffusion models involves prediciting the depth of objects in images using advanced algorithms that leverage the principles of diffusion processes. These models can effectively handle challenging conditions and improve the accuracy of depth perception from single images by generating synthetic training data and refining depth estimates through iterative processes.

> [!NOTE]
> **Synthetic data** are artificial data created using algorithms to mimic the statistical properties of the real-world.

> [!NOTE]
> **Monocular depth estimation** is the process of estimating the distance of objects in a scene _from a single camera viewpoint_.

> [!NOTE]
> **Semantic segmentation** is a core computer vision taks that assigns a class label to every single pixel in an image, allowing the computer understand the scene's composition and the objects within it.

### CleanDIFT

![Normal Diffusion Features vs CleanDIFT Features](https://compvis.github.io/cleandift/static/images/teaser_fig.jpg)

- Enable diffusion models to work directly with clean input images.
- Showcase that the added noise in the other method has a critical impact on the usefulness of the interal features that cannot be remedied by ensembling different random noises.
- Lightweight, unsupervised fine-tuning method
- Provides high-quality and **noise-free** semantic features.
- **Timestep-independent features**
- Outperform previous diffusion features

## Diffusion Models Training

- Addition of a varying amount of noise to a clean input image (forward process)
- The model is tasked to remove this noise from the image (backward process)
- The amount of noise is dependent on the diffusion **_timestep_**.
- Different noise level require the model to perform different tasks.
- Noise addition harms the internal feature representation of diffusion models.
  - _Extractable world knowledge_

## CleanDIFT Approach

- Adapt an _off-the-shelf_ large scale pre-trained diffusion backbone to provide clean features at _minimal cost_.
  - 30 minutes of fine-tuning on a single A100 GPU
  - Improved performance across a wide range of downstream task
- Diffusion model as a family of $T$ feature extractors
  - Different noise levels
  - Provide features with different characteristics
- Consolidation of all $T$ feature extraction functions in a new feature extractor
  - Alignment of internal representations
- Provide universal features usable for various downstream-tasks in a true zero-shot manner.

### More Specifically

- Initialize the new feature extractor as a trainable copy of the diffusion model;
- Fine-tune it with clean images and no timestep input;
- Align its features with all $T$ time-dependent feature extractors of the diffusion model.

> [!NOTE]
> **Internal representation alignment** of neural networks helps ensure that their understanding and processing of information closely match human values and intentions, which is crucial for safe and effective AI behavior.

## Main Contributions

1. A finetuning approach for diffusion models that enables them to operate on clean images and makes the inherent world knowledge of these models more accessible.
2. Show how to consolidate information form all diffusion timesteps into a single feature prediction.
   - Removes the need for task-specific timestep tuning.
3. Demonstrate significant performance gains of their diffusion feature technique across a wide range of down-stream tasks.
   - Surpass the current state of the art in _zero-shot_ unsupervised semantic correspondance detection.
   - Shows that the performance gains transfer to advanced methods that fuse diffusion features or operate in a supervised setting.
4. Demonstrate significant efficiency than previous methods that tried to address this problem by noise ensembling or supervised training.

## Internal Representations Learned by Neural Networks

- A representation of a neuron is the portrayal of all its possible inputs to ouput mappings.
  - Researchers focus on a finite set of the inputs drawn from a training or validation set.
- A neuron's representation is a single vector in a high-dimensional space.
  - Response over the entire dataset and not the response of a particular layer for a single input.

For a given dataset $X = \{x_1, \dots, x_m \}$:

- A neuron's representation is a vector in a set $\mathbb{R}^m$.
- A layer of the neural network is the subspace of $\mathbb{R}^m$ spanned by its neurons' vectors.

> [!NOTE]
> Researchers compare internal representations of neural networks to be able to understand how the input data is interpreted by different kinds of networks and thereby improve the design and efficiency of future machine learning systems.

> [!NOTE]
> We use **deep representations** in neural networks because the mathematical functions used are much easier to compute using deep networks rather than shallow networks.

> [!NOTE]
> **Contrastive objective** is a training strategy that aims to learn robust and discriminative representations by emphasizing the similarity between positive pairs of data points and the dissimilarity between negative pairs.

> [!NOTE]
> Generation can also be interpreted as a pretext task for learning _expressive features_, since the model has to build up comprehensive world knowledge in order to generate plausible samples.

> [!NOTE]
> Features from diffusion models are obtained by passing a noised image through the diffusion model and extracting **intermediate feature representations**.

> [!NOTE]
> **Knowledge distillation** is a technique used to distill knowledge from a _teacher model_ into a _student model_. It is applied in diffusion models to reduce the required denoising timesteps.

## Diffusion Models

- Trained to predict a clean image $x_0$ given a noisy image $x_t$, either implicitly or explicitly.
- The noisy image is a _weighted sum_ with random Gaussian noise $x_t = \sqrt{\alpha_t}x_0 + \sqrt{1 - \alpha_t}\epsilon$ with:
  - $\alpha_t$: timestep-dependent coefficient
  - $\epsilon \sim N(0, 1)$: noise
  - $t \in [0, 1]$: timestep of the diffusion process
    - $t = 0$: clean image
    - $t = T$: pure noise
- Substantial part of the features directly depends only on the added noise.
- The model faces different objectives for different noise levels:
  - For very high noise, there is little information in the input.
    - The model generate first the coarse structure of the input image.
  - At lower noise level, more high and medium frequency information is available.
    - Shift to generate finer details and intricate structures.

### Diffusion Feature Extraction

- Happens after first adding noise to an image and passing the resulting $x_t$ to an **U-Net denoiser**.
- Features are extracted at multiple hand-picked locations of the **U-Net decoder**.
- Different level of noise added to the input image result in features beneficial for different downstream applications.
  - Application of the **Markovian process**
    - Weighted combination of the previous steps image and newly sampled Gaussian noise, governed by _noise scheduler ($\beta_t)$_.
    - Gradual corruption
    - Total noise is controllable
- _Bottleneck_ the perceptual information the model extract.

### Diffusion Feature Encode Noise

- Noise information extracted along with image information current diffusion feature's variance.
  - **CleanDIFT** eliminate noise from feature extraction process.

## CleanDIFT: Noise-Free Diffusion Features

Extracts clean diffusion features through a lightweight fine-tuning process.

### Training Setup

- Use of a frozen diffusion model and CleanDIFT feature extraction model where:
  - Noisy image is fed to the diffusion model
  - Clean image is fed to the the CleanDIFT
- Projection of CleanDIFT model's features onto noisy diffusion model given a timestep $t$.
  - Knowledge sharing to avoid re-training diffusion model.
    - Fine-tuning only

> [!IMPORTANT]
> The projection head is discarded for downstream tasks and we can directly use CleanDIFT internal representation features.

### Extraction Setup

- Train the feature extraction model to match the diffusion model's internal representations.
- Initialize the feature extraction model as a _trainable copy_ of the diffusion model.
- The objective is to obtain a single, noise-free feature map from the feature extraction model that consolidates the information of the diffusion model's timestep-dependent internal representations into a single one.
- Alignment of the diffusion features and the feature extraction model features using a _point-wise timestep conditioned_ feature projection head.
  - Process of harmonizing the internal data representations to ensure consistency and interpretability across diverse modalities and architecture.
- Projection heads can also be used to efficiently obtain feature maps for a specific timesteps by reusing the feature extraction model's internal representations and passing them through the projection heads for different $t$ values.

### Training Objective

- Consolidate the information provided by all feature extraction functions into a single joint function with the same dimensionality.
- Alignment of internal representations to maximize the similarity between the features of the two models.
  - Minimization of **cosine similarity** between extracted at different stages $k = \{1, \dots, K\}$ in the network.
- Adaptation of CleanDIFT feature map by the learned projection heads for different feature map at a stage $k$.
- Learning of a timestep-dependent alignment from CleanDIFT by the projection head to the diffusion model.
- Sampling of multiple timesteps per image
  - Allow feature extraction model to match the diffusion model's features across the entire noise spectrum.

> [!NOTE]
> **Cosine similarity** is a metric that tells us how similar or different things are.

## Experiments

- Leverage more of the world knowledge inherent in diffusion models compared to existing diffusion feature extraction methods while being **task-agnostic** and **timestep-independent**.
- Evaluation on a wide range of _downstream tasks_.
- Comparison against:
  - standard diffusion features which combines diffusion features with additional features
  - non-diffusion based approaches

### Experimental Setup

#### Implementation Details

- Evaluation on Stable Diffusion (SD) backbone **SD 1.5** and **SD 2.1**
- Feature extraction model fine-tuning on _image-caption pairs_
  - 400 steps
  - A100 GPU
- Feature extraction after U-Nets middle block and after each U-Net's decoder blocks, except two final blocks.
  - Total of 11 feature maps.
- Point-wise feature projection heads
  - Three stacked Feed Forward Networks (FFNs)
    - Zero-initialized to act as identity mappings due to their residual connections.
- Every feature map has its own projection head.
- Training using _Adam_ with batch size of 8 and a learning rate of $2e^-6$ with a **linear warmup**.
- Stratified timestep sampling = 3
  - Three different noise levels per training images.

#### Datasets

- Fine-tuning on a random subset of [COYO-700M](https://huggingface.co/datasets/kakaobrain/coyo-700m)
  - Similar to [LAION](https://www.kaggle.com/datasets/romainbeaumont/laion400m)
    - Originally used for training **SD 1.5** and **SD 2.1**
- Selection of images with minimum size of $512^2$
- Crop and resize to match the corresponding input resolution of the underlying diffusion model.

> [!NOTE]
> Semantic correspondence results using DIFT features with the standard **SD 2.1** (t = 261) and CleanDIFT features shows that CleanDIFT features have significantly less incorrect matches that the base diffusion model.

### Unsupervised Semantic Correspondence

- Performance measurement in **Percentage of Correct Keypoints (PCK)**
  - Fraction of keypoints that fall within a certain pixel distance (threshold) from the _ground-truth_ location.
    - Evaluates how precise the predicted points are.
  - Average PCK directly across all keypoints, not over images.
  - Use $\alpha = 0.1$ as threshold.
  - Report both PCK values with error margins relative to the image size and the bounding box size.
    - $\text{PCK}_{img}$ and $\text{PCK}_{bbox}$
- Performance evaluation on _test split_ of [SPair-71K](https://arxiv.org/abs/1908.10543)
  - 12k image pairs from 18 categories
  - Most challenging and most informative benchmark

#### Results

- Comparison to Duffusion feature-based approach for semantic correspondence:
  - **_DIFT_**
  - Performance increase of 1.74 absolute for $\text{PCK}_{img}$
  - Performance increase of 1.86 absolute for $\text{PCK}_{bbox}$
  - DIFT averages the extracted feature maps across 8 different noise samples.
    - Without this averaging, the performance gain is even larger.
  - The feature extraction model learns more than a mere averaging over the noise in the diffusion model's feature maps.
  - Time-step dependent performance analysis:

    ![Time-step dependent performance analysis](https://compvis.github.io/cleandift/static/images/correspondence_quantitative.png)
    - CleanDIFT consistently outperform standard diffusion features.
    - The approach generalizes to other backbones.

  - **_A Tale of Two Features_**
    - Extension of DIFT by combining diffusion features with DINOv2 features
    - Replacement of the standard diffusion features with CleanDIFT features
      - Performance gains transfers when combining CleanDIFT features with DINOv2 features
  - **_Telling Left from Right_** further improves upon the results by introducing a test-time **adaptive pose alignment** strategy.
    - Performance gain transfers to this setting as well.
    - New state-of-the-art in unsupervised zero-shot semantic correspondence matching
  - In summary, replacing CleanDIFT features consistently improves the performance across all three methods.
    ![Zero-Shot Semantic Correspondence](https://compvis.github.io/cleandift/static/images/correspondence_table.png)

- Performance in a supervised fine-tuning setting for semantic correspondence matching:
  - **Diffusion Hyperfeatures**
  - Training of an aggregation network that uses all extracted feature maps and learns to aggregate them into a _single task-specific feature map_ for semantic correspondence matching.
    - No costly DDIM inversion to obtain
    - Directly feed the clean image to the feature extraction model
    - Feature extraction is 50x faster with single denoiser forward pass
    - Slight performance regression at a speedup of 50x
      - Achieve $PCK_{img}$ value of 72.48 vs their 72.75
      - Achieve $PCK_{bbox}$ value of 64.37 vs their 64.53
    - Outperform single-step ablation of the comparative full method which requires a single forward pass
      - 9.0 percentage points for $PCK_{img}$ and 9.1 percentatage points for $PCK_{bbox}$

> [!NOTE]
> **DDIM (Denoising Diffusion Implicit Model)** is a technique in diffusion models that reverse the image process, mapping a real image back to its corresponding _noisy latent_ or initial noise seed. This allow controllable **image editing**, **manipulation** and **reconstruction** by treating the deterministic DDIM sampling as a reversible **Ordinary Differential Equation (ODE)**.

### Depth Estimation

- Estimation of monocular depth estimation on [NYUv2 dataset](https://huggingface.co/datasets/0jl/NYUv2)
- Same evaluation protocol as in [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)
- Use of SD 2.1 as the base model and resize the input to the model's native resolution of $768^2$
- Feature extraction from the same location as done in [Emergent Correspondence from Image Diffusion (DIFT)](https://diffusionfeatures.github.io/)
  - Obtention of a feature map of dimension $48^2$
- No upsampling of the features and direct application of the **linear probe**
- The probe predicts depth in 256 uniform bins which is combined with a classification loss after a linear normalization
  - Follows the same procedure as in [AdaBins: Depth Estimation Using Adaptive Bins](https://ieeexplore.ieee.org/document/9578024)
- Training of one probe for the CleanDIFT features and another for standard diffusion features at $t = 299$
  - This timestep minimizes the error in the chosen settings.

#### Results

- Substantial fidelity gap in the estimated depth maps between the features from the standard SD 2.1 backbone and the one from the feature extraction model
- The reuse of the probe trained on standard diffusion features on the CleanDIFT features, not as good as the CleanDIFT probe still achieves significantly better results when compared to standard diffusion features.
- CleanDIFT features can be used as a _drop-in_ replacement for the original diffusion features and offer improved performance on downstream aplications.

![Substantial improvement in quantitative metrics over the baseline](https://compvis.github.io/cleandift/static/images/depth_table.png)

> [!NOTE]
> A **linear probe** is a learning technique in machine learning used to assess the information content in the representation layer of a neural network.

### Semantic Segmentation

- Investigate the difference between standard noisy diffusion features and CleanDIFT features
- Evaluation on the _semantic segmentation_ task by training **linear probes** on CleanDIFT features and on on standard diffusion features.
- Use of SD 2.1 as the diffusion backbone and extract features at the same location as in [Emergent Correspondence from Image Diffusion (DIFT)](https://diffusionfeatures.github.io/)
  - Obtention of a feature map of dimension $48^2$
- Training of the linear probes on the obtained feature maps and _upscale_ the obtained segmentation masks using **nearest neighbor upsampling**.
- Training and evaluation on the [PASCAL VOC dataset](https://www.kaggle.com/datasets/gopalbhattrai/pascal-voc-2012-dataset)
- Use of **mean Intersection Over Union (mIOU)** as evaluation metric following [EmerDiff: Emerging Pixel-Level Semantic Knowledge in Diffusion Models](https://arxiv.org/abs/2401.11739)

> [!NOTE]
> A **segmentation mask** is a pixel-level map that identify and isolates specific regions or objects in an image, assigning a unique label to each pixel.

> [!NOTE]
> **Nearest neighbor upsampling** is the simplest image/data resizing method, where each pixel value from the original (low-res) grid is copied directly to a larger block of pixels in the output (high-res) grid.

#### Results

- Significantly less noise segmentations than with standard diffusion features
  - Optimal timesteps for Standard SD features around $t = 100$, which performs best quantitatively
    - Contrastively for _semantic correspondence_, the timestep is found to be $t = 261$
- CleanDIFT both alleviates the need for the _timestep tuning_ and outperforms the standard diffusion features for the optimal timestep.

### Classification

- Assess the impact of the method on _non-spatial tasks_
- Evaluation of _classification performance_ using **_pooled features_**
- Pooling mitigates the influence of _localized noise_
- Application of [k-Nearest Neighbors (kNN) Classification](https://www.ibm.com/think/topics/knn) with $k = 10$ on [ImageNet1k](https://huggingface.co/datasets/ILSVRC/imagenet-1k), using SD 1.5 as the diffusion backbone.

> [!NOTE]
> A **pooling layer** downsample and aggregrate information that is dispersed among many vectors into fewer vectors while retaining important information.

> [!NOTE]
> The **k-Nearest Neighbors (KNN)** algorithm is a _non-parametric_, supervised learning classifier, which uses proximity to make classifications or predictions about the grouping of an individual data point. It is one of the most popular and simplest classification and regression classifications used in machine learning.

#### Results

![Experiment result from sweeping across feature maps and timesteps t for the base model](https://compvis.github.io/cleandift/static/images/classification_quantitative.png)

- Feature map with the lowest spatial resolution (feature map #0) yields the highest classification accuracy.
  - Best performing feature map with $t = 100$
- CleanDIFT slightly outperform the standard diffusion features even when using an optimal timestep $t$ for the base model.
  - Showcases that it does not introduce any detrimental effects.

> [!NOTE]
> **Spatial resolution** refers to the scale or size of the smallest unit of an image capable of distinguishing objects, or the measure of the smallest angular or linear distance to identify adjacent objects in an image.

### Ablation Studies

- Performed using [DIFT](https://diffusionfeatures.github.io/)
- Performance evaluation for unsupervised zero-shot semantic correspondence matching on a subset of the [SPair71k test split](https://huggingface.co/datasets/0jl/SPair-71k)

#### Training Objective

- Maximize the cosine similarity between the projected outputs of CleanDIFT feature extraction model and the standard diffusion features to align them
- Investigate the influence of the employed method similarity metric by:
  - Comparing feature extraction models trained on three different _alignment objectives_:
    - Mean absolute error ($L_1$)
    - Mean squared error ($L_2$)
    - Cosine similarity

##### Results

- All objectives result in feature extraction models that outperform standard diffusion features
- Cosine similarity consistently performs best across the alignment objectives by a significant margin

#### Projection Heads

- Investigation of the influence of the proposed projection heads that are used to project CleanDIFT features onto standard diffusion features.
- Alignment of feature extraction model and diffusion model
  - Determined by the utilized similarity metric and projection heads.
- The projection heads are typically not used for inference
  - They add computational overhead only during lightweight fine-tuning.
  - Worthwhile to include them and leverage the small performance gain.
  - Can be used to efficiently obtain feature maps for specific timesteps.

> [!NOTE]
> An **ablation study** is a method used in machine learning and other fields to determine the importance of a component within a system by removing it and observing the effect on performance.

## Conclusion

- Introduction of a novel approach for extracting diffusion features
- CleanDIFT produces **noise-free**, **timestep-independent**, **general-purpose** diffusion features
  - By consolidaing timestep-dependent representations from a **pre-trained diffusion backbone** into a **unified feature representation**.
- Achieved alignment between CleanDIFT feature extraction model and the pre-trained diffusion backbone through a lightweight fine-tuning procedure.
  - Takes approximately 30 minutes on a single A100 GPU
- CleanDIFT eliminates the information loss associated with adding noise to input images.
- CleanDIFT removes the requirement for tuning timesteps for each downstream task.
  - Avoid the computational overhead of ensembling over noise levels or timesteps.
- CleanDIFT efficiently extract features with just a single forward pass at inference time.
  - Substantially reducing inference costs compared to methods relying on **ensembling** or **inversion**.
- Extensive evaluations of CleanDIFT across diverse downstream tasks demonstrate significant performance improvements over conventional diffusion features.

> [!NOTE]
> **Ensemble learning** is a machine learning technique that aggregates two or more learners (e.g. regression models, neural networks) in order to produce better predictions.

## Citations

```bibtex
@inproceedings{stracke2025cleandift,
    title={CleanDIFT: Diffusion Features without Noise},
    author={Nick Stracke and Stefan Andreas Baumann and Kolja Bauer and Frank Fundel and Björn Ommer},
    booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
    year={2025}
}
```

## References

- [CleanDIFT](https://compvis.github.io/cleandift/)
- [Emergent Correspondence from Image Diffusion](https://diffusionfeatures.github.io/)
- [Neural Network Diffusion](https://arxiv.org/abs/2402.13144)
- [Monocular Depth Estimation using Diffusion Models](https://arxiv.org/abs/2302.14816)
- [Internal Representation learned by Neural Networks and why They are Compared](https://medium.com/wicds/internal-representation-learned-by-neural-networks-and-why-they-are-compared-80a2a9c1e89b)
- [Representation Alignment in Neural Networks](https://arxiv.org/pdf/2112.07806)
- [Why Deep Representations? C1W4L04](https://www.youtube.com/watch?v=5dWp1mw_XNk)
- [Aligning AI Through Internal Understanding: The Role of Interpretability](https://arxiv.org/html/2509.08592v1)
- [Monocular depth estimation](https://huggingface.co/docs/transformers/en/tasks/monocular_depth_estimation)
- [U-Net Architecture explained](https://www.youtube.com/watch?v=NhdzGfB1q74)
- [What is a U-Net ?](https://www.youtube.com/watch?v=wnuWqG18FVU)
- [Cosine Similarity](https://www.youtube.com/watch?v=e9U0QAFbfLI)
- [Understanding Feed Forward Neural Networks](https://medium.com/@eastgate/understanding-feed-forward-neural-network-ca70d9e24a0d)
- [Why Warmup the Learning Rate? Underlying Mechanisms and Improvement](https://arxiv.org/abs/2406.09405)
- [SPair-71k On HuggingFace (Unofficial script)](https://huggingface.co/datasets/0jl/SPair-71k)
- [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)
- [APA: Adaptive Pose Alignment for Robust Face Recognition](https://ieeexplore.ieee.org/document/9025679)
- [DDIM Inversion](https://huggingface.co/learn/diffusion-course/unit4/2)
- [Diffusion Hyperfeatures: Searching Through Time and Space for Semantic Correspondence](https://arxiv.org/abs/2305.14334)
- [AdaBins: Depth Estimation Using Adaptive Bins](https://ieeexplore.ieee.org/document/9578024)
- [EmerDiff: Emerging Pixel-Level Semantic Knowledge in Diffusion Models](https://arxiv.org/abs/2401.11739)
- [Pooling and their types in CNN](https://medium.com/@abhishekjainindore24/pooling-and-their-types-in-cnn-4a4b8a7a4611)
- [K-Nearest Neighbors Classification](https://www.ibm.com/think/topics/knn)
- [Understanding Seeds in AI: The Key to Reproducibility and Creativity](https://medium.com/@nikunj.vaghasiya2050/understanding-seeds-in-ai-the-key-to-reproducibility-and-creativity-edcfd3bf649c)
- [What is Residual Connection?](https://medium.com/data-science/what-is-residual-connection-efb07cab0d55)
- [What is a conditional vector?](https://stats.stackexchange.com/questions/338178/gans-stackgan-paper-what-is-a-conditioning-vector)
- [Feedforward Neural Network](https://www.sciencedirect.com/topics/computer-science/feedforward-neural-network)
- [AdaNorm: Adaptive Gradient Norm Correction based on Optimizer for CNNs](https://arxiv.org/abs/2210.06364)
- [Root Mean Square Normalization (RMSNorm)](https://arxiv.org/abs/1910.07467)
- [SwiGLU Activation Function](https://abdulkaderhelwan.medium.com/swiglu-activation-function-77627e0b2b52)
- [Random Fourier Features](https://gregorygundersen.com/blog/2019/12/23/random-fourier-features/)
