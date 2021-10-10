### Uploading Large Files
git init
git lfs track "*.pt"
git add .gitattributes
git remote add origin https://github.com/AqilAkmal/ImagePredictor.git
git add predictor/*
git commit -m "first commit"
git push --set-upstream origin master