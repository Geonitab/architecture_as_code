#!/bin/bash

# Build Release Script
# Generates all deliverables and organizes them in the release folder

set -e  # Exit on any error

# Function to check if a command exists
check_command() {
    local cmd="$1"
    local install_hint="$2"
    
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "❌ ERROR: $cmd not found"
        if [ -n "$install_hint" ]; then
            echo "   Install with: $install_hint"
        fi
        return 1
    else
        echo "✅ $cmd is available"
        return 0
    fi
}

# Check required dependencies
echo "🔍 Checking required dependencies..."
dependencies_ok=true

check_command "python3" "apt-get install python3" || dependencies_ok=false
check_command "node" "install Node.js from https://nodejs.org/" || dependencies_ok=false
check_command "npm" "install Node.js from https://nodejs.org/" || dependencies_ok=false

# Optional but recommended dependencies
if ! check_command "pandoc" "wget pandoc .deb and dpkg -i"; then
    echo "⚠️  Warning: pandoc not found - book building will be skipped"
fi

if ! check_command "mmdc" "npm install -g @mermaid-js/mermaid-cli"; then
    echo "⚠️  Warning: mermaid-cli not found - diagram conversion may fail"
fi

if [ "$dependencies_ok" != true ]; then
    echo "❌ Required dependencies missing. Please install them first."
    exit 1
fi

# Make scripts executable
chmod +x docs/build_book.sh 2>/dev/null || true

echo "🚀 Starting complete release build process..."
echo ""

# Create release directory structure
echo "📁 Creating release directory structure..."
mkdir -p releases/{book,presentation,whitepapers,website}

# 1. Generate book content first
echo "📚 Step 1: Generating book content..."
if python3 generate_book.py; then
    echo "✅ Book content generated successfully"
else
    echo "❌ Failed to generate book content"
    exit 1
fi

# 2. Build all book formats
echo "📖 Step 2: Building book in all formats..."
if [ -f "docs/build_book.sh" ]; then
    cd docs
    chmod +x build_book.sh
    if ./build_book.sh --release; then
        echo "✅ Book formats built successfully"
    else
        echo "❌ Failed to build book formats"
        exit 1
    fi
    cd ..
else
    echo "⚠️  docs/build_book.sh not found, skipping book build"
fi

# 3. Generate whitepapers
echo "📄 Step 3: Generating whitepapers..."
if python3 generate_whitepapers.py --release; then
    echo "✅ Whitepapers generated successfully"
else
    echo "❌ Failed to generate whitepapers"
    exit 1
fi

# 4. Generate presentations
echo "🎤 Step 4: Generating presentation materials..."
if python3 generate_presentation.py --release; then
    echo "✅ Presentation materials generated successfully"
else
    echo "❌ Failed to generate presentation materials"
    exit 1
fi

# 5. Build website and copy to release
echo "🌐 Step 5: Building website..."
if command -v npm >/dev/null 2>&1; then
    if npm run build; then
        echo "✅ Website built successfully"
    else
        echo "❌ Website build failed"
        exit 1
    fi
else
    echo "⚠️  npm not found, skipping website build"
    exit 1
fi

echo "📋 Step 6: Copying website to release folder..."
if [ -d "dist" ]; then
    rm -rf releases/website/*
    cp -r dist/* releases/website/
    echo "✅ Website copied to releases/website/"
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
    
    for html_file in releases/whitepapers/*.html; do
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
    pandoc /tmp/combined_whitepapers.md -o releases/whitepapers/whitepapers_combined.pdf \
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
if [ -f "releases/presentation/arkitektur_som_kod_presentation.pptx" ]; then
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
echo "📁 Release directory: $(pwd)/releases/"
echo ""

echo "📚 Book formats:"
ls -la releases/book/ 2>/dev/null || echo "   No book files found"

echo ""
echo "🎤 Presentation materials:"
ls -la releases/presentation/ 2>/dev/null || echo "   No presentation files found"

echo ""
echo "📄 Whitepapers:"
whitepaper_count=$(ls releases/whitepapers/*.html 2>/dev/null | wc -l || echo "0")
echo "   $whitepaper_count HTML whitepaper files"
[ -f "releases/whitepapers/whitepapers_combined.pdf" ] && echo "   ✅ Combined PDF generated"

echo ""
echo "🌐 Website:"
if [ -d "releases/website" ] && [ "$(ls -A releases/website)" ]; then
    website_files=$(find releases/website -type f | wc -l)
    echo "   $website_files files copied to releases/website/"
else
    echo "   No website files found"
fi

echo ""
echo "🏆 All deliverables are ready in the releases/ folder for distribution!"