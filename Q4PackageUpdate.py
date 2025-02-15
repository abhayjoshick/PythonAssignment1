import os
import subprocess
import logging

def get_package_manager():
    """Detect the package manager (apt or yum)."""
    if os.path.exists("/usr/bin/apt"):  
        return "apt"
    elif os.path.exists("/usr/bin/yum"):  
        return "yum"
    else:
        print("Unsupported package manager.")
        exit(1)

def check_updates(pkg_manager):
    """List available updates."""
    cmd = "apt list --upgradable" if pkg_manager == "apt" else "yum check-update"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    updates = result.stdout.split("\n")[1:]
    packages = [line.split()[0] for line in updates if line]
    
    for i, package in enumerate(packages):
        print(f"{i+1}. {package}")
    return packages

def update_packages(pkg_manager, packages, selection):
    """Update selected packages."""
    if selection == "all":
        cmd = "sudo apt upgrade -y" if pkg_manager == "apt" else "sudo yum update -y"
    else:
        selected_pkgs = " ".join([packages[int(i) - 1] for i in selection.split() if i.isdigit()])
        cmd = f"sudo apt install -y {selected_pkgs}" if pkg_manager == "apt" else f"sudo yum update -y {selected_pkgs}"
    
    print("Executing:", cmd)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Update failed: {result.stderr}")
        print("Some updates failed. Check log.")
    else:
        print("Update successful.")

def main():
    logging.basicConfig(filename="update_errors.log", level=logging.ERROR)
    pkg_manager = get_package_manager()
    packages = check_updates(pkg_manager)
    
    if not packages:
        print("No updates available.")
        return
    
    choice = input("Enter package index numbers to update (or 'all' to update everything): ")
    update_packages(pkg_manager, packages, choice)
    
if __name__ == "__main__":
    main()