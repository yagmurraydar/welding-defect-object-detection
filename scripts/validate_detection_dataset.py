
from pathlib import Path
import argparse
import math
from collections import Counter


CLASS_NAMES = [
    "Bad Welding",
    "Crack",
    "Excess Reinforcement",
    "Good Welding",
    "Porosity",
    "Spatters",
]

SPLITS = ("train", "valid", "test")


def validate_dataset(dataset_root):
    total_errors = 0
    total_rows = 0

    for split in SPLITS:
        image_dir = dataset_root / split / "images"
        label_dir = dataset_root / split / "labels"

        if not image_dir.is_dir():
            raise FileNotFoundError(
                f"Image directory not found: {image_dir}"
            )

        if not label_dir.is_dir():
            raise FileNotFoundError(
                f"Label directory not found: {label_dir}"
            )

        images = {
            file.stem
            for file in image_dir.iterdir()
            if file.is_file()
        }

        label_files = sorted(label_dir.glob("*.txt"))
        label_names = {file.stem for file in label_files}

        missing_labels = images - label_names
        orphan_labels = label_names - images

        bad_rows = 0
        duplicate_rows = 0
        empty_files = 0
        row_count = 0

        class_counts = Counter()
        errors = []

        for file in label_files:
            seen = set()
            file_row_count = 0

            lines = file.read_text(
                encoding="utf-8"
            ).splitlines()

            for line_number, line in enumerate(lines, start=1):
                if not line.strip():
                    continue

                file_row_count += 1
                row_count += 1

                parts = line.split()

                try:
                    if len(parts) != 5:
                        raise ValueError(
                            "Expected exactly 5 values."
                        )

                    class_id = int(parts[0])

                    if not 0 <= class_id < len(CLASS_NAMES):
                        raise ValueError("Invalid class ID.")

                    values = [float(value) for value in parts[1:]]

                    if not all(math.isfinite(value) for value in values):
                        raise ValueError(
                            "Coordinates must be finite."
                        )

                    if not all(0 <= value <= 1 for value in values):
                        raise ValueError(
                            "Coordinates must be between 0 and 1."
                        )

                    cx, cy, width, height = values

                    if width <= 0 or height <= 0:
                        raise ValueError(
                            "Box width and height must be positive."
                        )

                    if (
                        cx - width / 2 < -1e-6
                        or cy - height / 2 < -1e-6
                        or cx + width / 2 > 1.000001
                        or cy + height / 2 > 1.000001
                    ):
                        raise ValueError(
                            "Bounding box exceeds image boundaries."
                        )

                    normalized_line = " ".join(parts)

                    if normalized_line in seen:
                        duplicate_rows += 1
                    else:
                        seen.add(normalized_line)

                    class_counts[class_id] += 1

                except (ValueError, OverflowError) as exc:
                    bad_rows += 1

                    if len(errors) < 20:
                        errors.append(
                            f"{file.name}, line {line_number}: {exc}"
                        )

            if file_row_count == 0:
                empty_files += 1

        split_errors = (
            bad_rows
            + duplicate_rows
            + empty_files
            + len(missing_labels)
            + len(orphan_labels)
        )

        total_errors += split_errors
        total_rows += row_count

        print(f"\n--- {split.upper()} ---")
        print("Images:", len(images))
        print("Label files:", len(label_files))
        print("Label rows:", row_count)
        print("Invalid rows:", bad_rows)
        print("Duplicate rows:", duplicate_rows)
        print("Empty files:", empty_files)
        print("Missing labels:", len(missing_labels))
        print("Orphan labels:", len(orphan_labels))

        print("\nClass distribution:")

        for class_id, class_name in enumerate(CLASS_NAMES):
            print(f"  {class_name}: {class_counts[class_id]}")

        for error in errors:
            print("ERROR:", error)

    print("\n--- OVERALL RESULTS ---")
    print("Total labels:", total_rows)
    print("Total errors:", total_errors)

    if total_errors == 0:
        print("DATASET VALIDATION SUCCESSFUL!")
        return True

    print("DATASET VALIDATION FAILED!")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate a YOLO object detection dataset."
    )

    parser.add_argument(
        "--dataset-root",
        type=Path,
        required=True,
        help="Path to the detection dataset.",
    )

    args = parser.parse_args()
    dataset_root = args.dataset_root.resolve()

    if not dataset_root.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {dataset_root}"
        )

    data_yaml = dataset_root / "data.yaml"

    if not data_yaml.is_file():
        raise FileNotFoundError(
            f"data.yaml not found: {data_yaml}"
        )

    success = validate_dataset(dataset_root)

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
