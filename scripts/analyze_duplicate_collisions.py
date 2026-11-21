
from pathlib import Path
from collections import defaultdict
import argparse


def convert_line(line):
    parts = line.strip().split()

    if not parts:
        return None

    class_id = int(parts[0])
    values = [float(value) for value in parts[1:]]

    if len(parts) == 5:
        return " ".join(parts)

    if len(parts) >= 7 and len(parts) % 2 == 1:
        xs = values[0::2]
        ys = values[1::2]

        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        cx = (x_min + x_max) / 2
        cy = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min

        return (
            f"{class_id} {cx:.10f} {cy:.10f} "
            f"{width:.10f} {height:.10f}"
        )

    raise ValueError(f"Unsupported annotation format: {line}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze duplicate bounding boxes after conversion."
    )

    parser.add_argument(
        "--source-root",
        type=Path,
        required=True,
        help="Original YOLO dataset directory.",
    )

    parser.add_argument(
        "--converted-root",
        type=Path,
        required=True,
        help="Converted detection dataset directory.",
    )

    args = parser.parse_args()

    source_root = args.source_root.resolve()
    converted_root = args.converted_root.resolve()

    if not source_root.is_dir():
        raise FileNotFoundError(source_root)

    if not converted_root.is_dir():
        raise FileNotFoundError(converted_root)

    total_files = 0
    duplicate_groups = 0
    extra_rows = 0

    source_duplicate_extra = 0
    conversion_collision_extra = 0
    mismatched_files = 0

    examples = []

    for split in ("train", "valid", "test"):
        source_dir = source_root / split / "labels"
        converted_dir = converted_root / split / "labels"

        if not source_dir.is_dir() or not converted_dir.is_dir():
            raise FileNotFoundError(f"Missing label directory: {split}")

        split_files = 0
        split_extra = 0
        split_source_extra = 0
        split_collision_extra = 0

        for source_file in sorted(source_dir.glob("*.txt")):
            converted_file = converted_dir / source_file.name

            if not converted_file.is_file():
                mismatched_files += 1
                continue

            source_rows = [
                line.strip()
                for line in source_file.read_text(
                    encoding="utf-8-sig"
                ).splitlines()
                if line.strip()
            ]

            converted_rows = [
                line.strip()
                for line in converted_file.read_text(
                    encoding="utf-8-sig"
                ).splitlines()
                if line.strip()
            ]

            generated_rows = [
                convert_line(line) for line in source_rows
            ]

            if generated_rows != converted_rows:
                mismatched_files += 1
                continue

            groups = defaultdict(list)

            for original, converted in zip(
                source_rows, converted_rows
            ):
                groups[converted].append(original)

            file_has_duplicates = False

            for box, originals in groups.items():
                if len(originals) <= 1:
                    continue

                file_has_duplicates = True
                duplicate_groups += 1

                extra = len(originals) - 1
                source_extra = len(originals) - len(set(originals))
                collision_extra = len(set(originals)) - 1

                extra_rows += extra
                source_duplicate_extra += source_extra
                conversion_collision_extra += collision_extra

                split_extra += extra
                split_source_extra += source_extra
                split_collision_extra += collision_extra

                if collision_extra > 0 and len(examples) < 5:
                    examples.append({
                        "split": split,
                        "file": source_file.name,
                        "different_polygons": len(set(originals)),
                        "resulting_box": box,
                    })

            if file_has_duplicates:
                split_files += 1

        total_files += split_files

        print(f"\n--- {split.upper()} ---")
        print("Files with duplicates:", split_files)
        print("Extra rows:", split_extra)
        print("Source duplicates:", split_source_extra)
        print("Conversion collisions:", split_collision_extra)

    print("\n--- OVERALL RESULTS ---")
    print("Files with duplicates:", total_files)
    print("Duplicate box groups:", duplicate_groups)
    print("Total extra rows:", extra_rows)
    print("Original source duplicates:", source_duplicate_extra)
    print("Conversion collisions:", conversion_collision_extra)
    print("Mismatched files:", mismatched_files)

    print("\n--- COLLISION EXAMPLES ---")

    for example in examples:
        print(example)


if __name__ == "__main__":
    main()
