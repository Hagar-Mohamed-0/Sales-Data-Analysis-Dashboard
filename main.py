import kagglehub
import shutil
from pathlib import Path

path = kagglehub.dataset_download("vivek468/superstore-dataset-final")

print("Dataset downloaded to:", path)

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

for file in Path(path).iterdir():
    dest_file = data_dir / file.name
    shutil.copy2(file, dest_file)
    print(f"Copied {file.name} to {dest_file}")
    
