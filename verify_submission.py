#!/usr/bin/env python3
"""
Submission Verification Script
=============================

This script verifies that all components are ready for GitHub submission
to BeyondChats for the AI/LLM Engineer Intern assignment.
"""

import os
import sys
import subprocess
from datetime import datetime

def check_file_exists(filename, description):
    """Check if a required file exists"""
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"✅ {filename:<35} - {description} ({size} bytes)")
        return True
    else:
        print(f"❌ {filename:<35} - {description} (MISSING)")
        return False

def verify_script_functionality():
    """Verify the main script works"""
    print("\n🧪 TESTING MAIN SCRIPT FUNCTIONALITY:")
    print("-" * 50)
    
    try:
        # Test help command
        result = subprocess.run([
            sys.executable, 
            "reddit_persona_analyzer.py", 
            "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "Reddit profile URL" in result.stdout:
            print("✅ Main script help command works")
            return True
        else:
            print("❌ Main script help command failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing script: {e}")
        return False

def check_sample_outputs():
    """Check sample output files"""
    print("\n📊 SAMPLE OUTPUT VERIFICATION:")
    print("-" * 50)
    
    sample_files = [
        ("kojied_persona.txt", "Sample analysis for u/kojied"),
        ("Hungry-Move-6603_persona.txt", "Sample analysis for u/Hungry-Move-6603")
    ]
    
    all_present = True
    for filename, description in sample_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename:<35} - {description} ({size} bytes)")
            
            # Check if file has content
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 500 and "USER PERSONA ANALYSIS" in content:
                    print(f"   📄 Content verified - comprehensive analysis present")
                else:
                    print(f"   ⚠️  Content may be incomplete")
        else:
            print(f"❌ {filename:<35} - {description} (MISSING)")
            all_present = False
    
    return all_present

def verify_assignment_requirements():
    """Verify all assignment requirements are met"""
    print("\n📋 ASSIGNMENT REQUIREMENTS VERIFICATION:")
    print("-" * 50)
    
    requirements = [
        ("reddit_persona_analyzer.py", "✅ Executable Python script", True),
        ("README.md", "✅ Setup and execution instructions", True),
        ("kojied_persona.txt", "✅ Sample user analysis (kojied)", True),
        ("Hungry-Move-6603_persona.txt", "✅ Sample user analysis (Hungry-Move-6603)", True),
        ("requirements.txt", "✅ Python dependencies", True),
        (".gitignore", "✅ Version control configuration", False)
    ]
    
    all_met = True
    for filename, description, required in requirements:
        exists = os.path.exists(filename)
        if exists:
            print(f"✅ {description}")
        elif required:
            print(f"❌ {description} - MISSING REQUIRED FILE: {filename}")
            all_met = False
        else:
            print(f"⚠️  {description} - Optional file missing: {filename}")
    
    return all_met

def check_code_quality():
    """Check basic code quality indicators"""
    print("\n🔧 CODE QUALITY VERIFICATION:")
    print("-" * 50)
    
    try:
        with open("reddit_persona_analyzer.py", 'r', encoding='utf-8') as f:
            code = f.read()
            
        checks = [
            ("Shebang line", code.startswith("#!/usr/bin/env python3")),
            ("Docstring present", '"""' in code[:500]),
            ("Author attribution", "Patil" in code[:1000]),
            ("Import statements", "import requests" in code),
            ("Class definitions", "class RedditScraper" in code),
            ("Error handling", "try:" in code and "except" in code),
            ("Logging", "logging" in code),
            ("Type hints", "List[" in code or "Dict[" in code)
        ]
        
        passed = 0
        for check_name, condition in checks:
            if condition:
                print(f"✅ {check_name}")
                passed += 1
            else:
                print(f"❌ {check_name}")
        
        print(f"\n📊 Code quality score: {passed}/{len(checks)} ({(passed/len(checks)*100):.1f}%)")
        return passed >= len(checks) * 0.8  # 80% threshold
        
    except Exception as e:
        print(f"❌ Error checking code quality: {e}")
        return False

def main():
    """Main verification function"""
    print("=" * 70)
    print("🚀 BEYONDCHATS ASSIGNMENT SUBMISSION VERIFICATION")
    print("=" * 70)
    print(f"📅 Verification Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Developer: Patil (RedLens)")
    print(f"🌿 Target Branch: RedLens")
    print("=" * 70)
    
    # Core file verification
    print("\n📁 CORE FILES VERIFICATION:")
    print("-" * 50)
    
    required_files = [
        ("reddit_persona_analyzer.py", "Main analysis script"),
        ("README.md", "Documentation and setup guide"),
        ("requirements.txt", "Python dependencies"),
        ("SUBMISSION_SUMMARY.md", "Assignment completion summary"),
        ("demo.py", "Feature demonstration script"),
        ("setup.py", "Environment setup script"),
        ("test_analyzer.py", "Test suite"),
        ("config.ini", "Configuration file"),
        ("init_repo.bat", "GitHub setup script (Windows)"),
        ("init_repo.sh", "GitHub setup script (Unix)"),
        (".gitignore", "Git ignore rules")
    ]
    
    files_present = 0
    for filename, description in required_files:
        if check_file_exists(filename, description):
            files_present += 1
    
    # Run all verification checks
    checks = [
        ("Core Files", files_present >= len(required_files) * 0.9),  # 90% of files
        ("Script Functionality", verify_script_functionality()),
        ("Sample Outputs", check_sample_outputs()),
        ("Assignment Requirements", verify_assignment_requirements()),
        ("Code Quality", check_code_quality())
    ]
    
    # Final assessment
    print("\n" + "=" * 70)
    print("📊 FINAL VERIFICATION RESULTS:")
    print("=" * 70)
    
    passed_checks = 0
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
        if result:
            passed_checks += 1
    
    success_rate = (passed_checks / len(checks)) * 100
    print(f"\n📈 Overall Success Rate: {passed_checks}/{len(checks)} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("\n🎉 SUBMISSION READY!")
        print("✅ All critical components verified and ready for GitHub submission")
        print("🚀 Ready to push to RedLens branch for BeyondChats evaluation")
    elif success_rate >= 75:
        print("\n⚠️  MOSTLY READY")
        print("📋 Minor issues detected - review failed checks above")
        print("🔧 Consider fixing issues before submission")
    else:
        print("\n❌ NOT READY FOR SUBMISSION")
        print("🚨 Critical issues detected - please resolve before submitting")
        
    print("\n" + "=" * 70)
    print("🎯 Next steps:")
    print("1. Run: init_repo.bat (Windows) or init_repo.sh (Unix)")
    print("2. Create GitHub repository: 'reddit-persona-analyzer-beyondchats'")
    print("3. Push to RedLens branch")
    print("4. Submit repository URL to BeyondChats")
    print("=" * 70)

if __name__ == "__main__":
    main()
