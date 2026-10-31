#!/usr/bin/env node
/**
 * UI/UX Pro Max CLI - Design System Generator
 * 
 * Usage:
 *   ui-ux-pro-max search "<query>" [--domain <domain>] [--stack <stack>] [-n <max-results>] [--cross-domain]
 *   ui-ux-pro-max design-system "<query>" [-p "Project Name"] [--persist] [--page <page-name>]
 *   ui-ux-pro-max validate
 * 
 * Examples:
 *   ui-ux-pro-max search "dark mode dashboard" --stack react -n 5
 *   ui-ux-pro-max design-system "SaaS analytics platform" -p "MyApp" --persist
 *   ui-ux-pro-max design-system "e-commerce luxury" -p "Shop" --variance 7 --motion 5 --density 6
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
  
  // Ensure the script exists
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
    console.error('Make sure Python 3.8+ is installed and in your PATH.');
    process.exit(1);
  }

  return result.status;
}

function printUsage() {
  console.log(`
UI/UX Pro Max - Complete Design System Generator v2.0

USAGE:
  ui-ux-pro-max <command> [options]

COMMANDS:
  search          Search the UI/UX knowledge base
  design-system   Generate a complete design system recommendation
  validate        Validate all data files for consistency
  help            Show this help message

SEARCH OPTIONS:
  "<query>"       Search query (required)
  --domain, -d    Search domain: style, color, chart, landing, product, ux, typography, icons, gsap
  --stack, -s     Stack-specific search: react, nextjs, vue, svelte, astro, swiftui, flutter, etc.
  -n, --max-results    Number of results (1-20, default: 3)
  --cross-domain       Search across multiple domains simultaneously

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

EXAMPLES:
  ui-ux-pro-max search "modern saas landing page typography" --cross-domain
  ui-ux-pro-max search "dark mode dashboard" --stack react -n 5
  ui-ux-pro-max design-system "SaaS analytics platform" -p "MyApp" --persist
  ui-ux-pro-max design-system "e-commerce luxury" -p "Shop" --variance 7 --motion 5
  ui-ux-pro-max validate

DATA:
  ${fs.existsSync(DATA_DIR) ? '✓ Data files loaded' : '✗ Data directory not found'}
  Styles: ${fs.existsSync(path.join(DATA_DIR, 'styles.csv')) ? '✓' : '✗'}
  Colors: ${fs.existsSync(path.join(DATA_DIR, 'colors.csv')) ? '✓' : '✗'}
  Products: ${fs.existsSync(path.join(DATA_DIR, 'products.csv')) ? '✓' : '✗'}
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
    // Remove 'search' from args, pass rest to search.py
    runPython('search.py', args.slice(1));
    break;
    
  case 'design-system':
  case '-ds':
  case '--design-system':
    // Pass all remaining args to search.py with --design-system flag
    const dsArgs = ['--design-system', ...args.slice(1)];
    runPython('search.py', dsArgs);
    break;
    
  case 'validate':
    runPython('validate_data.py', []);
    break;
    
  default:
    // If first arg looks like a query, treat as search
    if (!args[0].startsWith('-')) {
      console.log(`Unknown command: ${command}. Treating as search query.`);
      runPython('search.py', args);
    } else {
      printUsage();
    }
    break;
}
