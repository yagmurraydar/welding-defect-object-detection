
from pathlib import Path
import argparse

from PIL import Image, ImageDraw, ImageFont


CLASS_NAMES = [
    "Bad Welding",
    "Crack",
    "Excess Reinforcement",
    "Good Welding",
    "Porosity",
    "Spatters",
]

COLORS = [
    (255, 80, 80),
    (255, 180, 0),
    (0, 180, 255),
    (0, 200, 100),
    (180, 80, 255),
    (255, 230, 0),
]


def main():
    parser = argparse.ArgumentParser(
        description="Visualize YOLO detection labels on images."
    )

    parser.add_argument(
        "--dataset-root",
        type=Path,
        required=True,
        help="Path to the detection dataset.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory where preview images will be saved.",
    )

    args = parser.parse_args()

    dataset_root = args.dataset_root.resolve()

    if not dataset_root.is_dir():
        raise FileNotFoundError(dataset_root)

    image_dir = dataset_root / "train" / "images"
    label_dir = dataset_root / "train" / "labels"

    if not image_dir.is_dir() or not label_dir.is_dir():
        raise FileNotFoundError(
            "Train images or labels directory not found."
        )

    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else dataset_root / "preview_samples"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    image_map = {
        path.stem: path
        for path in image_dir.iterdir()
        if path.is_file()
    }

    candidates = {
        class_id: []
        for class_id in range(len(CLASS_NAMES))
    }

    for label_file in sorted(label_dir.glob("*.txt")):
        class_ids = set()

        for line in label_file.read_text(
            encoding="utf-8"
        ).splitlines():

            if not line.strip():
                continue

            parts = line.split()

            if len(parts) != 5:
                raise ValueError(
                    f"Expected 5 values in {label_file.name}"
                )

            class_id = int(parts[0])

            if not 0 <= class_id < len(CLASS_NAMES):
                raise ValueError(
                    f"Invalid class ID in {label_file.name}"
                )

            class_ids.add(class_id)

        for class_id in class_ids:
            if label_file.stem in image_map:
                candidates[class_id].append(label_file)

    selected = {}
    used_images = set()

    # Select one different training image for each class.
    for class_id in range(len(CLASS_NAMES)):
        available = [
            file
            for file in candidates[class_id]
            if file.stem not in used_images
        ]

        if not available:
            raise RuntimeError(
                f"No suitable image found for {CLASS_NAMES[class_id]}"
            )

        selected[class_id] = available[0]
        used_images.add(available[0].stem)

    # Draw all labels belonging to each selected image.
    for target_class, label_file in selected.items():
        image_path = image_map[label_file.stem]

        with Image.open(image_path) as source:
            image = source.convert("RGB")

        draw = ImageDraw.Draw(image)
        width, height = image.size
        font = ImageFont.load_default()

        lines = label_file.read_text(
            encoding="utf-8"
        ).splitlines()

        box_count = 0

        for line in lines:
            if not line.strip():
                continue

            parts = line.split()

            class_id = int(parts[0])
            cx, cy, box_w, box_h = map(float, parts[1:])

            x1 = (cx - box_w / 2) * width
            y1 = (cy - box_h / 2) * height
            x2 = (cx + box_w / 2) * width
            y2 = (cy + box_h / 2) * height

            color = COLORS[class_id]
            text = CLASS_NAMES[class_id]

            draw.rectangle(
                (x1, y1, x2, y2),
                outline=color,
                width=3,
            )

            text_bbox = draw.textbbox(
                (x1, y1),
                text,
                font=font,
            )

            text_y = max(0, y1 - (text_bbox[3] - text_bbox[1]))

            draw.rectangle(
                (
                    x1,
                    text_y,
                    x1 + (text_bbox[2] - text_bbox[0]),
                    text_y + (text_bbox[3] - text_bbox[1]),
                ),
                fill=color,
            )

            draw.text(
                (x1, text_y),
                text,
                fill=(0, 0, 0),
                font=font,
            )

            box_count += 1

        output_file = output_dir / (
            f"{target_class}_"
            f"{CLASS_NAMES[target_class].replace(' ', '_')}.jpg"
        )

        image.save(output_file, quality=95)

        print(
            f"{CLASS_NAMES[target_class]}: "
            f"{image_path.name} | "
            f"{box_count} boxes | "
            f"{output_file.name}"
        )

    print(f"\nPreview images saved to: {output_dir}")


if __name__ == "__main__":
    main()
