import os
import shutil
import hashlib
import time
import filecmp
from collections import defaultdict

VERSIONS_DIR = "./versions"  
MAX_VERSIONS = 5  

def get_file_checksum(file_path):
    """Compute SHA-256 checksum of a file."""
    hash_func = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def save_new_version(file_path):
    """Save a new version of a file in the versions directory."""
    if not os.path.exists(VERSIONS_DIR):
        os.makedirs(VERSIONS_DIR)

    file_name = os.path.basename(file_path)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    version_file = os.path.join(VERSIONS_DIR, f"{file_name}_{timestamp}")

    shutil.copy2(file_path, version_file)
    print(f"✔ New version saved: {version_file}")

def track_changes(directory):
    """Monitor and store versions of modified files."""
    file_hashes = {}

    while True:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isdir(file_path) or VERSIONS_DIR in file_path:
                    continue  

                checksum = get_file_checksum(file_path)

                if file_path not in file_hashes:
                    file_hashes[file_path] = checksum
                elif file_hashes[file_path] != checksum:  
                    print(f"🔄 Detected change in {file}")
                    save_new_version(file_path)
                    file_hashes[file_path] = checksum  

        time.sleep(5)  

def restore_version(original_file, version_file):
    """Restore a specific version of a file."""
    shutil.copy2(version_file, original_file)
    print(f"✔ Restored {original_file} from {version_file}")

def list_versions(file_name):
    """List all saved versions of a file."""
    versions = sorted([f for f in os.listdir(VERSIONS_DIR) if f.startswith(file_name)], reverse=True)
    if not versions:
        print("❌ No versions found.")
    else:
        print("\nAvailable versions:")
        for idx, v in enumerate(versions, 1):
            print(f"{idx}. {v}")

def compare_versions(file1, file2):
    """Compare two versions and show differences."""
    if filecmp.cmp(file1, file2, shallow=False):
        print("✅ The files are identical.")
    else:
        print("❌ The files are different.")

def cleanup_old_versions():
    """Remove older versions, keeping only the last N versions per file."""
    file_versions = defaultdict(list)

    for version in os.listdir(VERSIONS_DIR):
        base_name = "_".join(version.split("_")[:-1]) 
        file_versions[base_name].append(version)

    for base_name, versions in file_versions.items():
        versions.sort(reverse=True) 
        for old_version in versions[MAX_VERSIONS:]:
            os.remove(os.path.join(VERSIONS_DIR, old_version))
            print(f"🗑 Deleted old version: {old_version}")

def main():
    directory = input("Enter directory to track: ").strip()
    print(f"Tracking changes in: {directory}")
    
    while True:
        print("\nOptions:")
        print("1. Start tracking")
        print("2. Restore a previous version")
        print("3. Compare two versions")
        print("4. Cleanup old versions")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            track_changes(directory)
        elif choice == "2":
            file_name = input("Enter file name to restore: ").strip()
            list_versions(file_name)
            version_name = input("Enter version file to restore: ").strip()
            restore_version(os.path.join(directory, file_name), os.path.join(VERSIONS_DIR, version_name))
        elif choice == "3":
            file1 = input("Enter first version file: ").strip()
            file2 = input("Enter second version file: ").strip()
            compare_versions(os.path.join(VERSIONS_DIR, file1), os.path.join(VERSIONS_DIR, file2))
        elif choice == "4":
            cleanup_old_versions()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
