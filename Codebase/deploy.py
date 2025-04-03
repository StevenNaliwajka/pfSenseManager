import subprocess
import sys

# Dry-run passthrough
args = sys.argv[1:]
dry_run_flag = "--dry-run" if "--dry-run" in args else ""

scripts = [
    "global.py",
    "deploy_aliases.py",
    "deploy_vlans.py",
    "deploy_rules.py",
    "deploy_port_forward.py",
    "deploy_dns_resolver.py"
]

print("Starting pfSenseManager full deploy\n----------------------------")

for script in scripts:
    path = f"./Codebase/Deploy/{script}"
    print(f"\nRunning: {path}")
    result = subprocess.run(["python3", path] + ([dry_run_flag] if dry_run_flag else []))
    if result.returncode != 0:
        print(f"Failed running {script}. Aborting.")
        sys.exit(result.returncode)

print("\nAll configuration scripts completed successfully." + (" (dry run mode)" if dry_run_flag else ""))
