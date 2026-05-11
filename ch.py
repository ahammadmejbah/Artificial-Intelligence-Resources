import os
import subprocess

# =========================
# CONFIGURATION
# =========================
TARGET_DATE = "2026-05-11"

# =========================
# MOVE INTO REPO
# =========================


commit_counter = 0


print(f"Generating commits for {TARGET_DATE}...\n")

# Store original README contents
original_contents = {}

# =========================
# WALK THROUGH DIRECTORIES
# =========================
for root, dirs, files in os.walk("."):

    # Skip .git directory
    if ".git" in dirs:
        dirs.remove(".git")

    folder_name = os.path.basename(root)

    if folder_name in ["", "."]:
        folder_name = "Root Directory"

    readme_path = os.path.join(root, "README.md")

    try:

        # =========================
        # SAVE ORIGINAL CONTENT
        # =========================
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                original_contents[readme_path] = f.read()
        else:
            original_contents[readme_path] = ""

        # =========================
        # WRITE TEMP CONTENT
        # =========================
        with open(readme_path, "a", encoding="utf-8") as f:
            f.write(f"\n## Directory: {folder_name}\n")
            f.write(f"Verified on: {TARGET_DATE}\n")

        # =========================
        # GIT ADD
        # =========================
        subprocess.run(
            ["git", "add", readme_path],
            check=True
        )

        # =========================
        # UNIQUE TIMESTAMP
        # =========================
        minutes = (commit_counter // 60) % 60
        seconds = commit_counter % 60

        timestamp = f"12:{minutes:02d}:{seconds:02d}"
        full_date = f"{TARGET_DATE} {timestamp}"

        message = f"Docs: indexed {folder_name} directory"

        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = full_date
        env["GIT_COMMITTER_DATE"] = full_date

        # =========================
        # COMMIT
        # =========================
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            env=env
        )

        print(f"✅ Commit created for: {folder_name}")

        commit_counter += 1

    except Exception as e:
        print(f"❌ Failed: {folder_name}")
        print(e)

# =========================
# CLEAN ALL README FILES
# =========================
print("\nCleaning README files...")

for path, content in original_contents.items():

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        print(f"Could not clean {path}: {e}")

# =========================
# COMMIT CLEANUP
# =========================
subprocess.run(["git", "add", "."], check=True)

cleanup_env = os.environ.copy()
cleanup_env["GIT_AUTHOR_DATE"] = f"{TARGET_DATE} 23:59:59"
cleanup_env["GIT_COMMITTER_DATE"] = f"{TARGET_DATE} 23:59:59"

subprocess.run(
    ["git", "commit", "-m", "Cleanup: restored README files"],
    check=True,
    env=cleanup_env
)

# =========================
# PUSH
# =========================
print(f"\nPushing {commit_counter + 1} commits...")

subprocess.run(
    ["git", "push", "-u", "origin", "main"],
    check=True
)

print("\nDone! Repository updated successfully.")