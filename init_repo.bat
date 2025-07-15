@echo off
REM GitHub Repository Setup Script for BeyondChats Assignment
REM ========================================================

echo 🚀 Setting up GitHub repository for BeyondChats assignment...
echo ============================================================

REM Initialize git repository
echo 📁 Initializing Git repository...
git init

REM Create and switch to RedLens branch
echo 🌿 Creating RedLens branch...
git checkout -b RedLens

REM Add all files
echo 📄 Adding files to repository...
git add .

REM Create initial commit
echo 💾 Creating initial commit...
git commit -m "Reddit User Persona Analyzer - BeyondChats Assignment Submission" -m "🎯 Complete implementation for AI/LLM Engineer Intern position" -m "📊 Features:" -m "✅ Reddit profile URL processing and data scraping" -m "✅ Comprehensive user persona generation with demographics analysis" -m "✅ Interest identification from subreddit participation" -m "✅ Communication style and engagement pattern analysis" -m "✅ Citation system with direct links to supporting evidence" -m "✅ Professional output formatting and error handling" -m "✅ Sample analyses for u/kojied and u/Hungry-Move-6603" -m "✅ Complete documentation and setup instructions" -m "✅ PEP-8 compliant Python code with modular design" -m "" -m "🚀 Developed by: Patil (RedLens)" -m "📅 Completed: July 15, 2025 (within 48-hour deadline)" -m "🌿 Branch: RedLens" -m "📋 Assignment: COMPLETE - Ready for BeyondChats evaluation"

echo.
echo ✅ Repository initialized successfully on RedLens branch!
echo.
echo 📋 Next steps to create GitHub repository:
echo 1. Go to GitHub.com and create a new public repository
echo 2. Name it 'reddit-persona-analyzer-beyondchats'
echo 3. Copy the repository URL
echo 4. Run these commands:
echo.
echo    git remote add origin ^<your-repository-url^>
echo    git push -u origin RedLens
echo.
echo 🎉 Your assignment will be submitted on the RedLens branch!
echo 📊 Repository will contain all required deliverables for evaluation.
echo ============================================================
pause
