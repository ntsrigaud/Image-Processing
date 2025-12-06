# Paper Study and Implementation Work Log

## Log Information

- **Date:** 2025-12-06
- **Developer:** Neil Taison Rigaud
- **Topic:** CleanDIFT: Diffusion Features without Noise

---

## Objective

The objective of this session is to use a Jupyter notebook to implement the new approach presented in the original paper [CleanDIFT](https://arxiv.org/pdf/2412.03439) which allows to obtain diffusion features without noise as a demonstration support for the final project presentation of the course of Introduction to Image Processing course.

---

## Tasks Checklist

- [ ] Conda environment setup for method implementation and experiment
  - [ ] Add conda `environment.yml` file for easy setup
  - [ ] Create environment and install libraries and dependencies
- [ ] Implement CleanDIFT feature extraction model
  - Use architecture details from the [source code](https://github.com/CompVis/cleandift/tree/main/src), architecture details notes from the README.md
- [ ] Implement feature extraction setup aligning with their orignal training objective
- [ ] Experimental setup according to the implementation details recorded in the README and original source codes
  - [ ] Stable Diffusion backbone SD 1.5 and SD 2.1 for different comparative experiments with previous approaches
  - [ ] Set up the necessary projection heads
  - [ ] Set up similar training parameters such as Adam with batch size 8 and learning rate $2^-6$ with linear warmup
  - [ ] Use stratified sample of 3, i.e tree different noise levels per training images
  - [ ] Fine-tuning on a random subset of [COYO-700M](https://huggingface.co/datasets/kakaobrain/coyo-700m)
    - [ ] Selection of images with minimum size of 512x512
    - [ ] Crop and resize the images to match corresponding input resolution of the underlying diffusion model
- [ ] Conduct all the main experiments from the paper
  - [ ] Unsupervised Semantic Correspondence
    - [ ] Performance measurement using Percentage of Correct Keypoints (PCK)
      - Average of PCK directly across all keypoints, not over images.
      - Use $\alpha = 0.1$
    - [ ] Performance evaluation on test split of [SPair-71K](https://arxiv.org/abs/1908.10543)
      - [ ] Obtain the same dataset configuration used in the paper for result accuracy
      - [ ] Use 12k image pairs from 18 categories
    - [ ] Compare with standard [DIFT](https://diffusionfeatures.github.io/) approach
      - [ ] Perform time-step dependent performance analysis
    - [ ] Compare with **A Tale of Two Features** approach
      - [ ] Check if this implementation of an extension of DIFT by combining diffusion features with DINOv2 features is available for direct usage
        - If yes, use it, otherwise implement it before proceeding to perform comparison with CleanDIFT
      - [ ] Replace the standard diffusion features with CleanDIFT features for comparison
    - [ ] Compare with **Telling Left from Right** approach
      - [ ] Check if this implementation is available for direct usage
        - If yes, use it, otherwise implement it before proceeding to perform comparison with CleanDIFT
      - [ ] Replace the standard diffusion features with CleanDIFT features for comparison
    - [ ] Compare the performance in supervised fine-tuning setting for semantic correspondence matching
      - [ ] Compare new approach with [Diffusion Hyperfeatures: Searching Through Time and Space for Semantic Correspondence](https://arxiv.org/abs/2305.14334)
      - [ ] Verify that feature extraction is actually 50x faster with single denoiser forward pass using CleanDIFT
      - [ ] Verify that there is a slight performance regression of CleanDIFT using PCK metrics
      - [ ] Compare performance in single-step ablation of the comparative full method requiring single forward pass
    - [ ] Provide appropriate graphs for the comparison with diffusion feature-based approach on this task
  - [ ] Depth estimation
  - [ ] Semantic Segmentation
  - [ ] Classification
  - [ ] Ablation Studies
- [ ] Provide experiment takeaways

---

## Work Log

### [16:00] - Session Start

**Observations/Discoveries:**

- **Issues encountered:**

- **Solutions applied:**

## Technical Notes

### Dependencies

List any new dependencies added or version changes.

### Configuration Changes

Note any configuration file changes or environment variable updates.

### Performance Considerations

Document any performance impacts or optimizations made.

---

## References

- Documentation: [link]
- External resources: [link]

---

## Lessons Learned

What did you learn during this session? Any insights for future work?

-
