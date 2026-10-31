#!/usr/bin/env node
/**
 * UI/UX Pro Max CLI - Design System Generator v2.1
 * 
 * Usage:
 *   ui-ux-pro-max search "<query>" [--domain <domain>] [--stack <stack>] [-n <max-results>] [--cross-domain]
 *   ui-ux-pro-max design-system "<query>" [-p "Project Name"] [--persist] [--page <page-name>]
 *   ui-ux-pro-max audit "<query>" [-p "Project Name"]
 *   ui-ux-pro-max export-tokens "<query>" [-p "Project Name"] --output <file>
 *   ui-ux-pro-max validate
 * 
 * Examples:
 *   ui-ux-pro-max search "modern saas landing page typography" --cross-domain
 *   ui-ux-pro-max search "dark mode dashboard" --stack react -n 5
 *   ui-ux-pro-max design-system "SaaS analytics platform" -p "MyApp" --persist
 *   ui-ux-pro-max audit "e-commerce luxury" -p "Shop"
 *   ui-ux-pro-max export-tokens "dashboard app" -p "Dashboard" --output tokens.json
 *   ui-ux-pro-max validate
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Resolve paths relative to this script's location
const SCRIPTS_DIR = path.join(__dirname, '..', 'scripts');
const DATA_DIR = path.join(__dirname, '..', 'data');
const PYTHON_PATH = process.env.PYTHON || 'python3';

function runPython(scriptName, args) {
  const scriptPath = path.join(SCRIPTS_DIR, scriptName);
  
  if (!fs.existsSync(scriptPath)) {
    console.error(`Error: Script not found: ${scriptPath}`);
    process.exit(1);
  }

  const result = spawnSync(PYTHON_PATH, [scriptPath, ...args], {
    cwd: path.join(__dirname, '..'),
    stdio: 'inherit',
    encoding: 'utf-8'
  });

  if (result.error) {
    console.error(`Error running Python: ${result.error.message}`);
    console.error('Make sure Python 3.9+ is installed and in your PATH.');
    process.exit(1);
  }

  return result.status;
}

function printUsage() {
  console.log(`
UI/UX Pro Max v2.1 - Complete Design System Generator

USAGE:
  ui-ux-pro-max <command> [options]

COMMANDS:
  search          Search the UI/UX knowledge base
  design-system   Generate a complete design system recommendation
  audit           Audit design system for WCAG accessibility compliance
  export-tokens   Export design tokens (Figma/CSS/Tailwind format)
  validate        Validate all data files for consistency
  help            Show this help message

SEARCH OPTIONS:
  "<query>"       Search query (required)
  --domain, -d    Search domain: style, color, chart, landing, product, ux, typography, icons, gsap
  --stack, -s     Stack-specific search: react, nextjs, vue, svelte, astro, swiftui, flutter, etc.
  -n, --max-results   Number of results (1-20, default: 3)
  --cross-domain    Search across multiple domains simultaneously

DESIGN-SYSTEM OPTIONS:
  "<query>"       Search query for design system generation (required)
  -p, --project-name    Project name for output header
  --persist           Save to design-system/<project>/ folder
  --page <name>       Create page-specific override file
  --variance 1-10     Design variance: 1=centered/minimal, 10=bold/asymmetric
  --motion 1-10       Motion intensity: 1=subtle, 10=complex
  --density 1-10      Visual density: 1=spacious, 10=dense/dashboard
  -o, --output-dir    Output directory for persisted files
  --force             Overwrite existing MASTER.md

AUDIT OPTIONS:
  "<query>"       Search query (required)
  -p, --project-name    Project name for output header

EXPORT-TOKENS OPTIONS:
  "<query>"       Search query (required)
  -p, --project-name    Project name for output header
  -o, --output        Output file path (default: stdout as JSON)

EXAMPLES:
  ui-ux-pro-max search "modern saas landing page typography" --cross-domain
  ui-ux-pro-max search "dark mode dashboard" --stack react -n 5
  ui-ux-pro-max design-system "SaaS analytics platform" -p "MyApp" --persist
  ui-ux-pro-max audit "e-commerce luxury" -p "Shop"
  ui-ux-pro-max export-tokens "dashboard app" -p "Dashboard" --output tokens.json
  ui-ux-pro-max validate

DATA:
  Styles: ${fs.existsSync(path.join(DATA_DIR, 'styles.csv')) ? 'OK' : 'MISSING'}
  Colors: ${fs.existsSync(path.join(DATA_DIR, 'colors.csv')) ? 'OK' : 'MISSING'}
  Products: ${fs.existsSync(path.join(DATA_DIR, 'products.csv')) ? 'OK (212 types)' : 'MISSING'}
`);
}

// Parse arguments
const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
  printUsage();
  process.exit(0);
}

const command = args[0];

switch (command) {
  case 'search':
    runPython('search.py', args.slice(1));
    break;
    
  case 'design-system':
  case '-ds':
  case '--design-system':
    const dsArgs = ['--design-system', ...args.slice(1)];
    runPython('search.py', dsArgs);
    break;
    
  case 'audit':
    // Run search with design system, then audit the result
    const auditScript = path.join(SCRIPTS_DIR, 'helpers', 'audit_cli.py');
    if (fs.existsSync(auditScript)) {
      runPython('helpers/audit_cli.py', args.slice(1));
    } else {
      // Fallback: generate design system and show accessibility info
      const dsArgs = ['--design-system', ...args.slice(1)];
      const result = spawnSync(PYTHON_PATH, [path.join(SCRIPTS_DIR, 'search.py'), ...dsArgs], {
        cwd: path.join(__dirname, '..'),
        stdio: 'pipe',
        encoding: 'utf-8'
      });
      
      if (result.stdout) {
        console.log(result.stdout);
        
        // Run audit on the generated design system
        const auditResult = spawnSync(PYTHON_PATH, [
          path.join(SCRIPTS_DIR, 'helpers', 'export_tokens.py'),
          '--audit'
        ], {
          cwd: path.join(__dirname, '..'),
          stdio: 'inherit'
        });
      }
    }
    break;
    
  case 'export-tokens':
    runPython('helpers/export_tokens.py', args.slice(1));
    break;
    
  case 'validate':
    runPython('validate_data.py', []);
    break;
    
  default:
    if (!args[0].startsWith('-')) {
      console.log(`Unknown command: ${command}. Treating as search query.`);
      runPython('search.py', args);
    } else {
      printUsage();
    }
    break;
}
