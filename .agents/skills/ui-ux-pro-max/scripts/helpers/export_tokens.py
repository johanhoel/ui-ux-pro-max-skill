#!/usr/bin/env python3
"""Export design system tokens to Figma Tokens / CSS / Tailwind formats."""


def export_figma_tokens(design_system: dict) -> dict:
    """
    Export design system tokens in Figma-compatible format.
    
    Returns a dict with figma_tokens, css_variables, and tailwind_config.
    """
    colors = design_system.get('colors', {})
    typography = design_system.get('typography', {})
    
    # Build color tokens for Figma
    figma_colors = {}
    semantic_roles = {
        'primary': 'Primary Brand Color',
        'on_primary': 'Text on Primary Background',
        'secondary': 'Secondary Brand Color',
        'on_secondary': 'Text on Secondary Background',
        'accent': 'Accent / CTA Color',
        'background': 'Page Background',
        'card': 'Card Background',
        'muted': 'Muted / Disabled State',
        'border': 'Border / Divider Color',
        'destructive': 'Error / Destructive Action',
    }
    
    for role, label in semantic_roles.items():
        hex_val = colors.get(role, '')
        if hex_val:
            figma_colors[role] = {
                'value': hex_val,
                'description': label,
                'type': 'color'
            }
    
    # Build typography tokens
    figma_typography = {}
    heading_font = typography.get('heading', '')
    body_font = typography.get('body', '')
    
    if heading_font:
        figma_typography['font-family-heading'] = {
            'value': heading_font,
            'description': 'Heading font family',
            'type': 'fontFamilies'
        }
    if body_font:
        figma_typography['font-family-body'] = {
            'value': body_font,
            'description': 'Body font family',
            'type': 'fontFamilies'
        }
    
    # Build CSS custom properties
    css_lines = [
        '/* UI/UX Pro Max Design Tokens */',
        '/* Generated automatically - do not edit manually */',
        '',
        ':root {'
    ]
    
    for role, token in figma_colors.items():
        if isinstance(token, dict) and 'value' in token:
            css_lines.append(f'  --color-{role}: {token["value"]};')
    
    spacing = design_system.get('spacing_scale', {})
    if spacing:
        css_lines.append('')
        css_lines.append('  /* Spacing Tokens */')
        for token_name, value in spacing.items():
            css_lines.append(f'  --space-{token_name}: {value};')
    
    css_lines.extend([
        '',
        '  /* Shadow Tokens */',
        '  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);',
        '  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);',
        '  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);',
        '  --shadow-xl: 0 20px 25px rgba(0,0,0,0.15);',
        '}'
    ])
    
    # Build Tailwind config snippet
    tailwind_colors = {}
    for role in ['primary', 'secondary', 'accent', 'background', 'card', 'muted', 'border', 'destructive']:
        hex_val = colors.get(role, '')
        if hex_val:
            tailwind_colors[role] = hex_val
    
    if tailwind_colors:
        lines = ["colors:"]
        for k, v in tailwind_colors.items():
            lines.append(f'  {k}: "{v}",')
        tailwind_snippet = '\n'.join(lines)
    else:
        tailwind_snippet = "# No colors configured"

    return {
        'figma_tokens': figma_colors,
        'css_variables': '\n'.join(css_lines),
        'tailwind_config': tailwind_snippet,
        'typography': figma_typography
    }


def audit_accessibility(design_system: dict) -> dict:
    """
    Audit design system for WCAG 2.1 AA compliance.
    
    Checks color contrast ratios, font configuration, and accessibility requirements.
    Returns audit results with pass/fail status.
    """
    colors = design_system.get('colors', {})
    typography = design_system.get('typography', {})
    
    def relative_luminance(hex_color):
        """Calculate relative luminance per WCAG 2.0 spec."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return None
        try:
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        except ValueError:
            return None
        
        def linearize(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)
    
    def contrast_ratio(lum1, lum2):
        """Calculate WCAG contrast ratio."""
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        return (lighter + 0.05) / (darker + 0.05)
    
    checks = []
    issues = []
    
    # Check color pairs for sufficient contrast
    pairs_to_check = [
        ('background', 'primary', 'Primary text on background'),
        ('background', 'on_primary', 'On-primary text on background'),
        ('card', 'foreground', 'Card foreground on card bg'),
        ('muted', 'muted_foreground', 'Muted text on muted bg'),
        ('destructive', 'on_destructive', 'Destructive action text'),
    ]
    
    for bg_key, fg_key, description in pairs_to_check:
        bg_hex = colors.get(bg_key)
        fg_hex = colors.get(fg_key)
        
        if not bg_hex or not fg_hex:
            continue
        
        lum_bg = relative_luminance(bg_hex)
        lum_fg = relative_luminance(fg_hex)
        
        if lum_bg is None or lum_fg is None:
            checks.append({
                'check': description,
                'status': 'SKIP',
                'detail': f'Invalid hex color for {bg_key}/{fg_key}'
            })
            continue
        
        ratio = contrast_ratio(lum_bg, lum_fg)
        
        if ratio >= 4.5:
            checks.append({
                'check': description,
                'status': 'PASS',
                'detail': f'Contrast ratio {ratio:.2f}:1 (AA compliant)'
            })
        elif ratio >= 3.0:
            issues.append({
                'check': description,
                'status': 'WARNING',
                'detail': f'Ratio {ratio:.2f}:1 - passes for large text only',
                'recommendation': 'Use larger font or increase contrast'
            })
        else:
            issues.append({
                'check': description,
                'status': 'FAIL',
                'detail': f'Ratio {ratio:.2f}:1 - fails WCAG AA (need >=4.5:1)',
                'recommendation': f'Change color to achieve 4.5:1+ ratio'
            })
    
    # Check font configuration
    heading_font = typography.get('heading', '')
    body_font = typography.get('body', '')
    
    if heading_font:
        checks.append({
            'check': f'Heading font ({heading_font})',
            'status': 'PASS',
            'detail': 'Font family specified for headings'
        })
    else:
        issues.append({
            'check': 'Heading font',
            'status': 'WARNING',
            'detail': 'No heading font specified',
            'recommendation': 'Specify a readable heading font'
        })
    
    if body_font:
        checks.append({
            'check': f'Body font ({body_font})',
            'status': 'PASS',
            'detail': 'Font family specified for body text'
        })
    else:
        issues.append({
            'check': 'Body font',
            'status': 'WARNING',
            'detail': 'No body font specified',
            'recommendation': 'Specify a readable body font (min 16px)'
        })
    
    all_pass = len([i for i in issues if i['status'] == 'FAIL']) == 0
    
    return {
        'passed': all_pass,
        'checks': checks,
        'issues': issues,
        'summary': f'{len(checks)} checks run, {len(issues)} issue(s) found'
    }
