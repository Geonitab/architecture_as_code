#!/bin/bash

# Build Release Script
# Generates all deliverables and organizes them in the release folder

set -e  # Exit on any error

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if a command exists
check_command() {
    local cmd="$1"
    local install_hint="$2"
    
    if ! command -v "$cmd" >/dev/null 2>&1; then
        log "❌ ERROR: $cmd not found"
        if [ -n "$install_hint" ]; then
            log "   Install with: $install_hint"
        fi
        return 1
    else
        log "✅ $cmd is available"
        return 0
    fi
}

# Function to verify file exists and has content
verify_file() {
    local file="$1"
    local description="$2"
    
    if [ -f "$file" ] && [ -s "$file" ]; then
        local size=$(ls -lh "$file" | awk '{print $5}')
        log "✅ $description: $file ($size)"
        return 0
    else
        log "❌ $description missing or empty: $file"
        return 1
    fi
}

# Function to verify directory has files
verify_directory() {
    local dir="$1"
    local description="$2"
    
    if [ -d "$dir" ]; then
        local count=$(find "$dir" -type f | wc -l)
        if [ "$count" -gt 0 ]; then
            log "✅ $description: $dir ($count files)"
            return 0
        else
            log "❌ $description directory empty: $dir"
            return 1
        fi
    else
        log "❌ $description directory missing: $dir"
        return 1
    fi
}

# Check required dependencies
log "🔍 Checking required dependencies..."
dependencies_ok=true

check_command "python3" "apt-get install python3" || dependencies_ok=false

# Optional but recommended dependencies
if ! check_command "pandoc" "wget pandoc .deb and dpkg -i"; then
    log "⚠️  Warning: pandoc not found - book building will be skipped"
fi

if ! check_command "mmdc" "npm install -g @mermaid-js/mermaid-cli"; then
    log "⚠️  Warning: mermaid-cli not found - diagram conversion may fail"
fi

if [ "$dependencies_ok" != true ]; then
    log "❌ Required dependencies missing. Please install them first."
    exit 1
fi

# Make scripts executable
chmod +x docs/build_book.sh 2>/dev/null || true

log "🚀 Starting complete release build process..."
log ""

# Create release directory structure
log "📁 Creating release directory structure..."
mkdir -p releases/{book,presentation,whitepapers,website}
log "✅ Release directories created:"
ls -la releases/

# 1. Generate book content first
log "📚 Step 1: Generating book content..."
if python3 generate_book.py; then
    log "✅ Book content generated successfully"
    # Verify some content was actually generated
    if [ -d "docs" ] && [ "$(find docs -name "*.md" | wc -l)" -gt 0 ]; then
        log "✅ Found $(find docs -name "*.md" | wc -l) markdown files in docs/"
    else
        log "⚠️  Warning: No markdown files found in docs/ after generation"
    fi
else
    log "❌ Failed to generate book content"
    exit 1
fi

# 2. Build all book formats
log "📖 Step 2: Building book in all formats..."
if [ -f "docs/build_book.sh" ]; then
    # Store current directory
    current_dir=$(pwd)
    
    cd docs
    chmod +x build_book.sh
    if ./build_book.sh --release; then
        log "✅ Book formats built successfully"
        # Return to original directory before verification
        cd "$current_dir"
        # Verify book files were created
        verify_file "releases/book/arkitektur_som_kod.pdf" "Book PDF"
        verify_file "releases/book/arkitektur_som_kod.epub" "Book EPUB" || true
        verify_file "releases/book/arkitektur_som_kod.docx" "Book DOCX" || true
    else
        log "❌ Failed to build book formats"
        cd "$current_dir"
        exit 1
    fi
else
    log "⚠️  docs/build_book.sh not found, skipping book build"
fi

# 3. Generate whitepapers
log "📄 Step 3: Generating whitepapers..."
if python3 generate_whitepapers.py --release; then
    log "✅ Whitepapers generated successfully"
    # Verify whitepapers were created
    verify_directory "releases/whitepapers" "Whitepapers directory"
else
    log "❌ Failed to generate whitepapers"
    exit 1
fi

# 4. Generate presentations
log "🎤 Step 4: Generating presentation materials..."
if python3 generate_presentation.py --release; then
    log "✅ Presentation materials generated successfully"
    # Verify presentation materials were created
    verify_directory "releases/presentation" "Presentation directory"
else
    log "❌ Failed to generate presentation materials"
    exit 1
fi

# 5. Website build skipped (frontend removed)
log "🌐 Step 5: Skipping website build (no frontend available)"

# 6. Generate combined whitepaper PDF (optional)
log "📑 Step 6: Generating combined whitepaper PDF..."
if command -v pandoc >/dev/null 2>&1; then
    # Create a temporary combined markdown file from all HTML whitepapers
    log "Creating combined whitepaper content..."
    echo "# Arkitektur som kod - Whitepapers Samling" > /tmp/combined_whitepapers.md
    echo "" >> /tmp/combined_whitepapers.md
    
    whitepaper_found=false
    for html_file in releases/whitepapers/*.html; do
        if [ -f "$html_file" ]; then
            whitepaper_found=true
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
    
    if [ "$whitepaper_found" = true ]; then
        # Convert to PDF
        if pandoc /tmp/combined_whitepapers.md -o releases/whitepapers/whitepapers_combined.pdf \
            --pdf-engine=xelatex \
            -V documentclass=article \
            -V geometry:margin=1in \
            --toc; then
            log "✅ Combined whitepaper PDF generated"
            verify_file "releases/whitepapers/whitepapers_combined.pdf" "Combined whitepaper PDF"
        else
            log "⚠️  Combined PDF generation failed (optional step)"
        fi
    else
        log "⚠️  No whitepaper HTML files found for combining"
    fi
    
    # Clean up
    rm -f /tmp/combined_whitepapers.md
else
    log "⚠️  Pandoc not available, skipping combined whitepaper PDF"
fi

# 7. Generate presentation PDF (if PPTX exists)
log "🎥 Step 7: Attempting to generate presentation PDF..."
if [ -f "releases/presentation/arkitektur_som_kod_presentation.pptx" ]; then
    log "⚠️  PowerPoint to PDF conversion requires additional tools (LibreOffice or similar)"
    log "   Manual conversion recommended for presentation PDF"
else
    log "ℹ️  No PPTX file found, skipping presentation PDF generation"
fi

# 8. Summary
log ""
log "🎉 Release build completed successfully!"
log ""
log "=== RELEASE SUMMARY ==="
log "📁 Release directory: $(pwd)/releases/"
log ""

log "📚 Book formats:"
ls -la releases/book/ 2>/dev/null || log "   No book files found"

log ""
log "🎤 Presentation materials:"
ls -la releases/presentation/ 2>/dev/null || log "   No presentation files found"

log ""
log "📄 Whitepapers:"
whitepaper_count=$(ls releases/whitepapers/*.html 2>/dev/null | wc -l || echo "0")
log "   $whitepaper_count HTML whitepaper files"
[ -f "releases/whitepapers/whitepapers_combined.pdf" ] && log "   ✅ Combined PDF generated"

log ""
log "🌐 Website:"
if [ -d "releases/website" ] && [ "$(ls -A releases/website)" ]; then
    website_files=$(find releases/website -type f | wc -l)
    log "   $website_files files copied to releases/website/"
else
    log "   No website files found"
fi

log ""
log "📊 Final verification:"
total_files=$(find releases/ -type f | wc -l)
total_size=$(du -sh releases/ | awk '{print $1}')
log "   Total files: $total_files"
log "   Total size: $total_size"

log ""
log "🏆 All deliverables are ready in the releases/ folder for distribution!"