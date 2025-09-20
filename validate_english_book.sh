#!/bin/bash

echo "=== English Book Generation Validation ==="
echo "This script validates the English book generation process"
echo

# Check if English docs directory exists
if [ -d "english/docs" ]; then
    echo "✅ English docs directory exists"
else
    echo "❌ English docs directory missing"
    exit 1
fi

# Check for markdown files
echo "📄 Checking for English markdown files:"
cd english/docs
markdown_count=0
for file in *.md; do
    if [ -f "$file" ]; then
        echo "  ✅ $file ($(wc -l < "$file") lines)"
        markdown_count=$((markdown_count + 1))
    fi
done
echo "📊 Total markdown files: $markdown_count"

# Check for Mermaid diagrams
echo
echo "🖼️ Checking for English Mermaid diagrams:"
diagram_count=0
if [ -d "images" ]; then
    for file in images/*.mmd; do
        if [ -f "$file" ]; then
            echo "  ✅ $file"
            diagram_count=$((diagram_count + 1))
        fi
    done
else
    echo "  ⚠️ Images directory not found"
fi
echo "📊 Total Mermaid diagrams: $diagram_count"

# Check build script
echo
echo "🔨 Checking English build script:"
if [ -f "build_book_en.sh" ] && [ -x "build_book_en.sh" ]; then
    echo "  ✅ build_book_en.sh exists and is executable"
else
    echo "  ❌ build_book_en.sh missing or not executable"
fi

# Check for required files for minimal book build
echo
echo "📚 Checking for core English chapters:"
required_files=("01_introduction.md" "02_chapter1.md" "21_conclusion.md" "22_glossary.md" "23_about_authors.md")
missing_count=0
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        missing_count=$((missing_count + 1))
    fi
done

echo
echo "=== Summary ==="
echo "📄 Markdown files: $markdown_count"
echo "🖼️ Mermaid diagrams: $diagram_count"
echo "❌ Missing required files: $missing_count"

if [ $missing_count -eq 0 ]; then
    echo "✅ All core files present - English book ready for generation"
    echo
    echo "To build the English PDF (when Pandoc is available):"
    echo "  cd english/docs && ./build_book_en.sh"
    echo
    echo "Expected output: architecture_as_code.pdf"
else
    echo "⚠️  Some core files missing, but partial build possible"
fi

echo
echo "🌐 GitHub Actions workflow: english/.github/workflows/build-book-en.yml"
echo "🔄 Book generator: generate_book_en.py"
echo "📱 English UI: english/src/pages/Index.tsx"