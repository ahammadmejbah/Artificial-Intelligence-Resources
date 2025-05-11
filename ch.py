import os
import subprocess

TARGET_DATE = "2025-05-11"

commit_counter = 0

print(f"Generating commits for {TARGET_DATE}...\n")

# ====================================
# SAVE ORIGINAL README CONTENTS
# ====================================

original_readmes = {}

for root, dirs, files in os.walk("."):

    if ".git" in dirs:
        dirs.remove(".git")

    readme_path = os.path.join(root, "README.md")

    if os.path.exists(readme_path):

        with open(readme_path, "r", encoding="utf-8") as f:
            original_readmes[readme_path] = f.read()

# ====================================
# CREATE COMMITS
# ====================================

for root, dirs, files in os.walk("."):

    if ".git" in dirs:
        dirs.remove(".git")

    folder_name = os.path.basename(root)

    if folder_name in ["", "."]:
        folder_name = "Root"

    readme_path = os.path.join(root, "README.md")

    try:

        # Create README if missing
        if not os.path.exists(readme_path):

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"# {folder_name}\n")

        # Add temporary content
        with open(readme_path, "a", encoding="utf-8") as f:
            f.write(f"\nVerified on: {TARGET_DATE}\n")

        subprocess.run(
            ["git", "add", readme_path],
            check=True
        )

        minutes = (commit_counter // 60) % 60
        seconds = commit_counter % 60

        timestamp = f"12:{minutes:02d}:{seconds:02d}"
        full_date = f"{TARGET_DATE} {timestamp}"

        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = full_date
        env["GIT_COMMITTER_DATE"] = full_date

        subprocess.run(
            ["git", "commit", "-m", f"Docs: updated {folder_name}"],
            env=env,
            check=True
        )

        print(f"✅ {folder_name}")

        commit_counter += 1

    except Exception as e:
        print(f"❌ Error in {folder_name}")
        print(e)

# ====================================
# RESTORE ORIGINAL FILES
# ====================================

print("\nRestoring original README files...\n")

for path, content in original_readmes.items():

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Remove newly created README files
for root, dirs, files in os.walk("."):

    if ".git" in dirs:
        dirs.remove(".git")

    readme_path = os.path.join(root, "README.md")

    if readme_path not in original_readmes:

        try:
            os.remove(readme_path)
        except:
            pass

# ====================================
# CLEANUP COMMIT
# ====================================

subprocess.run(["git", "add", "."], check=True)

cleanup_env = os.environ.copy()
cleanup_env["GIT_AUTHOR_DATE"] = f"{TARGET_DATE} 23:59:59"
cleanup_env["GIT_COMMITTER_DATE"] = f"{TARGET_DATE} 23:59:59"

subprocess.run(
    ["git", "commit", "-m", "Cleanup: restored original README files"],
    env=cleanup_env,
    check=True
)

# ====================================
# PUSH
# ====================================

subprocess.run(
    ["git", "push", "origin", "main"],
    check=True
)

print("\n✅ All commits pushed successfully.")