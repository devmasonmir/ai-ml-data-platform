param([string]$Username = "masonmirtech")
git init; git branch -M main; git add .
git commit -m "feat: AI and Machine Learning Data Platform - Databricks, Feast Feature Store, Terraform, RAG Datasets"
git remote remove origin 2>$null
git remote add origin "https://github.com/$Username/ai-ml-data-platform.git"
git push -u origin main
