git pull || {echo "git push failed";exit 1;}
git push https://x-access-token:$GITHUB_TOKEN@github.com/MagnusSletten/Databank.git || { echo "git push failed"; exit 1; }