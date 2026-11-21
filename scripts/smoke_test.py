
from pathlib import Path
import argparse

from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser(
        description="Run a small YOLO26n training smoke test."
    )

    parser.add_argument(
        "--dataset-root",
        type=Path,
        required=True,
        help="Path to the detection dataset directory.",
    )

    parser.add_argument(
        "--weights",
        type=str,
        default="yolo26n.pt",
        help="Pretrained YOLO model weights or model identifier.",
    )

    parser.add_argument(
        "--project",
        type=Path,
        default=Path("runs"),
        help="Directory where training results will be saved.",
    )

    args = parser.parse_args()

    dataset_root = args.dataset_root.resolve()
    data_yaml = dataset_root / "data.yaml"
    project_dir = args.project.resolve()

    if not dataset_root.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {dataset_root}"
        )

    if not data_yaml.is_file():
        raise FileNotFoundError(
            f"data.yaml not found: {data_yaml}"
        )

    print("Loading YOLO model...")
    print(f"Weights: {args.weights}")

    model = YOLO(args.weights)

    print("\nStarting training smoke test...")

    model.train(
        data=str(data_yaml),
        epochs=1,
        imgsz=320,
        batch=1,
        workers=0,
        device="cpu",
        cache=False,
        fraction=0.02,
        val=False,
        amp=False,
        plots=False,
        project=str(project_dir),
        name="smoke_test",
        exist_ok=True,
    )

    print("\nTraining smoke test completed successfully!")


if __name__ == "__main__":
    main()
