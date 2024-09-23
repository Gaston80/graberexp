import subprocess
list_files = subprocess.run(["git", "add", '.'])
print(list_files)
list_files = subprocess.run(["git", "commit", '-m', "Update"])
print(list_files)
list_files = subprocess.run(["git", "push"])
print(list_files)
