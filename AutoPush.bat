set /p commit_message="Insert commit message: "

git add -A
git commit -m "%commit_message%"
git push