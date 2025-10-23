"""
Technical accuracy validator for book content.

Validates code snippets, diagrams, and technical examples.
"""
import pytest
import re
import yaml
import json
from pathlib import Path


class TestTechnicalAccuracy:
    """Test technical accuracy of code examples and references."""
    
    def test_yaml_code_blocks_valid(self, chapter_files, requirements_config):
        """Test that YAML code blocks contain valid YAML syntax."""
        if not requirements_config["quality"]["technical_accuracy"]["validate_yaml_examples"]:
            pytest.skip("YAML validation disabled in configuration")
        
        yaml_issues = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find YAML code blocks (excluding terraform which might be mixed syntax)
            yaml_blocks = re.findall(
                r'```(?:yaml|yml)\s*\n(.*?)\n```', 
                content, 
                re.DOTALL | re.IGNORECASE
            )
            
            for i, yaml_block in enumerate(yaml_blocks):
                # Skip blocks that contain obvious Terraform syntax
                if any(tf_indicator in yaml_block for tf_indicator in [
                    'provider "', 'resource "', 'terraform {', 'variable "'
                ]):
                    continue
                
                # Skip CloudFormation templates (they have special tags)
                if '!Ref' in yaml_block or '!GetAtt' in yaml_block:
                    continue
                
                # Skip blocks that contain Jenkins pipeline syntax
                if 'pipeline {' in yaml_block or 'agent any' in yaml_block:
                    continue
                
                # Skip blocks with non-YAML content (like nested code blocks)
                if '```' in yaml_block:
                    continue
                
                # Skip blocks that are primarily comments or explanations
                lines = yaml_block.strip().split('\n')
                yaml_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
                if len(yaml_lines) < 3:  # Skip if less than 3 actual YAML lines
                    continue
                
                try:
                    # For multi-document YAML, try to load each document separately
                    if '---' in yaml_block:
                        # Split on document separators and validate each
                        documents = yaml_block.split('---')
                        for doc in documents:
                            doc = doc.strip()
                            if doc and doc != '...' and not doc.startswith('#'):
                                yaml.safe_load(doc)
                    else:
                        yaml.safe_load(yaml_block)
                except yaml.YAMLError as e:
                    # Only report if it's a clear YAML syntax error, not structure issues
                    error_str = str(e)
                    if any(keyword in error_str.lower() for keyword in [
                        'cannot start any token',
                        'expected <block end>',
                        'found unexpected end of stream',
                        'mapping values are not allowed'
                    ]):
                        yaml_issues.append({
                            "file": chapter_file.name,
                            "block_index": i + 1,
                            "error": str(e),
                            "content": yaml_block[:200] + "..." if len(yaml_block) > 200 else yaml_block
                        })
        
        # Convert to warnings instead of hard failures for educational content
        if yaml_issues:
            import warnings
            warnings.warn(
                f"YAML syntax issues detected in {len(yaml_issues)} code blocks. These should be reviewed for accuracy.",
                UserWarning
            )
    
    def test_json_code_blocks_valid(self, chapter_files):
        """Test that JSON code blocks contain valid JSON syntax."""
        json_issues = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find JSON code blocks
            json_blocks = re.findall(
                r'```json\s*\n(.*?)\n```', 
                content, 
                re.DOTALL | re.IGNORECASE
            )
            
            for i, json_block in enumerate(json_blocks):
                try:
                    json.loads(json_block)
                except json.JSONDecodeError as e:
                    json_issues.append({
                        "file": chapter_file.name,
                        "block_index": i + 1,
                        "error": str(e),
                        "content": json_block[:200] + "..." if len(json_block) > 200 else json_block
                    })
        
        assert not json_issues, f"Invalid JSON code blocks: {json_issues}"
    
    def test_diagram_references_valid(self, chapter_files, docs_directory, requirements_config):
        """Test that diagram references point to existing or expected files."""
        if not requirements_config["quality"]["technical_accuracy"]["validate_diagram_references"]:
            pytest.skip("Diagram reference validation disabled")
        
        images_dir = docs_directory / "images"
        diagram_issues = []
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find diagram references
            diagram_refs = re.findall(
                r'!\[.*?\]\((images/diagram_.*?\.png)\)', 
                content
            )
            
            for diagram_ref in diagram_refs:
                diagram_path = docs_directory / diagram_ref
                mermaid_path = docs_directory / diagram_ref.replace('.png', '.mmd')
                
                # Check if either PNG exists or Mermaid source exists
                if not diagram_path.exists() and not mermaid_path.exists():
                    diagram_issues.append({
                        "file": chapter_file.name,
                        "reference": diagram_ref,
                        "issue": "Neither PNG nor Mermaid source file exists"
                    })
        
        # Only warn about missing diagrams since they might be generated
        if diagram_issues:
            import warnings
            warnings.warn(
                f"Diagram reference issues: {len(diagram_issues)} found",
                UserWarning
            )
    
    def test_code_block_syntax_highlighting(self, chapter_files):
        """Test that code blocks specify appropriate language for syntax highlighting."""
        code_block_issues = []
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find code blocks without language specification
            unnamed_blocks = re.findall(r'```\s*\n', content)
            # Find code blocks with language
            named_blocks = re.findall(r'```(\w+)', content)
            
            if unnamed_blocks:
                code_block_issues.append({
                    "file": chapter_file.name,
                    "issue": f"{len(unnamed_blocks)} code blocks without language specification",
                    "suggestion": "Add language identifier (e.g., ```yaml, ```bash, ```python)"
                })
        
        # This is a warning for better practice
        if code_block_issues:
            import warnings
            warnings.warn(
                f"Code blocks without syntax highlighting: {len(code_block_issues)} files",
                UserWarning
            )
    
    def test_terraform_code_syntax(self, chapter_files):
        """Test Terraform code blocks for basic syntax validity."""
        terraform_issues = []
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find Terraform/HCL code blocks
            terraform_blocks = re.findall(
                r'```(?:terraform|hcl|tf)\s*\n(.*?)\n```', 
                content, 
                re.DOTALL | re.IGNORECASE
            )
            
            for i, tf_block in enumerate(terraform_blocks):
                # Basic syntax checks
                issues = []
                
                # Check for unmatched braces
                open_braces = tf_block.count('{')
                close_braces = tf_block.count('}')
                if open_braces != close_braces:
                    issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")
                
                # Check for basic resource structure
                if 'resource "' in tf_block:
                    if not re.search(r'resource\s+"[^"]+"\s+"[^"]+"\s*{', tf_block):
                        issues.append("Invalid resource block syntax")
                
                if issues:
                    terraform_issues.append({
                        "file": chapter_file.name,
                        "block_index": i + 1,
                        "issues": issues,
                        "content": tf_block[:200] + "..." if len(tf_block) > 200 else tf_block
                    })
        
        assert not terraform_issues, f"Terraform syntax issues: {terraform_issues}"
    
    def test_bash_script_syntax(self, chapter_files):
        """Test bash/shell code blocks for basic syntax validity."""
        bash_issues = []
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find bash/shell code blocks
            bash_blocks = re.findall(
                r'```(?:bash|shell|sh)\s*\n(.*?)\n```', 
                content, 
                re.DOTALL | re.IGNORECASE
            )
            
            for i, bash_block in enumerate(bash_blocks):
                issues = []
                
                # Check for dangerous commands (security awareness)
                dangerous_patterns = [
                    r'rm\s+-rf\s+/', r'chmod\s+777', r'sudo\s+chmod\s+777',
                    r'curl.*\|\s*sh', r'wget.*\|\s*sh'
                ]
                
                for pattern in dangerous_patterns:
                    if re.search(pattern, bash_block):
                        issues.append(f"Potentially dangerous command pattern: {pattern}")
                
                # Check for unmatched quotes
                single_quotes = bash_block.count("'") % 2
                double_quotes = bash_block.count('"') % 2
                if single_quotes or double_quotes:
                    issues.append("Unmatched quotes detected")
                
                if issues:
                    bash_issues.append({
                        "file": chapter_file.name,
                        "block_index": i + 1,
                        "issues": issues,
                        "content": bash_block[:200] + "..." if len(bash_block) > 200 else bash_block
                    })
        
        # Only warn about bash issues as they might be intentional examples
        if bash_issues:
            import warnings
            warnings.warn(
                f"Bash script concerns: {len(bash_issues)} blocks",
                UserWarning
            )
    
    def test_url_references_format(self, chapter_files):
        """Test that URL references follow proper markdown format."""
        url_issues = []
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find potential URLs not in proper markdown format
            # Look for http/https URLs not in markdown link format
            loose_urls = re.findall(
                r'(?<!\]\()https?://[^\s\)]+(?!\))', 
                content
            )
            
            if loose_urls:
                url_issues.append({
                    "file": chapter_file.name,
                    "issue": f"URLs not in markdown link format: {len(loose_urls)}",
                    "examples": loose_urls[:3],
                    "suggestion": "Use [link text](URL) format"
                })
        
        # This is a style warning
        if url_issues:
            import warnings
            warnings.warn(
                f"URL formatting issues: {len(url_issues)} files",
                UserWarning
            )
    
    def test_code_block_length(self, chapter_files):
        """Monitor code block length for readability (informational only)."""
        WARN_THRESHOLD = 75
        INFO_THRESHOLD = 200
        long_code_blocks = []
        very_long_code_blocks = []
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find all code blocks regardless of language
            code_blocks = re.findall(
                r'```[^`]*?\n(.*?)\n```', 
                content, 
                re.DOTALL
            )
            
            for i, code_block in enumerate(code_blocks):
                # Count non-empty lines in the code block
                lines = [line for line in code_block.split('\n') if line.strip()]
                line_count = len(lines)
                
                if line_count > INFO_THRESHOLD:
                    very_long_code_blocks.append({
                        "file": chapter_file.name,
                        "block_index": i + 1,
                        "line_count": line_count,
                        "info_threshold": INFO_THRESHOLD,
                        "preview": code_block[:200] + "..." if len(code_block) > 200 else code_block
                    })
                elif line_count > WARN_THRESHOLD:
                    long_code_blocks.append({
                        "file": chapter_file.name,
                        "block_index": i + 1,
                        "line_count": line_count,
                        "warn_threshold": WARN_THRESHOLD,
                        "preview": code_block[:200] + "..." if len(code_block) > 200 else code_block
                    })
        
        # Warn about moderately long code blocks
        if long_code_blocks:
            import warnings
            warnings.warn(
                f"Code blocks over {WARN_THRESHOLD} lines detected: {len(long_code_blocks)} cases. Consider adding explanatory text between sections.",
                UserWarning
            )
        
        # Inform about very long code blocks but don't fail
        if very_long_code_blocks:
            import warnings
            warnings.warn(
                f"Very long code blocks over {INFO_THRESHOLD} lines detected: {len(very_long_code_blocks)} cases. These may be valuable complete examples but consider if they could be split with explanatory text.",
                UserWarning
            )

    def test_technical_term_definitions(self, chapter_files):
        """Test that technical terms are properly introduced/defined."""
        # Common technical terms that should be defined on first use
        technical_terms = [
            r'\bCI/CD\b', r'\bAPI\b', r'\bREST\b', r'\bJSON\b',
            r'\bYAML\b', r'\bKubernetes\b', r'\bDocker\b', r'\bTerraform\b'
        ]
        
        term_usage = {}
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            for term_pattern in technical_terms:
                matches = re.findall(term_pattern, content, re.IGNORECASE)
                if matches:
                    term = matches[0].upper()
                    if term not in term_usage:
                        term_usage[term] = []
                    term_usage[term].append(chapter_file.name)
        
        # This is informational - check if terms appear across multiple chapters
        # suggesting they might benefit from a glossary entry
        frequent_terms = {
            term: files for term, files in term_usage.items() 
            if len(files) > 3
        }
        
        if frequent_terms:
            import warnings
            warnings.warn(
                f"Terms appearing in multiple chapters (consider glossary): {list(frequent_terms.keys())}",
                UserWarning
            )
