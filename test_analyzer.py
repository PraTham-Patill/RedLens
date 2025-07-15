#!/usr/bin/env python3
"""
Test script for Reddit Persona Analyzer
========================================

This script demonstrates the functionality of the Reddit Persona Analyzer
by running it on the sample users provided in the assignment.
"""

import subprocess
import sys
import os

def run_analysis(profile_url, expected_username):
    """Run analysis for a given profile URL"""
    print(f"\n{'='*60}")
    print(f"TESTING: {profile_url}")
    print(f"Expected username: {expected_username}")
    print(f"{'='*60}")
    
    try:
        # Run the main script
        result = subprocess.run([
            sys.executable, 
            "reddit_persona_analyzer.py", 
            profile_url
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Analysis completed successfully!")
            print(f"Output:\n{result.stdout}")
            
            # Check if output file was created
            output_file = f"{expected_username}_persona.txt"
            if os.path.exists(output_file):
                print(f"✅ Output file created: {output_file}")
                
                # Show file size
                file_size = os.path.getsize(output_file)
                print(f"📄 File size: {file_size} bytes")
                
                return True
            else:
                print(f"❌ Output file not found: {output_file}")
                return False
        else:
            print(f"❌ Analysis failed with return code: {result.returncode}")
            print(f"Error output:\n{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Analysis timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False

def main():
    """Main test function"""
    print("Reddit Persona Analyzer - Test Suite")
    print("=====================================")
    print("Testing the script with assignment sample users...")
    
    # Test cases from the assignment
    test_cases = [
        ("https://www.reddit.com/user/kojied/", "kojied"),
        ("https://www.reddit.com/user/Hungry-Move-6603/", "Hungry-Move-6603")
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for profile_url, expected_username in test_cases:
        if run_analysis(profile_url, expected_username):
            success_count += 1
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests passed: {success_count}/{total_tests}")
    print(f"Success rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 All tests passed! The script is working correctly.")
    else:
        print(f"⚠️  {total_tests - success_count} test(s) failed.")
    
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
