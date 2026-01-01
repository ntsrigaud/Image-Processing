You are tasked with conducting a rigorous post-implementation analysis and documentation pass for a scientific paper reproduction project based on "CleanDIFT: Clean Diffusion Features without Noise." This is not a generic summary task. You must explicitly distinguish between **original authors' work** and **my independent work contributions**, using concrete evidence from code, experiments, and documentations.

1. Scope and Sources

You must analyze **all of the following**, treating them as primary sources:
- My Jupyter notebook implementation used for experiments
- My research notes and documentation in the project root
- My experimental results and logs (including timing and PCK metrics)
- The original CleanDIFT paper
- The original authors' repository and documentation (used strictly as reference, not merged)

Do **not** invent information. If something cannot be verified from the available materials, state that explicitly.

2. Step-by-Step Implementation Difference Analysis

Perform a **systematic comparison** between:
- The original CleanDIFT reference implementation
- My adapted Jupyter-based implementation

For each meaningful difference, document:
- **What was changed or reimplemented**
- **Why the change was necessary (e.g, missing models, broken assumptions, compute limits)
- **How it affects correctness, performance, or reproducibility**
- **Whether the change is purely engineering, or constitutes a methodological contribution**

This must include, but is not limited to:
- Custom implementation of SD 2.1 and SD 1.5 to support pretrained weights
- Model loading, checkpoint handling, and diffusion pipeline differences
- Sampling strategy, inference flow, and efficiency-related modifications
- Dataset subsetting decisions and their implications
- Any bug fixes, stability workarounds, or undocumented assumptions discovered

Produce this as **clear, concise technical documentation** suitable for an appendix or contribution section.

3. Explicit Attribution of Contributions

Based on the analysis above, produce a **clean separation** of contributions:

- **Original authors' contributions** (method, theory, claims)
- **My contributions**, categorized as:
  - Engineering adaptations
  - Reproducibility fixes
  - Experimental validation under constrained resources
  - Performance observations or empirical findings

Avoid exaggeration. Do not claim novelty where there is none.

4. Experimental Validation Contextualization

Analyze the experimental results with intellectual honesty:

- Clearly state the limitations imposed by the 1k-sample subset vs the paper's 12k subset
- Explain what **can** and **cannot** be concluded from the observed performance and speedups
- Justify why the results are still meaningful as a verification exercise
- Explicitly discuss uncertainty about equivalence with the original implementation

5. Presentation Preparation Guidelines

Using:

- My research notes
- My implementation documentation
- The paper (as reference only)

Produce a **structured guideline** for a PowerPoint presentation that includes:

- Motivation and problem statement
- Core ideas behind CleanDIFT
- Key related concepts (diffusion features, correspondence, inversion)
- Original authors' contributions
- My implementation challenges and solutions
- Experimental setup and results
- Limitations and lessons learned

This should be a **slide-by-slide outline** not the slide themselves.

6. Research Report Structure

Finally, generate a **concise research report outline** suitable for academic submission, including:

- Abstract
- Introduction and background
- Related concepts
- Paper summary
- Reproduction methodology
- Experimental results
- Discussion of limitations
- Explicit contribution statement
- Conclusion

The tone must be professional, precise, and factual.
Avoid unnecessary theory dumps, marketing language, or speculation.
