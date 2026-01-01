# Paper Study and Implementation Work Log

## Log Information

- **Date:** 2025-12-07
- **Developer:** Neil Taison Rigaud
- **Topic:** CleanDIFT: Diffusion Features without Noise

---

## Objective

The objective of this session is to use a Jupyter notebook to implement the new approach presented in the original paper [CleanDIFT](https://arxiv.org/pdf/2412.03439) which allows to obtain diffusion features without noise as a demonstration support for the final project presentation of the course of Introduction to Image Processing course.

---

## Tasks Checklist

- [ ] State the problem solved by this new approach and its importance
- [ ] Research the CleanDIFT method
  - [ ] What is it? Fine-tuning or full diffusion model architecture ?
  - [ ] What are the projection heads ? How are they used in CleanDIFT ?
  - [ ] How is CleanDIFT used with different timesteps with a standard diffusion backbone for different downstream tasks ?
  - [ ] How do we use frozen weights to fine-tune the feature extraction model for a specific downstream task ?
  - [ ] What are the key components in this new architecture and what are their roles ?
- [ ] Implement the CleanDIFT architecture for demonstration purpose
- [ ] Choose a suitable standard diffusion backbone for most of the experimental tasks or allow the use of SD 1.5 and SD 2.1 use in the original paper
- [ ] Using the source code from the official repository as reference, implement the core components linked to the chosen backbone along with the projection heads
- [ ] Use frozen weights for for the standard diffusion backbone(s).
  - No need to use for CleanDIFT since the fine-tuning operation takes only around 30 minutes.
- [ ] Complete the experimental setup
  - [ ] Feature extraction model fine-tuning on a random subset of the [COYO-700M dataset on Hugging Face](https://huggingface.co/datasets/kakaobrain/coyo-700m)
    - [ ] Selection of images with minimum size of 512 x 512
    - [ ] Crop and resize the image to match the corresponding input resolution of the underlying diffusion model
  - [ ] Feature extraction after U-Nets middle blocks and after U-Nets decoder blocks, except two final blocks.
    - Total of 11 feature maps
  - [ ] Point-wise feature projection heads
    - [ ] Three stacked FFNs
    - [ ] Zero-initialized to act as identity mappings due to their residual connections
  - [ ] Ensure that every feature map has its own projection head
  - [ ] Configure training parameters:
    - [ ] Adam with batch size of 8
    - [ ] Learning rate of $2e^-6$
    - [ ] **Linear warmup**
  - [ ] Stratified sampling of 3
    - Three different noise levels per training images
- [ ] Perform task-specific experiments:
  - [ ] Unsupervised semantic correspondence
    - [ ] Performance measurement in PCK
    - [ ] Use $\alpha = 0.1$ as threshold
    - [ ] Report both $PCK_{img}$ and $PCK_{bbox}$
    - [ ] Performance evaluation on **test split [SPair-71k on Hugging Face](https://huggingface.co/datasets/0jl/SPair-71k) **
      - [ ] 12k image pairs from 18 categories
    - [ ] Comparison to diffusion feature-based approach
      - [ ] [Diffusion Features](https://diffusionfeatures.github.io/)
      - [ ] [A Tale of Two Features](https://github.com/Junyi42/sd-dino)
      - [ ] [Telling Left from Right](https://telling-left-from-right.github.io/)
  - [ ] Performance in a supervised fine-tuning setting for semantic correspondence matching:
    - [ ] [Diffusion Hyperfeatures](https://github.com/diffusion-hyperfeatures/diffusion_hyperfeatures)

---

## Work Log

### [09:00] - Session Start

**Objective:** Implement CleanDIFT demonstration notebook for Image Processing course presentation.

**Observations/Discoveries:**

**Solutions applied:**

**Next Steps:**

## Technical Notes

### Dependencies

**Core Requirements:**

**Additional Libraries:**

### Configuration Changes

**Model Architecture:**

**Inference Settings:**

### Performance Considerations

---

## References

### Primary Sources

- **Paper**: [CleanDIFT: Diffusion Features without Noise](https://arxiv.org/abs/2412.03439)
- **Project Page**: https://compvis.github.io/cleandift/
- **Code Repository**: https://github.com/CompVis/cleandift
- **Pretrained Weights**: https://huggingface.co/CompVis/cleandift

### Related Work

- **DIFT**: [Diffusion Features](https://diffusionfeatures.github.io/)
- **Stable Diffusion**: [High-Resolution Image Synthesis](https://arxiv.org/abs/2112.10752)
- **TLFR**: [Telling Left from Right](https://telling-left-from-right.github.io/)
- **Diffusion Hyperfeatures**: [Searching Through Time and Space](https://arxiv.org/abs/2305.14334)

### Datasets

- **SPair-71K**: Semantic correspondence benchmark (12k pairs, 18 categories)
- **COYO-700M**: Training dataset (image-text pairs, 700M images)
- **NYUv2**: Indoor depth estimation benchmark
- **KITTI**: Outdoor depth estimation benchmark

---

## Lessons Learned

### Technical Insights

### Implementation Insights

### Research Impact

### Presentation Learnings

### Personal Takeaways

- **Adam (Adaptive Moment Estimation)** is an optimization algorithm used for training deep neural networks.
  - Gradient descent-based method that adapts learning rate for each parameter individually based on estimations of the first moment and second moments of the gradients.

---

## Future Work

### For This Project

- [ ] Run full notebook on actual GPU to verify execution
- [ ] Add failure case analysis (when does CleanDIFT struggle?)
- [ ] Compare with DINOv2 features on same tasks
- [ ] Create slide deck from notebook content
- [ ] Prepare 2-minute elevator pitch version

### Extensions

- [ ] Implement semantic segmentation demo
- [ ] Try CleanDIFT + TLFR combination
- [ ] Benchmark on SPair-71K subset
- [ ] Explore different SD backbones (SD 1.5, SDXL)
- [ ] Test on video frames (temporal consistency)

### Research Directions

- Apply to video correspondence (optical flow)
- Combine with 3D reconstruction methods
- Explore few-shot fine-tuning for specialized domains
- Investigate compression for edge deployment
- Study feature interpretability and explainability
