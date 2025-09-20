#!/bin/bash
#
# Docs Directory Protection Validator
# 
# This script validates changes to the docs directory to ensure:
# 1. No excessive content deletions from chapter files
# 2. Chapter files maintain minimum content length
# 3. Critical files are not deleted
#
# Usage: ./scripts/validate-docs-protection.sh [base-branch]
#

set -e

# Configuration
MAX_DELETIONS_RATIO=0.1  # Maximum 10% of lines can be deleted
MIN_CONTENT_LENGTH=100   # Minimum content length for chapter files
BASE_BRANCH=${1:-"main"} # Default to main branch

echo "=== Docs Directory Protection Validator ==="
echo "Base branch: $BASE_BRANCH"
echo "Max deletion ratio: $MAX_DELETIONS_RATIO"
echo "Min content length: $MIN_CONTENT_LENGTH lines"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if base branch exists
if ! git rev-parse --verify "origin/$BASE_BRANCH" > /dev/null 2>&1; then
    echo "❌ Error: Base branch 'origin/$BASE_BRANCH' not found"
    echo "Available branches:"
    git branch -r
    exit 1
fi

echo "📥 Fetching latest changes from base branch..."
git fetch origin "$BASE_BRANCH" --quiet

# Get list of changed files in docs directory
echo "🔍 Analyzing changes to docs directory..."
changed_files=$(git diff --name-only "origin/$BASE_BRANCH"...HEAD | grep '^docs/' || true)

if [ -z "$changed_files" ]; then
    echo "✅ No changes detected in docs directory"
    echo "Protection validation: PASSED"
    exit 0
fi

echo "Changed files in docs directory:"
echo "$changed_files" | sed 's/^/  - /'
echo ""

# Analyze each changed file
validation_failed=false
critical_files_modified=false
issues_found=()

for file in $changed_files; do
    echo "--- Analyzing $file ---"
    
    if [ -f "$file" ]; then
        # Get diff stats
        diff_stats=$(git diff --numstat "origin/$BASE_BRANCH"...HEAD -- "$file")
        added=$(echo "$diff_stats" | awk '{print $1}')
        deleted=$(echo "$diff_stats" | awk '{print $2}')
        
        # Skip if no diff stats (binary files, etc.)
        if [ "$added" = "-" ] || [ "$deleted" = "-" ]; then
            echo "  ℹ️ Skipping binary or problematic file"
            continue
        fi
        
        # Convert to numbers (handle empty values)
        added=${added:-0}
        deleted=${deleted:-0}
        
        echo "  Lines added: $added"
        echo "  Lines deleted: $deleted"
        
        # Check if this is a critical chapter file
        if echo "$file" | grep -E '^docs/[0-9]+_.*\.md$' > /dev/null; then
            critical_files_modified=true
            echo "  ⚠️ Critical chapter file modified"
        fi
        
        # Check for excessive deletions
        if [ "$deleted" -gt 0 ]; then
            if [ "$added" -eq 0 ]; then
                deletion_ratio="1.0"  # 100% deletion if no additions
            else
                # Calculate deletion ratio using awk for better compatibility
                deletion_ratio=$(awk "BEGIN {printf \"%.3f\", $deleted / ($added + $deleted)}")
            fi
            
            echo "  Deletion ratio: $deletion_ratio"
            
            # Check if deletion ratio exceeds threshold (using awk for comparison)
            if awk "BEGIN {exit !($deletion_ratio > $MAX_DELETIONS_RATIO)}"; then
                echo "  ❌ EXCESSIVE DELETIONS DETECTED!"
                echo "  This file has $deletion_ratio deletion ratio (threshold: $MAX_DELETIONS_RATIO)"
                validation_failed=true
                issues_found+=("$file: ${deleted} lines deleted, ${added} lines added (${deletion_ratio} deletion ratio)")
            fi
        fi
        
        # Check file content length for chapter files
        if echo "$file" | grep -E '^docs/[0-9]+_.*\.md$' > /dev/null; then
            content_length=$(wc -l < "$file" 2>/dev/null || echo "0")
            echo "  Current content length: $content_length lines"
            
            if [ "$content_length" -lt "$MIN_CONTENT_LENGTH" ]; then
                echo "  ❌ CONTENT TOO SHORT!"
                echo "  Chapter file has only $content_length lines (minimum: $MIN_CONTENT_LENGTH)"
                validation_failed=true
                issues_found+=("$file: Only ${content_length} lines of content (minimum: ${MIN_CONTENT_LENGTH})")
            fi
        fi
        
    else
        echo "  📄 File deleted"
        if echo "$file" | grep -E '^docs/[0-9]+_.*\.md$' > /dev/null; then
            echo "  ❌ CRITICAL CHAPTER FILE DELETED!"
            validation_failed=true
            critical_files_modified=true
            issues_found+=("$file: Critical chapter file was deleted")
        fi
    fi
    
    echo ""
done

# Summary
echo "=== VALIDATION SUMMARY ==="

if [ "$validation_failed" = "true" ]; then
    echo "❌ VALIDATION FAILED"
    echo ""
    echo "Issues found:"
    for issue in "${issues_found[@]}"; do
        echo "  - $issue"
    done
    echo ""
    echo "Protection Rules:"
    echo "  - Chapter files must not have excessive content deletions (max $(echo "$MAX_DELETIONS_RATIO * 100" | bc -l | cut -d. -f1)% deletion ratio)"
    echo "  - Chapter files must maintain minimum content length ($MIN_CONTENT_LENGTH lines)"
    echo "  - Critical chapter files should not be deleted"
    echo ""
    if [ "$critical_files_modified" = "true" ]; then
        echo "⚠️ Critical chapter files have been modified."
        echo "   If this is intentional, please provide justification."
    fi
    echo ""
    echo "Action Required: Please review and adjust your changes to the docs directory."
    exit 1
else
    echo "✅ VALIDATION PASSED"
    echo "Changes to docs directory are within acceptable limits."
    if [ "$critical_files_modified" = "true" ]; then
        echo ""
        echo "ℹ️ Note: Critical chapter files were modified, but changes are within acceptable limits."
    fi
    exit 0
fi