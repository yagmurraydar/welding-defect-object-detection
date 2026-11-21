
from pathlib import Path
import argparse
import math
import shutil


SPLITS = ("train", "valid", "test")

CLASS_NAMES = [
    "Bad Welding",
    "Crack",
    "Excess Reinforcement",
    "Good Welding",
    "Porosity",
    "Spatters",
]


def convert_line(line):
    parts = line.strip().split()

    if not parts:
        return None, None

    try:
        class_id = int(parts[0])
    except ValueError as exc:
        raise ValueError("Invalid class ID.") from exc

    if not 0 <= class_id < len(CLASS_NAMES):
        raise ValueError(f"Invalid class ID: {class_id}")

    try:
        coordinates = [float(value) for value in parts[1:]]
    except ValueError as exc:
        raise ValueError("Coordinates must be numeric.") from exc

    if not all(math.isfinite(value) for value in coordinates):
        raise ValueError("Coordinates must be finite.")

    if not all(0.0 <= value <= 1.0 for value in coordinates):
        raise ValueError("Coordinates must be between 0 and 1.")

    # Preserve existing YOLO bounding boxes.
    if len(parts) == 5:
        cx, cy, width, height = coordinates

        if width <= 0 or height <= 0:
            raise ValueError("Bounding box dimensions must be positive.")

        if (
            cx - width / 2 < -1e-6
            or cy - height / 2 < -1e-6
            or cx + width / 2 > 1.000001
            or cy + height / 2 > 1.000001
        ):
            raise ValueError("Bounding box exceeds image boundaries.")

        return " ".join(parts), "bounding_box"

    # Convert YOLO polygon coordinates into a bounding box.
    if len(parts) >= 7 and len(parts) % 2 == 1:
        xs = coordinates[0::2]
        ys = coordinates[1::2]

        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        width = x_max - x_min
        height = y_max - y_min

        if width <= 0 or height <= 0:
            raise ValueError("Polygon has zero area.")

        cx = (x_min + x_max) / 2
        cy = (y_min + y_max) / 2

        converted = (
            f"{class_id} "
            f"{cx:.10f} {cy:.10f} "
            f"{width:.10f} {height:.10f}"
        )

        return converted, "polygon"

    raise ValueError(f"Unsupported annotation format: {len(parts)} values")


def main():
    parser = argparse.ArgumentParser(
        description="Convert YOLO polygon labels to bounding boxes."
    )

    parser.add_argument(
        "--source-root",
        type=Path,
        required=True,
        help="Original dataset directory.",
    )

    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Destination detection dataset directory.",
    )

    args = parser.parse_args()

    source_root = args.source_root.resolve()
    output_root = args.output_root.resolve()

    if not source_root.is_dir():
        raise FileNotFoundError(
            f"Source dataset not found: {source_root}"
        )

    if source_root == output_root:
        raise ValueError("Source and output directories must be different.")

    prepared_labels = {}
    statistics = {}

    # Validate every split before writing converted labels.
    for split in SPLITS:
        source_images = source_root / split / "images"
        source_labels = source_root / split / "labels"

        if not source_images.is_dir() or not source_labels.is_dir():
            raise FileNotFoundError(
                f"Missing images or labels directory: {split}"
            )

        image_files = [
            path for path in source_images.iterdir()
            if path.is_file()
        ]

        image_names = {path.stem for path in image_files}
        label_files = sorted(source_labels.glob("*.txt"))
        label_names = {path.stem for path in label_files}

        if image_names != label_names:
            raise ValueError(
                f"{split}: Image and label filenames do not match."
            )

        box_count = 0
        polygon_count = 0
        empty_files = 0

        for label_file in label_files:
            converted_lines = []

            lines = label_file.read_text(
                encoding="utf-8-sig"
            ).splitlines()

            for line_number, line in enumerate(lines, start=1):
                try:
                    converted, label_type = convert_line(line)
                except ValueError as exc:
                    raise ValueError(
                        f"{split}/{label_file.name}, "
                        f"line {line_number}: {exc}"
                    ) from exc

                if converted is None:
                    continue

                converted_lines.append(converted)

                if label_type == "bounding_box":
                    box_count += 1
                else:
                    polygon_count += 1

            if not converted_lines:
                empty_files += 1

            prepared_labels[(split, label_file.name)] = (
                "\n".join(converted_lines)
                + ("\n" if converted_lines else "")
            )

        statistics[split] = {
            "images": len(image_files),
            "label_files": len(label_files),
            "bounding_boxes": box_count,
            "converted_polygons": polygon_count,
            "empty_files": empty_files,
        }

    # All source labels passed validation. Now create the output.
    for split in SPLITS:
        target_images = output_root / split / "images"
        target_labels = output_root / split / "labels"

        target_images.mkdir(parents=True, exist_ok=True)
        target_labels.mkdir(parents=True, exist_ok=True)

        source_images = source_root / split / "images"

        for image_file in source_images.iterdir():
            if image_file.is_file():
                shutil.copy2(
                    image_file,
                    target_images / image_file.name,
                )

    for (split, filename), content in prepared_labels.items():
        target_file = output_root / split / "labels" / filename
        target_file.write_text(content, encoding="utf-8")

    yaml_content = f'''path: "{output_root.as_posix()}"
train: train/images
val: valid/images
test: test/images

nc: 6
names: {CLASS_NAMES}
'''

    (output_root / "data.yaml").write_text(
        yaml_content,
        encoding="utf-8",
    )

    print("\nCONVERSION COMPLETED SUCCESSFULLY")

    for split, stats in statistics.items():
        print(f"\n{split.upper()}")

        for key, value in stats.items():
            print(f"{key}: {value}")

    print(f"\nOutput dataset: {output_root}")


if __name__ == "__main__":
    main()
