#!/usr/bin/env python3
"""CLI entry point for accessibility audit mode."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core import search
from helpers.export_tokens import audit_accessibility


def main():
    parser = argparse.ArgumentParser(description='Audit design system for WCAG accessibility')
    parser.add_argument('query', help='Search query (e.g., "SaaS dashboard")')
    parser.add_argument('--project-name', '-p', default=None, help='Project name')
    
    args = parser.parse_args()
    
    # Generate design system from query
    result = search(args.query)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    
    # Build a minimal design_system dict for audit
    colors_data = {}
    typography_data = {}
    
    # Extract colors from search results
    color_results = []
    style_results = result.get('results', [])
    
    # Try to get color data from the product/style match
    if result.get('domain') == 'color':
        for row in result.get('results', []):
            for key in ['primary', 'secondary', 'accent', 'background', 'card', 'muted', 'border', 'destructive']:
                if key in row:
                    colors_data[key] = row[key]
    
    # Extract typography
    typ_results = search(args.query, domain='typography')
    if typ_results.get('results'):
        for row in typ_results['results'][:1]:
            typography_data['heading'] = row.get('Heading Font', '')
            typography_data['body'] = row.get('Body Font', '')
    
    design_system = {
        'project_name': args.project_name or 'Audit Project',
        'colors': colors_data,
        'typography': typography_data,
        'spacing_scale': {
            'xs': '4px', 'sm': '8px', 'md': '16px',
            'lg': '24px', 'xl': '32px', '2xl': '48px', '3xl': '64px'
        }
    }
    
    # Run audit
    audit_result = audit_accessibility(design_system)
    
    print(f"\n{'='*60}")
    print(f"  ACCESSIBILITY AUDIT - {design_system['project_name']}")
    print(f"{'='*60}\n")
    
    if audit_result['passed']:
        print("RESULT: PASS - All checks passed!")
    else:
        print(f"RESULT: {'PASS' if not any(i['status'] == 'FAIL' for i in audit_result['issues']) else 'WARN'} - {audit_result['summary']}")
    
    print("\n--- Checks ---\n")
    for check in audit_result['checks']:
        status_icon = {'PASS': '[OK]', 'WARNING': '[!!]', 'FAIL': '[XX]', 'SKIP': '[--]'}[check['status']]
        print(f"  {status_icon} {check['check']}")
        if check.get('detail'):
            print(f"       {check['detail']}")
    
    if audit_result['issues']:
        print("\n--- Issues ---\n")
        for issue in audit_result['issues']:
            status_icon = {'PASS': '[OK]', 'WARNING': '[!!]', 'FAIL': '[XX]', 'SKIP': '[--]'}[issue['status']]
            print(f"  {status_icon} {issue['check']}")
            print(f"       Detail: {issue.get('detail', '')}")
            if issue.get('recommendation'):
                print(f"       Fix: {issue['recommendation']}")
    
    print(f"\n{'='*60}\n")


if __name__ == '__main__':
    main()
