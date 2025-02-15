import os
import hashlib
import shutil

def get_file_checksum(file_path, algo="sha256"):
    """Calculate the checksum of a file using the specified algorithm."""
    hash_func = hashlib.new(algo)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def find_duplicates(directory, min_size=0):
    """Find duplicate files in a directory based on SHA-256 checksums."""
    file_hashes = {}
    duplicates = {}

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) < min_size:
                continue  # Skip small files

            checksum = get_file_checksum(file_path)
            if checksum in file_hashes:
                duplicates.setdefault(checksum, []).append(file_path)
            else:
                file_hashes[checksum] = file_path

    return duplicates

def handle_duplicates(duplicates, action="list", move_dir=None):
    """List, delete, or move duplicate files."""
    report_lines = []

    for checksum, files in duplicates.items():
        if len(files) > 1:
            report_lines.append(f"Checksum: {checksum}")
            for idx, file in enumerate(files, 1):
                report_lines.append(f"  {idx}. {file}")

            if action == "delete":
                for file in files[1:]:  # Keep one, delete others
                    os.remove(file)
                    report_lines.append(f"  [Deleted] {file}")

            elif action == "move" and move_dir:
                os.makedirs(move_dir, exist_ok=True)
                for file in files[1:]:
                    shutil.move(file, os.path.join(move_dir, os.path.basename(file)))
                    report_lines.append(f"  [Moved] {file} -> {move_dir}")

    return "\n".join(report_lines)

def main():
    directory = input("Enter directory to scan: ").strip()
    min_size = int(input("Enter minimum file size for detection (bytes, 0 to disable): ").strip())
    action = input("Choose action (list/delete/move): ").strip().lower()
    move_dir = None

    if action == "move":
        move_dir = input("Enter directory to move duplicates: ").strip()

    duplicates = find_duplicates(directory, min_size)
    report = handle_duplicates(duplicates, action, move_dir)

    with open("duplicate_report.txt", "w") as f:
        f.write(report)

    print("\nDuplicate Scan Complete. Report saved to 'duplicate_report.txt'.")

if __name__ == "__main__":
    main()
