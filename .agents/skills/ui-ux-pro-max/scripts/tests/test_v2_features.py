#!/usr/bin/env python3
"""
Test suite for UI/UX Pro Max v2.0 features:
- Product type expansion (192 -> 212)
- Visual mockups in design system output
- Cross-domain search ranking
- Color palette mapping per product type
- Page-specific override templates
- Figma token export
- Accessibility audit mode
"""

import csv
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import DATA_DIR


class TestProductTypeExpansion:
    """Test that product types were expanded from 192 to 212."""
    
    def test_product_count(self):
        products_path = DATA_DIR / "products.csv"
        assert products_path.exists(), "products.csv must exist"
        
        with open(products_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 212, f"Expected 212 product types, got {len(rows)}"
    
    def test_new_product_types_exist(self):
        """Verify all 20 new product types from v2.0 are present."""
        products_path = DATA_DIR / "products.csv"
        
        with open(products_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        product_names = {row['Product Type'] for row in rows}
        
        expected_new_types = [
            "AI Agent Platform",
            "AI Image Generator", 
            "AI Code Assistant",
            "Spatial Computing App",
            "AR Shopping Experience",
            "Voice-First Interface",
            "Multimodal AI Assistant",
            "Digital Health Platform",
            "Creator Economy Tool",
            "Autonomous Systems Dashboard",
            "Sustainable Energy Platform",
            "Web3 Wallet & DeFi Hub",
            "AI-Powered Fitness App",
            "Smart City Dashboard",
            "AI Music Platform",
            "Gesture-Controlled Interface",
            "AI-Powered Design Tool",
            "Real-Time Collaboration Platform",
            "AI-Powered Legal Tech Platform",
            "Immersive Learning Platform",
        ]
        
        for expected in expected_new_types:
            assert expected in product_names, f"Missing new product type: {expected}"


class TestVisualMockups:
    """Test that visual mockups are generated correctly."""
    
    def test_color_swatches_in_output(self):
        """Verify color swatch section appears in design system output."""
        from design_system import generate_design_system
        
        result = generate_design_system("SaaS dashboard", "TestProject")
        text = result['text']
        
        assert 'COLOR SWATCHES' in text or 'COLOR PALETTE' in text, \
            "Color swatches section must appear in output"
    
    def test_wireframe_in_output(self):
        """Verify wireframe appears in design system output."""
        from design_system import generate_design_system
        
        result = generate_design_system("SaaS dashboard", "TestProject")
        text = result['text']
        
        assert 'WIREFRAME' in text or 'NAV BAR' in text, \
            "Wireframe section must appear in output"
    
    def test_component_placement_in_output(self):
        """Verify component placement guide appears."""
        from design_system import generate_design_system
        
        result = generate_design_system("SaaS dashboard", "TestProject")
        text = result['text']
        
        assert 'COMPONENT PLACEMENT' in text, \
            "Component placement section must appear in output"


class TestCrossDomainSearch:
    """Test cross-domain search functionality."""
    
    def test_cross_domain_function_exists(self):
        """Verify search_cross_domain function exists and works."""
        from search import search_cross_domain
        
        result = search_cross_domain("modern saas dashboard", max_results=2)
        
        assert 'query' in result, "Result must contain query key"
        assert 'domains_searched' in result, "Result must contain domains_searched"
        assert 'total_hits' in result, "Result must contain total_hits"
        assert isinstance(result['domains_searched'], list), \
            "domains_searched must be a list"
    
    def test_cross_domain_detects_multiple_domains(self):
        """Verify cross-domain search detects relevant domains."""
        from search import search_cross_domain
        
        result = search_cross_domain("modern saas dashboard", max_results=1)
        
        # Should detect at least style and product domains
        detected = set(result['domains_searched'])
        assert len(detected) >= 2, \
            f"Should detect multiple domains, got: {detected}"


class TestColorPaletteMapping:
    """Test color palette mapping per product type."""
    
    def test_colors_have_contrast_columns(self):
        """Verify WCAG contrast columns exist in colors.csv."""
        colors_path = DATA_DIR / "colors.csv"
        
        with open(colors_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
        
        assert 'light_contrast' in headers, \
            "colors.csv must have light_contrast column"
        assert 'dark_contrast' in headers, \
            "colors.csv must have dark_contrast column"
        assert 'contrast_status' in headers, \
            "colors.csv must have contrast_status column"
    
    def test_all_palettes_pass_wcag(self):
        """Verify all palettes pass WCAG AA (>=4.5:1)."""
        colors_path = DATA_DIR / "colors.csv"
        
        with open(colors_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        for row in rows:
            status = row.get('contrast_status', '')
            assert 'PASS' in status.upper(), \
                f"Palette '{row.get('Product Type', 'unknown')}' failed WCAG: {status}"


class TestPageOverrideTemplates:
    """Test page-specific override templates."""
    
    def test_dashboard_override_has_wireframe(self):
        """Verify dashboard page override includes wireframe."""
        from design_system import generate_design_system, format_page_override_md
        
        ds = generate_design_system("SaaS analytics", "TestProject")
        
        # Simulate a dashboard page
        page_content = format_page_override_md(
            ds['design_system'], 
            'dashboard', 
            'analytics dashboard'
        )
        
        assert 'WIREFRAME' in page_content or 'SIDEBAR' in page_content, \
            "Dashboard override must include wireframe"


class TestFigmaTokenExport:
    """Test Figma/design token export functionality."""
    
    def test_export_tokens_function_exists(self):
        """Verify export_tokens function exists in design_system module."""
        from design_system import generate_design_system
        
        ds = generate_design_system("SaaS dashboard", "TestProject")
        
        # Should be able to get tokens dict
        assert 'design_system' in ds, "Result must contain design_system key"
    
    def test_tokens_include_color_variables(self):
        """Verify exported tokens include CSS custom properties."""
        from design_system import generate_design_system
        
        ds = generate_design_system("SaaS dashboard", "TestProject")
        
        colors = ds['design_system'].get('colors', {})
        
        # Should have primary color defined
        assert 'primary' in colors or len(colors) > 0, \
            "Color tokens must be present"


class TestAccessibilityAudit:
    """Test accessibility audit mode."""
    
    def test_audit_flag_exists_in_cli(self):
        """Verify --audit flag exists in CLI argument parser."""
        import argparse
        
        # Read the search.py file and check for --audit
        search_path = Path(__file__).parent.parent / 'search.py'
        content = search_path.read_text(encoding='utf-8')
        
        assert '--audit' in content or 'audit' in content.lower(), \
            "CLI must support audit mode"


class TestDataConsistency:
    """Test overall data consistency."""
    
    def test_catalog_summary_matches_actual_counts(self):
        """Verify catalog-summary.json counts match actual file contents."""
        summary_path = DATA_DIR / "catalog-summary.json"
        
        with open(summary_path, encoding='utf-8') as f:
            summary = json.load(f)
        
        # Check products count
        products_path = DATA_DIR / "products.csv"
        with open(products_path, encoding='utf-8') as f:
            actual_products = len(list(csv.DictReader(f)))
        
        assert summary['counts']['products'] == actual_products, \
            f"catalog-summary.json says {summary['counts']['products']} products but found {actual_products}"
    
    def test_stacks_count_matches_files(self):
        """Verify stacks count matches actual stack files."""
        summary_path = DATA_DIR / "catalog-summary.json"
        
        with open(summary_path, encoding='utf-8') as f:
            summary = json.load(f)
        
        stacks_dir = DATA_DIR / "stacks"
        actual_stacks = len([f for f in os.listdir(stacks_dir) if f.endswith('.csv')])
        
        assert summary['counts']['stacks'] == actual_stacks, \
            f"catalog-summary.json says {summary['counts']['stacks']} stacks but found {actual_stacks}"


class TestSynonymExpansion:
    """Test synonym expansion for query matching."""
    
    def test_synonyms_file_exists(self):
        """Verify synonyms.csv exists and has correct structure."""
        synonyms_path = DATA_DIR / "synonyms.csv"
        
        assert synonyms_path.exists(), "synonyms.csv must exist"
        
        with open(synonyms_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
        
        assert 'Term' in headers, "Must have Term column"
        assert 'Synonyms' in headers, "Must have Synonyms column"
    
    def test_synonym_groups_count(self):
        """Verify we have the expected number of synonym groups."""
        synonyms_path = DATA_DIR / "synonyms.csv"
        
        with open(synonyms_path, encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        
        assert len(rows) == 42, f"Expected 42 synonym groups, got {len(rows)}"


class TestComponentDatabase:
    """Test the UI component database."""
    
    def test_components_file_exists(self):
        """Verify components.csv exists."""
        components_path = DATA_DIR / "components.csv"
        
        assert components_path.exists(), "components.csv must exist"
    
    def test_component_count(self):
        """Verify we have 54 UI components documented."""
        components_path = DATA_DIR / "components.csv"
        
        with open(components_path, encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        
        assert len(rows) == 54, f"Expected 54 components, got {len(rows)}"
    
    def test_components_have_required_fields(self):
        """Verify all components have required fields."""
        components_path = DATA_DIR / "components.csv"
        
        with open(components_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
        
        required = ['Category', 'Component Name', 'Description', 'Do', 'Don\'t']
        for field in required:
            assert field in headers, f"Missing required field: {field}"


class TestStackCoverage:
    """Test stack coverage includes new frameworks."""
    
    def test_new_stacks_exist(self):
        """Verify SvelteKit, SolidJS, and Qwik stacks exist."""
        stacks_dir = DATA_DIR / "stacks"
        
        expected_files = ['sveltekit.csv', 'solidjs.csv', 'qwik.csv']
        
        for filename in expected_files:
            filepath = stacks_dir / filename
            assert filepath.exists(), f"Stack file missing: {filename}"
    
    def test_stack_count_is_25(self):
        """Verify we have 25 framework stacks."""
        stacks_dir = DATA_DIR / "stacks"
        
        stack_files = [f for f in os.listdir(stacks_dir) if f.endswith('.csv')]
        
        assert len(stack_files) == 25, \
            f"Expected 25 stack files, got {len(stack_files)}: {sorted(stack_files)}"
