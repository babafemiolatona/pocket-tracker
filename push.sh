git add -A
read -p "Enter commit message: " commit_message
git commit -m "$commit_message"
BRANCH=$(git describe --contains --all HEAD)
git pull --rebase origin "$BRANCH"
git push origin "$BRANCH"