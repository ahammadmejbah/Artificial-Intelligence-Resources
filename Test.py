import os

# Configuration: How many commits do you want for today?
# 50 commits will usually make the square dark green.
number_of_commits = 50 

# The specific date you requested
target_date = "2026-01-01"

print(f"Starting {number_of_commits} commits for {target_date}...")

for i in range(number_of_commits):
    # 1. Modify the file so there is something to commit
    with open('file.txt', 'a') as file:
        file.write(f'Commit {i+1} for {target_date}\n')

    # 2. Stage the file
    os.system('git add .')

    # 3. Commit with the specific date
    # We add a fake time (12:00 + seconds) to keep them ordered
    commit_date = f"{target_date} 12:00:{i%60:02d}"
    message = f"Commit {i+1}"
    
    # Matches the style of your image, but locks date to 01/01/2026
    os.system(f'git commit --date="{commit_date}" -m "{message}"')

# 4. Push all commits at once at the end
print("Pushing to GitHub...")
os.system('git push -u origin main')
print("Done! Check your contribution graph.")