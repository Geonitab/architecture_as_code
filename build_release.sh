#!/bin/bash

# Build Release Script
# Generates all deliverables and organizes them in the release folder

set -e  # Exit on any error

echo "🚀 Starting complete release build process..."
echo ""

# Create release directory structure
echo "📁 Creating release directory structure..."
mkdir -p release/{book,presentation,whitepapers,website}

# 1. Generate book content first
echo "📚 Step 1: Generating book content..."
python3 generate_book.py

# 2. Build all book formats
echo "📖 Step 2: Building book in all formats..."
cd docs
./build_book.sh --release
cd ..

# 3. Generate whitepapers
echo "📄 Step 3: Generating whitepapers..."
python3 generate_whitepapers.py --release

# 4. Generate presentations
echo "🎤 Step 4: Generating presentation materials..."
python3 generate_presentation.py --release

# 5. Build website and copy to release
echo "🌐 Step 5: Building website..."
npm run build

echo "📋 Step 6: Copying website to release folder..."
if [ -d "dist" ]; then
    rm -rf release/website/*
    cp -r dist/* release/website/
    echo "✅ Website copied to release/website/"
else
    echo "❌ Website build directory 'dist' not found"
    exit 1
fi

# 6. Generate combined whitepaper PDF (optional)
echo "📑 Step 7: Generating combined whitepaper PDF..."
if command -v pandoc >/dev/null 2>&1; then
    # Create a temporary combined markdown file from all HTML whitepapers
    echo "# Arkitektur som kod - Whitepapers Samling" > /tmp/combined_whitepapers.md
    echo "" >> /tmp/combined_whitepapers.md
    
    for html_file in release/whitepapers/*.html; do
        if [ -f "$html_file" ]; then
            # Extract content between body tags (simple approach)
            filename=$(basename "$html_file" .html)
            echo "## $filename" >> /tmp/combined_whitepapers.md
            echo "" >> /tmp/combined_whitepapers.md
            # This is a simplified extraction - in production you might want a more sophisticated approach
            grep -A 1000 "<body" "$html_file" | grep -B 1000 "</body" | sed 's/<[^>]*>//g' | sed '/^$/d' >> /tmp/combined_whitepapers.md
            echo "" >> /tmp/combined_whitepapers.md
            echo "---" >> /tmp/combined_whitepapers.md
            echo "" >> /tmp/combined_whitepapers.md
        fi
    done
    
    # Convert to PDF
    pandoc /tmp/combined_whitepapers.md -o release/whitepapers/whitepapers_combined.pdf \
        --pdf-engine=xelatex \
        -V documentclass=article \
        -V geometry:margin=1in \
        --toc || echo "⚠️  Combined PDF generation failed (optional step)"
    
    # Clean up
    rm -f /tmp/combined_whitepapers.md
else
    echo "⚠️  Pandoc not available, skipping combined whitepaper PDF"
fi

# 7. Generate presentation PDF (if PPTX exists)
echo "🎥 Step 8: Attempting to generate presentation PDF..."
if [ -f "release/presentation/arkitektur_som_kod_presentation.pptx" ]; then
    echo "⚠️  PowerPoint to PDF conversion requires additional tools (LibreOffice or similar)"
    echo "   Manual conversion recommended for presentation PDF"
else
    echo "ℹ️  No PPTX file found, skipping presentation PDF generation"
fi

# 8. Summary
echo ""
echo "🎉 Release build completed successfully!"
echo ""
echo "=== RELEASE SUMMARY ==="
echo "📁 Release directory: $(pwd)/release/"
echo ""

echo "📚 Book formats:"
ls -la release/book/ 2>/dev/null || echo "   No book files found"

echo ""
echo "🎤 Presentation materials:"
ls -la release/presentation/ 2>/dev/null || echo "   No presentation files found"

echo ""
echo "📄 Whitepapers:"
whitepaper_count=$(ls release/whitepapers/*.html 2>/dev/null | wc -l || echo "0")
echo "   $whitepaper_count HTML whitepaper files"
[ -f "release/whitepapers/whitepapers_combined.pdf" ] && echo "   ✅ Combined PDF generated"

echo ""
echo "🌐 Website:"
if [ -d "release/website" ] && [ "$(ls -A release/website)" ]; then
    website_files=$(find release/website -type f | wc -l)
    echo "   $website_files files copied to release/website/"
else
    echo "   No website files found"
fi

echo ""
echo "🏆 All deliverables are ready in the release/ folder for distribution!"