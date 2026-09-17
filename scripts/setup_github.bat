@echo off
setlocal
echo ===================================================
echo  AI and Machine Learning Data Platform
echo ===================================================
git init
git branch -M main
git add .
git commit -m "feat: AI and Machine Learning Data Platform - Databricks, Feast Feature Store, Terraform, RAG Datasets"
set /p GH_USER="Enter GitHub username (or press enter for soniablaketech/masonmirtech): "
git remote remove origin 2>nul
git remote add origin https://github.com/%GH_USER%/ai-ml-data-platform.git
git push -u origin main
pause
