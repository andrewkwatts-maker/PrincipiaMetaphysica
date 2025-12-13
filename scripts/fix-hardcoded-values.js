/**
 * Fix Hardcoded Values Script
 *
 * Replaces hardcoded physics values in HTML with PM data references.
 * Creates proper <span class="pm-value"> elements that load from Firebase.
 *
 * Run: node scripts/fix-hardcoded-values.js [--dry-run]
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const DRY_RUN = process.argv.includes('--dry-run');

// Mapping of hardcoded values to PM paths
const VALUE_MAPPINGS = [
  // Higgs mass - various formats
  {
    patterns: [
      /125\.10\s*GeV/g,
      /125\.1\s*GeV/g,
      /125\.25\s*GeV/g,
      /m_h\s*=\s*125\.\d+/g
    ],
    replacement: '<span class="pm-value" data-pm-value="v11_final_observables.higgs_mass.m_h_GeV"></span> GeV',
    name: 'Higgs mass',
    skipInContext: ['data-pm-value', 'class="pm-value"', '<!--']
  },

  // VEV
  {
    patterns: [
      /173\.97\s*GeV/g,
      /174\s*GeV/g,
      /v\s*=\s*173\.\d+\s*GeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="v12_6_geometric_derivations.vev_pneuma.v_EW"></span> GeV',
    name: 'VEV',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // PMNS theta_23
  {
    patterns: [
      /θ[₂₃23]*\s*=\s*45\.0°/g,
      /theta_23\s*=\s*45\.0/g,
      /45\.0°(?=.*(?:maximal|mixing|atmospheric))/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="pmns_matrix.theta_23" data-format="fixed:1"></span>°',
    name: 'theta_23',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // PMNS theta_12
  {
    patterns: [
      /θ[₁₂12]*\s*=\s*33\.\d+°/g,
      /theta_12\s*=\s*33\.\d+/g,
      /33\.4\d*°(?=.*(?:solar|mixing))/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="pmns_matrix.theta_12" data-format="fixed:2"></span>°',
    name: 'theta_12',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // PMNS theta_13
  {
    patterns: [
      /θ[₁₃13]*\s*=\s*8\.\d+°/g,
      /theta_13\s*=\s*8\.\d+/g,
      /8\.5\d*°(?=.*(?:reactor|mixing))/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="pmns_matrix.theta_13" data-format="fixed:2"></span>°',
    name: 'theta_13',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Dark energy w0
  {
    patterns: [
      /w[₀0]\s*=\s*-0\.852\d*/g,
      /w_0\s*=\s*-0\.85\d*/g,
      /-0\.8528(?=.*(?:dark|energy|equation))/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="dark_energy.w0_PM" data-format="fixed:4"></span>',
    name: 'w0',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Alpha GUT inverse
  {
    patterns: [
      /1\/α[_GUT]*\s*=\s*24\.\d+/g,
      /alpha_GUT_inv\s*=\s*24\.\d+/g,
      /24\.30(?=.*(?:GUT|unification))/gi,
      /24\.68(?=.*(?:GUT|unification))/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="proton_decay.alpha_GUT_inv" data-format="fixed:2"></span>',
    name: 'alpha_GUT_inv',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // M_GUT
  {
    patterns: [
      /M[_GUT]*\s*=\s*2\.1\d*\s*×\s*10[¹⁶\^16]+\s*GeV/g,
      /2\.118\s*×\s*10\^?16\s*GeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="proton_decay.M_GUT" data-format="scientific:2"></span> GeV',
    name: 'M_GUT',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Proton lifetime
  {
    patterns: [
      /τ[_p]*\s*=\s*3\.\d+\s*×\s*10[³⁴\^34]+\s*years/g,
      /3\.87\s*×\s*10\^?34\s*years/g,
      /3\.91\s*×\s*10\^?34\s*years/g
    ],
    replacement: '<span class="pm-value" data-pm-value="proton_decay.tau_p_median" data-format="scientific:2"></span> years',
    name: 'proton_lifetime',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // KK graviton mass
  {
    patterns: [
      /m[_KK]*\s*=\s*5\.0\d*\s*TeV/g,
      /5\.00\s*TeV/g,
      /5\.02\s*TeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="kk_graviton.mass_TeV" data-format="fixed:2"></span> TeV',
    name: 'KK_graviton_mass',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Dimensions - be careful with these as they appear in text
  // Only replace in specific contexts
  {
    patterns: [
      /(?<![a-zA-Z])26D(?=\s*(?:bulk|spacetime|dimensional))/gi,
      /26-dimensional\s*bulk/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_bulk"></span>D',
    name: 'D_bulk',
    skipInContext: ['data-pm-value', 'class="pm-value"'],
    requireContext: ['bulk', 'spacetime', 'dimensional']
  },

  // Topology chi
  {
    patterns: [
      /χ\s*=\s*144/g,
      /chi\s*=\s*144/gi,
      /χ[_eff]*\s*=\s*144/g
    ],
    replacement: 'χ = <span class="pm-value" data-pm-value="topology.chi_eff"></span>',
    name: 'chi_eff',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Topology b3
  {
    patterns: [
      /b[₃3]\s*=\s*24/g,
      /b_3\s*=\s*24/g
    ],
    replacement: 'b₃ = <span class="pm-value" data-pm-value="topology.b3"></span>',
    name: 'b3',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // n_gen = 3
  {
    patterns: [
      /n[_gen]*\s*=\s*3(?=\s*(?:generation|families))/gi,
      /3\s*generations?(?=\s*(?:of|fermion))/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="topology.n_gen"></span> generations',
    name: 'n_gen',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // 13D after Sp(2,R)
  {
    patterns: [
      /(?<![a-zA-Z])13D(?=\s*(?:effective|after|space))/gi,
      /13-dimensional(?=\s*(?:effective|after|space))/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_after_sp2r"></span>D',
    name: 'D_after_sp2r',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // 26-dimensional standalone
  {
    patterns: [
      /26-dimensional(?!\s*bulk)/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_bulk"></span>-dimensional',
    name: 'D_bulk_alt',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Standalone 45.0° for theta_23
  {
    patterns: [
      /(?<![0-9])45\.0°(?![0-9])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="pmns_matrix.theta_23" data-format="fixed:1"></span>°',
    name: 'theta_23_standalone',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'latitude', 'angle=']
  },

  // delta_CP
  {
    patterns: [
      /δ[_CP]*\s*=\s*-?1\d{2}\.?\d*°/g,
      /delta_CP\s*=\s*-?1\d{2}/g
    ],
    replacement: 'δ_CP = <span class="pm-value" data-pm-value="pmns_matrix.delta_CP" data-format="fixed:1"></span>°',
    name: 'delta_CP',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Mass squared differences
  {
    patterns: [
      /Δm²₂₁\s*=\s*7\.\d+\s*×\s*10⁻⁵\s*eV²/g,
      /Δm²₃₂\s*=\s*2\.\d+\s*×\s*10⁻³\s*eV²/g
    ],
    replacement: '<span class="pm-value" data-pm-value="neutrino_mass.delta_m_sq" data-format="scientific:2"></span> eV²',
    name: 'mass_squared_diff',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Top quark mass
  {
    patterns: [
      /m[_t]*\s*=\s*172\.\d+\s*GeV/g,
      /172\.69\s*GeV/g,
      /172\.7\s*GeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="v10_2_all_fermions.quarks.t.mass_GeV" data-format="fixed:2"></span> GeV',
    name: 'm_t',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Z boson mass
  {
    patterns: [
      /m[_Z]*\s*=\s*91\.1\d+\s*GeV/g,
      /91\.19\s*GeV/g,
      /91\.2\s*GeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="gauge_bosons.Z.mass_GeV" data-format="fixed:4"></span> GeV',
    name: 'm_Z',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // W boson mass
  {
    patterns: [
      /m[_W]*\s*=\s*80\.\d+\s*GeV/g,
      /80\.377\s*GeV/g,
      /80\.4\s*GeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="gauge_bosons.W.mass_GeV" data-format="fixed:3"></span> GeV',
    name: 'm_W',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Weinberg angle
  {
    patterns: [
      /sin²θ[_W]*\s*=\s*0\.231\d*/g,
      /sin²\(θ_W\)\s*=\s*0\.231/g
    ],
    replacement: 'sin²θ_W = <span class="pm-value" data-pm-value="electroweak.sin2_theta_W" data-format="fixed:4"></span>',
    name: 'sin2_theta_W',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Tau lepton mass
  {
    patterns: [
      /m[_τ]*\s*=\s*1776\.\d+\s*MeV/g,
      /1776\.86\s*MeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="v10_2_all_fermions.leptons.tau.mass_MeV" data-format="fixed:2"></span> MeV',
    name: 'm_tau',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Bottom quark mass
  {
    patterns: [
      /m[_b]*\s*=\s*4\.1\d+\s*GeV/g,
      /4\.18\s*GeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="v10_2_all_fermions.quarks.b.mass_GeV" data-format="fixed:2"></span> GeV',
    name: 'm_b',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Standalone 26D references - MOST COMMON (942 instances)
  {
    patterns: [
      /(?<![a-zA-Z0-9])26D(?![a-zA-Z])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_bulk"></span>D',
    name: '26D_standalone',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'ATTRIBUTION']
  },

  // Standalone 13D references - VERY COMMON (868 instances)
  {
    patterns: [
      /(?<![a-zA-Z0-9])13D(?![a-zA-Z])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_after_sp2r"></span>D',
    name: '13D_standalone',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'ATTRIBUTION']
  },

  // 13-dimensional text (18 instances)
  {
    patterns: [
      /13-dimensional(?!\s*(?:effective|after|space))/gi
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_after_sp2r"></span>-dimensional',
    name: '13D_dimensional',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'ATTRIBUTION']
  },

  // 4D standalone - common for observable spacetime
  {
    patterns: [
      /(?<![a-zA-Z0-9])4D(?![a-zA-Z])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_observable"></span>D',
    name: '4D_standalone',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'ATTRIBUTION', '4D Effective']
  },

  // 7D standalone - G2 manifold dimension
  {
    patterns: [
      /(?<![a-zA-Z0-9])7D(?![a-zA-Z])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_G2"></span>D',
    name: '7D_standalone',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'ATTRIBUTION']
  },

  // 8D standalone - Spin(8) representation
  {
    patterns: [
      /(?<![a-zA-Z0-9])8D(?![a-zA-Z])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_spin8"></span>D',
    name: '8D_standalone',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'ATTRIBUTION']
  },

  // 10D standalone - string theory dimension
  {
    patterns: [
      /(?<![a-zA-Z0-9])10D(?![a-zA-Z])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_string"></span>D',
    name: '10D_standalone',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'ATTRIBUTION']
  },

  // 11D standalone - M-theory dimension
  {
    patterns: [
      /(?<![a-zA-Z0-9])11D(?![a-zA-Z])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dimensions.D_Mtheory"></span>D',
    name: '11D_standalone',
    skipInContext: ['data-pm-value', 'class="pm-value"', 'ATTRIBUTION']
  },

  // b₃=24 (15 instances)
  {
    patterns: [
      /b[₃3]\s*=\s*24(?![0-9])/g
    ],
    replacement: 'b₃ = <span class="pm-value" data-pm-value="topology.b3"></span>',
    name: 'b3_equals',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // PMNS theta_12 specific values (33.6°)
  {
    patterns: [
      /33\.6°/g
    ],
    replacement: '<span class="pm-value" data-pm-value="pmns_matrix.theta_12" data-format="fixed:1"></span>°',
    name: 'theta_12_336',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // PMNS theta_13 specific values (8.57°)
  {
    patterns: [
      /8\.57°/g
    ],
    replacement: '<span class="pm-value" data-pm-value="pmns_matrix.theta_13" data-format="fixed:2"></span>°',
    name: 'theta_13_857',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Alpha GUT 24.68 and 24.30
  {
    patterns: [
      /(?<![0-9])24\.68(?![0-9])/g,
      /(?<![0-9])24\.30(?![0-9])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="proton_decay.alpha_GUT_inv" data-format="fixed:2"></span>',
    name: 'alpha_GUT_values',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // w0 approximate value -0.85
  {
    patterns: [
      /(?<![0-9])-0\.85(?![0-9])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dark_energy.w0_PM" data-format="fixed:2"></span>',
    name: 'w0_approx',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // w0 specific values
  {
    patterns: [
      /-0\.8509/g,
      /-0\.8527/g
    ],
    replacement: '<span class="pm-value" data-pm-value="dark_energy.w0_PM" data-format="fixed:4"></span>',
    name: 'w0_specific',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // KK graviton 5.0 TeV and 5.06 TeV
  {
    patterns: [
      /5\.0\s*TeV/g,
      /5\.06\s*TeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="kk_graviton.mass_TeV" data-format="fixed:2"></span> TeV',
    name: 'KK_TeV_values',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // M_GUT specific value
  {
    patterns: [
      /2\.1181\s*×\s*10\^?16/g
    ],
    replacement: '<span class="pm-value" data-pm-value="proton_decay.M_GUT" data-format="scientific:4"></span>',
    name: 'M_GUT_specific',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Chi = 144
  {
    patterns: [
      /χ\s*=\s*144(?![0-9])/g
    ],
    replacement: 'χ = <span class="pm-value" data-pm-value="topology.chi_eff"></span>',
    name: 'chi_equals',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // n_gen = 3 pattern
  {
    patterns: [
      /n[_gen]*\s*=\s*3(?=\s|<|$)/g
    ],
    replacement: 'n_gen = <span class="pm-value" data-pm-value="topology.n_gen"></span>',
    name: 'n_gen_equals',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Higgs 125.10 GeV specific
  {
    patterns: [
      /125\.10\s*GeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="v11_final_observables.higgs_mass.m_h_GeV"></span> GeV',
    name: 'higgs_12510',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Strong coupling constant α_s
  {
    patterns: [
      /0\.1179(?![0-9])/g,
      /0\.118(?![0-9])/g
    ],
    replacement: '<span class="pm-value" data-pm-value="gauge_couplings.alpha_s_MZ" data-format="fixed:4"></span>',
    name: 'alpha_s',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Electron mass
  {
    patterns: [
      /0\.511\s*MeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="v10_2_all_fermions.leptons.e.mass_MeV" data-format="fixed:3"></span> MeV',
    name: 'm_electron',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  },

  // Muon mass
  {
    patterns: [
      /105\.66\s*MeV/g
    ],
    replacement: '<span class="pm-value" data-pm-value="v10_2_all_fermions.leptons.mu.mass_MeV" data-format="fixed:2"></span> MeV',
    name: 'm_muon',
    skipInContext: ['data-pm-value', 'class="pm-value"']
  }
];

// Directories to process
const PROCESS_DIRS = ['', 'sections', 'foundations', 'docs'];

// Files to skip - partial HTML fragments and attribution files
const SKIP_FILES = [
  'test-',
  'node_modules',
  'ATTRIBUTION',
  '.backup',
  'appendices_content.html'
];

/**
 * Check if replacement should be skipped based on context
 */
function shouldSkip(content, match, mapping) {
  const start = Math.max(0, match.index - 200);
  const end = Math.min(content.length, match.index + match[0].length + 200);
  const context = content.substring(start, end);

  // Check skip contexts
  for (const skipPattern of mapping.skipInContext || []) {
    if (context.includes(skipPattern)) {
      return true;
    }
  }

  // Check required contexts
  if (mapping.requireContext) {
    const hasRequired = mapping.requireContext.some(req =>
      context.toLowerCase().includes(req.toLowerCase())
    );
    if (!hasRequired) {
      return true;
    }
  }

  return false;
}

/**
 * Process a single file
 */
function processFile(filePath) {
  const fullPath = path.join(ROOT_DIR, filePath);
  if (!fs.existsSync(fullPath)) return null;

  let content = fs.readFileSync(fullPath, 'utf-8');
  let modified = false;
  let replacements = [];

  for (const mapping of VALUE_MAPPINGS) {
    for (const pattern of mapping.patterns) {
      // Reset regex
      pattern.lastIndex = 0;

      let match;
      const matches = [];

      // Collect all matches first
      while ((match = pattern.exec(content)) !== null) {
        if (!shouldSkip(content, match, mapping)) {
          matches.push({
            text: match[0],
            index: match.index,
            length: match[0].length
          });
        }
      }

      // Replace from end to start to preserve indices
      for (let i = matches.length - 1; i >= 0; i--) {
        const m = matches[i];
        content = content.substring(0, m.index) +
                  mapping.replacement +
                  content.substring(m.index + m.length);
        modified = true;
        replacements.push({
          original: m.text,
          replacement: mapping.replacement,
          name: mapping.name
        });
      }
    }
  }

  if (modified && !DRY_RUN) {
    fs.writeFileSync(fullPath, content);
  }

  return {
    path: filePath,
    modified,
    replacements
  };
}

/**
 * Get all HTML files
 */
function getHtmlFiles() {
  const files = [];

  for (const dir of PROCESS_DIRS) {
    const fullPath = path.join(ROOT_DIR, dir);
    if (!fs.existsSync(fullPath)) continue;

    const dirFiles = fs.readdirSync(fullPath)
      .filter(f => {
        if (!f.endsWith('.html')) return false;
        for (const skip of SKIP_FILES) {
          if (f.includes(skip)) return false;
        }
        return true;
      })
      .map(f => path.join(dir, f));

    files.push(...dirFiles);
  }

  return files;
}

/**
 * Main execution
 */
function main() {
  console.log('Fix Hardcoded Values');
  console.log('─'.repeat(70));

  if (DRY_RUN) {
    console.log('DRY RUN MODE - No files will be modified\n');
  }

  const files = getHtmlFiles();
  console.log(`Found ${files.length} HTML files to process\n`);

  let totalReplacements = 0;
  let filesModified = 0;
  const allReplacements = [];

  for (const file of files) {
    const result = processFile(file);

    if (result && result.modified) {
      filesModified++;
      totalReplacements += result.replacements.length;
      allReplacements.push(result);

      console.log(`\n${result.path}:`);
      for (const r of result.replacements.slice(0, 5)) {
        console.log(`  • ${r.name}: "${r.original.substring(0, 40)}..." → PM value`);
      }
      if (result.replacements.length > 5) {
        console.log(`  ... and ${result.replacements.length - 5} more`);
      }
    }
  }

  console.log('\n' + '─'.repeat(70));
  console.log('Summary:');
  console.log(`  Files processed:     ${files.length}`);
  console.log(`  Files modified:      ${filesModified}`);
  console.log(`  Total replacements:  ${totalReplacements}`);

  if (DRY_RUN) {
    console.log('\nRun without --dry-run to apply changes');
  }

  // Save report
  const report = {
    timestamp: new Date().toISOString(),
    dryRun: DRY_RUN,
    filesProcessed: files.length,
    filesModified,
    totalReplacements,
    details: allReplacements
  };

  const reportPath = path.join(ROOT_DIR, 'fix-hardcoded-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`\nReport saved to: ${reportPath}`);
}

main();
