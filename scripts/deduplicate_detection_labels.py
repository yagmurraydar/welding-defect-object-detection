
from pathlib import Path
import argparse
import shutil


SPLITS = ("train", "valid", "test")


def main():
    parser = argparse.ArgumentParser(
        description="Remove exact duplicate YOLO detection labels."
    )

    parser.add_argument(
        "--dataset-root",
        type=Path,
        required=True,
        help="Path to the converted detection dataset.",
    )

    parser.add_argument(
        "--backup-root",
        type=Path,
        required=True,
        help="Path where original labels will be backed up.",
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually remove duplicates. Without this flag, only preview.",
    )

    args = parser.parse_args()

    dataset_root = args.dataset_root.resolve()
    backup_root = args.backup_root.resolve()

    if not dataset_root.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {dataset_root}"
        )

    if dataset_root == backup_root:
        raise ValueError("Dataset and backup directories must differ.")

    if dataset_root in backup_root.parents:
        raise ValueError("Backup cannot be inside the dataset directory.")

    if backup_root in dataset_root.parents:
        raise ValueError("Dataset cannot be inside the backup directory.")

    if args.apply and backup_root.exists():
        raise FileExistsError(
            f"Backup directory already exists: {backup_root}. "
            "Choose a new backup path."
        )

    plans = {}
    statistics = {}

    # First inspect all files without modifying anything.
    for split in SPLITS:
        label_dir = dataset_root / split / "labels"

        if not label_dir.is_dir():
            raise FileNotFoundError(
                f"Label directory not found: {label_dir}"
            )

        before_count = 0
        removed_count = 0

        for file in sorted(label_dir.glob("*.txt")):
            lines = [
                line.strip()
                for line in file.read_text(
                    encoding="utf-8-sig"
                ).splitlines()
                if line.strip()
            ]

            unique_lines = []
            seen = set()

            for line in lines:
                before_count += 1

                if line in seen:
                    removed_count += 1
                    continue

                seen.add(line)
                unique_lines.append(line)

            plans[file] = unique_lines

        statistics[split] = {
            "before": before_count,
            "removed": removed_count,
            "after": before_count - removed_count,
        }

    print("\n--- DUPLICATE ANALYSIS ---")

    for split, stats in statistics.items():
        print(f"\n{split.upper()}")
        print("Original rows:", stats["before"])
        print("Duplicate rows:", stats["removed"])
        print("Rows after cleanup:", stats["after"])

    total_removed = sum(
        stats["removed"] for stats in statistics.values()
    )

    print("\nTotal duplicate rows:", total_removed)

    if not args.apply:
        print("\nDRY RUN: No files were changed.")
        print("Use --apply to create a backup and remove duplicates.")
        return

    if total_removed == 0:
        print("\nNo duplicate labels found. Nothing to change.")
        return

    # Back up every label file before modifying any of them.
    print("\nCreating label backup...")

    backup_root.mkdir(parents=True, exist_ok=False)

    for file in plans:
        relative_path = file.relative_to(dataset_root)
        backup_file = backup_root / relative_path

        backup_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, backup_file)

    # Write cleaned labels using temporary files and atomic replacement.
    for file, unique_lines in plans.items():
        content = "\n".join(unique_lines)

        if unique_lines:
            content += "\n"

        temporary_file = file.with_name(file.name + ".tmp")

        temporary_file.write_text(
            content,
            encoding="utf-8",
        )

        temporary_file.replace(file)

    # Verify that no exact duplicate rows remain.
    remaining_duplicates = []

    for file in plans:
        lines = [
            line.strip()
            for line in file.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]

        if len(lines) != len(set(lines)):
            remaining_duplicates.append(str(file))

    if remaining_duplicates:
        raise RuntimeError(
            "Duplicate labels remain: "
            + ", ".join(remaining_duplicates)
        )

    print("\nCLEANUP COMPLETED SUCCESSFULLY")
    print("Removed duplicate rows:", total_removed)
    print("Remaining duplicates: 0")
    print("Backup directory:", backup_root)


if __name__ == "__main__":
    main()
