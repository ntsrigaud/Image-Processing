# Download COYO-700M subset for training
# COYO-700M is a large-scale image-text dataset used in the paper
# We'll download a small subset for demonstration purposes

import os
import json
import requests
from PIL import Image
from io import BytesIO
from datasets import load_dataset

# Create data directory
os.makedirs('./data/train', exist_ok=True)

print("Downloading COYO-700M subset...")
print("Note: Full dataset is 700M images. We're using a small subset for demo.")
print("For full paper reproduction, use larger subsets.\n")

# Load COYO-700M dataset from HuggingFace (streaming mode for efficiency)
# Using a filtered version that matches paper requirements (512x512+)
try:
    # COYO dataset is available on HuggingFace
    # We'll use kakaobrain/coyo-700m (in streaming mode to avoid downloading everything)
    dataset = load_dataset(
        "kakaobrain/coyo-700m",
        split="train",
        streaming=True
    )

    count = 0
    max_images = 10000  # Paper uses 10K+ images from COYO-700M for training
    successful_downloads = 0

    print(f"Downloading up to {max_images} images (≥ 512x512)...\n")

    for item in dataset:
        if successful_downloads >= max_images:
            break

        try:
            # Get image URL and caption
            img_url = item.get('url')
            caption = item.get('text', '')

            if not img_url or not caption:
                continue

            # Download image with timeout
            response = requests.get(img_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()

            # Open and validate image
            img = Image.open(BytesIO(response.content)).convert('RGB')

            # Filter: Only keep images ≥ 512x512 (as specified in paper)
            if min(img.size) >= 512:
                # Resize to 512x512 for uniform batch processing
                img = img.resize((512, 512), Image.Resampling.LANCZOS)

                # Save image
                img_path = f'./data/train/img_{successful_downloads:05d}.jpg'
                json_path = f'./data/train/img_{successful_downloads:05d}.json'

                img.save(img_path, quality=95)

                # Save caption metadata
                with open(json_path, 'w') as f:
                    json.dump({"caption": caption}, f)

                successful_downloads += 1

                if successful_downloads % 10 == 0:
                    print(f"✓ Downloaded {successful_downloads}/{max_images} images...")

        except Exception as e:
            # Skip failed downloads (timeouts, invalid images, etc.)
            count += 1
            if count % 50 == 0:
                print(f"  Processed {count} items, {successful_downloads} valid images...")
            continue

    print(f"\n{'=' * 60}")
    print(f"✓ Successfully downloaded {successful_downloads} training images")
    print(f"  Location: ./data/train/")
    print(f"  Image size: 512x512 (resized)")
    print(f"  Format: JPG + JSON captions")
    print(f"{'=' * 60}")

except Exception as e:
    print(f"\n⚠ Error accessing COYO dataset: {e}")
    print("\nFallback: Using alternative dataset...")

    # Fallback to Conceptual Captions if COYO is unavailable
    dataset = load_dataset("conceptual_captions", split="train", streaming=True)
    count = 0
    max_images = 10000  # Match main dataset size

    for item in dataset:
        if count >= max_images:
            break

        try:
            img_url = item.get('image_url')
            caption = item.get('caption', '')

            if img_url and caption:
                response = requests.get(img_url, timeout=5)
                img = Image.open(BytesIO(response.content)).convert('RGB')

                if min(img.size) >= 512:
                    img = img.resize((512, 512), Image.Resampling.LANCZOS)
                    img_path = f'./data/train/img_{count:05d}.jpg'
                    json_path = f'./data/train/img_{count:05d}.json'

                    img.save(img_path)
                    with open(json_path, 'w') as f:
                        json.dump({"caption": caption}, f)

                    count += 1
                    if count % 10 == 0:
                        print(f"Downloaded {count} images...")
        except Exception:
            continue

    print(f"✓ Downloaded {count} training images (fallback dataset)")