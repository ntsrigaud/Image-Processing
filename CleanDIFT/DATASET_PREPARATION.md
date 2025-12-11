# CleanDIFT Dataset Preparation Guide

## Quick Start: Download Proper Training Data

### Option 1: Using HuggingFace Datasets (Recommended)

```python
from datasets import load_dataset
import os
from PIL import Image
import requests
from io import BytesIO
import json
from tqdm.auto import tqdm

def download_coyo_subset(
    output_dir="./data/train_large",
    num_images=10000,
    min_size=512,
    max_workers=8
):
    """
    Download a proper subset of COYO-700M for CleanDIFT training.

    Args:
        output_dir: Where to save images and captions
        num_images: Number of images to download
        min_size: Minimum image dimension (width or height)
        max_workers: Parallel download workers
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading COYO-700M dataset (streaming mode)...")
    dataset = load_dataset(
        "kakaobrain/coyo-700m",
        streaming=True,
        split="train"
    )

    successful = 0
    failed = 0
    skipped = 0

    pbar = tqdm(total=num_images, desc="Downloading images")

    for idx, item in enumerate(dataset):
        if successful >= num_images:
            break

        try:
            # Get image URL and caption
            img_url = item['url']
            caption = item['text']

            # Download image
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content)).convert('RGB')

            # Filter by size
            width, height = img.size
            if min(width, height) < min_size:
                skipped += 1
                continue

            # Save image
            img_path = os.path.join(output_dir, f"img_{successful:05d}.jpg")
            img.save(img_path, quality=95)

            # Save caption
            caption_path = os.path.join(output_dir, f"img_{successful:05d}.json")
            with open(caption_path, 'w') as f:
                json.dump({"caption": caption, "url": img_url}, f)

            successful += 1
            pbar.update(1)

        except Exception as e:
            failed += 1
            if failed % 100 == 0:
                print(f"Failed: {failed}, Skipped: {skipped}")
            continue

    pbar.close()
    print(f"\nSuccessfully downloaded {successful} images")
    print(f"  Failed: {failed}")
    print(f"  Skipped (too small): {skipped}")
    print(f"  Saved to: {output_dir}")

# Usage
download_coyo_subset(
    output_dir="./data/train_large",
    num_images=10000,  # 10K images
    min_size=512
)
```

### Option 2: Pre-filtered URLs List

If HuggingFace datasets is slow or blocked, use a pre-filtered list:

```python
def download_from_url_list(url_file, output_dir="./data/train_large"):
    """
    Download images from a text file containing URLs and captions.

    Format of url_file (one per line):
    https://example.com/image.jpg|||Caption text here
    """
    with open(url_file, 'r') as f:
        lines = f.readlines()

    os.makedirs(output_dir, exist_ok=True)
    successful = 0

    for idx, line in enumerate(tqdm(lines)):
        try:
            url, caption = line.strip().split('|||')

            response = requests.get(url, timeout=10)
            img = Image.open(BytesIO(response.content)).convert('RGB')

            if min(img.size) < 512:
                continue

            img.save(f"{output_dir}/img_{successful:05d}.jpg")
            with open(f"{output_dir}/img_{successful:05d}.json", 'w') as f:
                json.dump({"caption": caption}, f)

            successful += 1

        except:
            continue

    print(f"Downloaded {successful} images")
```

---

## Dataset Size Recommendations

Based on paper and practical considerations:

| Purpose            | Images | Training Time | Expected Quality |
| ------------------ | ------ | ------------- | ---------------- |
| **Quick Test**     | 1,000  | ~30 min       | Poor             |
| **Minimum Viable** | 5,000  | ~2 hours      | Acceptable       |
| **Paper Spec**     | 10,000 | ~4 hours      | Good             |
| **High Quality**   | 50,000 | ~20 hours     | Excellent        |

For reproducing paper results, aim for **at least 10,000 images**.

---

## Improved DataLoader

Replace the current DummyDataset with this improved version:

```python
import torch
import torch.utils.data as data
from PIL import Image
from torchvision import transforms
import json
import os

class COYODataset(data.Dataset):
    """
    Dataset for CleanDIFT training matching paper specifications.
    """
    def __init__(
        self,
        dataset_dir: str,
        img_size: int = 512,
        min_size: int = 512,
        train: bool = True
    ):
        self.dataset_dir = dataset_dir
        self.img_size = img_size
        self.min_size = min_size
        self.data = []

        # Load all image-caption pairs
        jpg_files = sorted([f for f in os.listdir(dataset_dir) if f.endswith('.jpg')])

        for img_file in jpg_files:
            img_path = os.path.join(dataset_dir, img_file)
            json_path = os.path.join(dataset_dir, img_file.replace('.jpg', '.json'))

            if not os.path.exists(json_path):
                continue

            # Filter by image size (as per paper)
            try:
                img = Image.open(img_path)
                if min(img.size) < self.min_size:
                    continue
            except:
                continue

            # Load caption
            with open(json_path, 'r') as f:
                json_data = json.load(f)

            self.data.append({
                'img_path': img_path,
                'caption': json_data.get('caption', '')
            })

        print(f"Loaded {len(self.data)} valid images from {dataset_dir}")

        # Data augmentation (paper uses crop + resize)
        if train:
            self.transform = transforms.Compose([
                transforms.RandomCrop(min(img_size, 512)),
                transforms.Resize((img_size, img_size)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.ToTensor(),
                transforms.Normalize([0.5], [0.5])  # To [-1, 1]
            ])
        else:
            self.transform = transforms.Compose([
                transforms.CenterCrop(min(img_size, 512)),
                transforms.Resize((img_size, img_size)),
                transforms.ToTensor(),
                transforms.Normalize([0.5], [0.5])
            ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        # Load image
        img = Image.open(item['img_path']).convert('RGB')
        img = self.transform(img)

        return {
            'image': img,
            'caption': item['caption']
        }


class DataModule:
    def __init__(
        self,
        dataset_dir: str,
        batch_size: int = 8,
        img_size: int = 512,
        num_workers: int = 4
    ):
        self.batch_size = batch_size
        self.num_workers = num_workers

        train_dataset = COYODataset(
            dataset_dir=dataset_dir,
            img_size=img_size,
            train=True
        )

        self.train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=True,
            drop_last=True  # Important for consistent batch sizes
        )

        print(f"DataLoader created:")
        print(f"  Batch size: {batch_size}")
        print(f"  Num workers: {num_workers}")
        print(f"  Total batches: {len(self.train_loader)}")

    def train_dataloader(self):
        return self.train_loader
```

---

## Usage in Training

```python
# 1. Download dataset (run once)
download_coyo_subset(
    output_dir="./data/train_large",
    num_images=10000,
    min_size=512
)

# 2. Create dataloader
data_module = DataModule(
    dataset_dir="./data/train_large",
    batch_size=8,  # Or 4 if memory constrained
    img_size=512,
    num_workers=2  # Colab: use 2, Local: use 4-8
)

train_dataloader = data_module.train_dataloader()
```

---

## Verification

After downloading, verify your dataset:

```python
import os
import json
from PIL import Image

def verify_dataset(dataset_dir):
    """Verify dataset quality and statistics."""
    jpg_files = [f for f in os.listdir(dataset_dir) if f.endswith('.jpg')]

    print(f"Total images: {len(jpg_files)}")

    sizes = []
    has_caption = 0

    for jpg_file in jpg_files[:100]:  # Sample first 100
        # Check image
        img_path = os.path.join(dataset_dir, jpg_file)
        img = Image.open(img_path)
        sizes.append(min(img.size))

        # Check caption
        json_path = img_path.replace('.jpg', '.json')
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
                if data.get('caption'):
                    has_caption += 1

    print(f"Min image size (sampled): {min(sizes)}")
    print(f"Avg image size (sampled): {sum(sizes)/len(sizes):.1f}")
    print(f"Caption coverage: {has_caption}/{len(sizes)}")

verify_dataset("./data/train_large")
```

---

## Notes

1. **Download time**: 10,000 images takes ~2-4 hours depending on network
2. **Disk space**: Each image ~100-500KB, 10K images ≈ 2-5GB
3. **Captions**: Essential for text conditioning (paper uses them)
4. **Size filtering**: Paper specifies minimum 512² pixels
5. **Augmentation**: Paper uses crop + resize (random for training)

---

## Troubleshooting

**"Too slow to download"**

- Use smaller `num_images` (5000 is minimum viable)
- Increase `max_workers` (but watch memory)
- Use pre-filtered URL list instead

**"Out of memory during loading"**

- Reduce `batch_size`
- Reduce `num_workers` to 0 or 1
- Use gradient accumulation instead

**"Images too large"**

- Add max size filtering in dataset
- Pre-process images to 512×512

**"Missing captions"**

- Some COYO images may have empty captions
- Filter them out or use empty string (model handles it)
