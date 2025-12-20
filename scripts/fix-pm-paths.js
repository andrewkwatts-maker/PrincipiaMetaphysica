/**
 * Fix PM Path Mismatches
 *
 * Updates HTML pages to use correct paths from theory-constants-enhanced.js
 *
 * Run: node scripts/fix-pm-paths.js [--dry-run]
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const DRY_RUN = process.argv.includes('--dry-run');

// Path corrections: old_path -> correct_path
const PATH_CORRECTIONS = [
  // Case sensitivity fixes
  ['pmns_matrix.delta_CP', 'pmns_matrix.delta_cp'],
  ['pmns_matrix.avg_sigma', 'pmns_matrix.average_sigma'],

  // Renamed/restructured paths
  ['dark_energy.wa_PM', 'dark_energy.wa_PM_effective'],
  ['dark_energy.w0_DESI_central', 'desi_dr2_data.w0'],
  ['dark_energy.w0_DESI_error', 'desi_dr2_data.w0_error'],
  ['dark_energy.w0_sigma', 'dark_energy.w0_deviation_sigma'],
  ['dark_energy.planck_tension_resolved', 'dark_energy.w0_deviation_sigma'],

  // Nested structure fixes
  ['v11_final_observables.higgs_mass.m_h_GeV', 'v11_final_observables.higgs_mass.m_h_GeV'],
  ['v11_final_observables.proton_lifetime.tau_p_years', 'v11_final_observables.proton_lifetime.tau_p_years'],

  // Gauge unification paths
  ['gauge_unification.alpha_GUT_inv', 'proton_decay.alpha_GUT_inv'],

  // Shared dimensions paths
  ['shared_dimensions.d_eff', 'v10_geometric_derivations.torsion_derivation.d_eff'],
  ['shared_dimensions.shadow_kuf', 'v10_geometric_derivations.torsion_derivation.shadow_kuf'],
  ['shared_dimensions.shadow_chet', 'v10_geometric_derivations.torsion_derivation.shadow_chet'],

  // KK spectrum paths
  ['kk_spectrum.m1', 'v12_final_values.kk_graviton.m1_TeV'],
  ['kk_spectrum.sigma_m1_fb', 'v12_final_values.kk_graviton.discovery'],
  ['kk_spectrum.BR_qq', 'proton_decay_channels.BR_epi0_mean'],
  ['kk_spectrum.BR_ll', 'proton_decay_channels.BR_Knu_mean'],

  // Proton decay
  ['proton_decay.uncertainty_oom', 'proton_decay.tau_p_uncertainty_oom'],

  // Pure geometric paths (v12.7)
  ['pure_geometric.flux_stab_pure.m_h_GeV', 'v11_final_observables.higgs_mass.m_h_GeV'],
  ['pure_geometric.vev_pure.v_GeV', 'v12_6_geometric_derivations.vev_pneuma.v_EW'],
  ['pure_geometric.alpha_gut_pure.alpha_GUT_inv', 'proton_decay.alpha_GUT_inv'],
  ['pure_geometric.kk_graviton_exact.m_KK_TeV', 'v12_final_values.kk_graviton.m1_TeV'],
  ['pure_geometric.w0_predicted.w0', 'dark_energy.w0_PM'],
  ['pure_geometric.proton_lifetime_predicted.tau_p_years', 'v11_final_observables.proton_lifetime.tau_p_years'],

  // Neutrino mass ordering
  ['neutrino_mass_ordering.prob_IH', 'neutrino_mass_ordering.prob_IH_mean'],
  ['neutrino_mass_ordering.prob_NH', 'neutrino_mass_ordering.prob_NH_mean'],
  ['neutrino_mass_ordering.sum_m_IH', 'v10_1_neutrino_masses.sum_masses_eV'],
  ['neutrino_mass_ordering.sum_m_NH', 'v10_1_neutrino_masses.sum_masses_eV'],
  ['neutrino_mass_ordering.m1_IH', 'v10_1_neutrino_masses.m1_eV'],
  ['neutrino_mass_ordering.m2_NH', 'v10_1_neutrino_masses.m2_eV'],

  // V12.6 paths
  ['v12_6_geometric_derivations.vev_pneuma.v_EW', 'v12_6_geometric_derivations.vev_pneuma.v_EW'],
  ['v12_6_geometric_derivations.alpha_gut_casimir.alpha_GUT_inv', 'proton_decay.alpha_GUT_inv'],
  ['v12_6_geometric_derivations.w0_d_eff.w0', 'dark_energy.w0_PM'],
  ['v12_6_geometric_derivations.kk_graviton_fixed.m_KK_TeV', 'v12_final_values.kk_graviton.m1_TeV'],

  // V12.7 paths
  ['v12_7_pure_geometric.w0_predicted.w0', 'dark_energy.w0_PM'],
  ['v12_7_pure_geometric.alpha_gut_pure.alpha_GUT_inv', 'proton_decay.alpha_GUT_inv'],
  ['v12_7_pure_geometric.proton_lifetime_predicted.tau_p_years', 'v11_final_observables.proton_lifetime.tau_p_years'],

  // Gauge bosons
  ['gauge_bosons.Z.mass_GeV', 'v10_2_all_fermions.gauge_bosons_derived.Z_mass_GeV'],
  ['gauge_bosons.W.mass_GeV', 'v10_2_all_fermions.gauge_bosons_derived.W_mass_GeV'],

  // V12.7 pure geometric - fix remaining
  ['v12_7_pure_geometric.flux_stab_pure.m_h_GeV', 'v11_final_observables.higgs_mass.m_h_GeV'],
  ['v12_7_pure_geometric.vev_pure.v_GeV', 'v12_6_geometric_derivations.vev_pneuma.v_EW'],

  // Validation paths
  ['validation.exact_matches', 'validation.exact_matches'],
  ['validation.predictions_within_1sigma', 'validation.predictions_within_1sigma'],
  ['validation.total_predictions', 'validation.total_predictions']
];

// Directories to process
const PROCESS_DIRS = ['', 'sections', 'foundations', 'docs'];

/**
 * Process a single file
 */
function processFile(filePath) {
  const fullPath = path.join(ROOT_DIR, filePath);
  if (!fs.existsSync(fullPath)) return null;

  let content = fs.readFileSync(fullPath, 'utf-8');
  let modified = false;
  let replacements = [];

  for (const [oldPath, newPath] of PATH_CORRECTIONS) {
    if (oldPath === newPath) continue; // Skip identical paths

    // Match data-pm-value="old_path" pattern
    const pattern = new RegExp(`data-pm-value="${oldPath.replace(/\./g, '\\.')}"`, 'g');
    const replacement = `data-pm-value="${newPath}"`;

    if (pattern.test(content)) {
      content = content.replace(pattern, replacement);
      modified = true;
      replacements.push({
        old: oldPath,
        new: newPath
      });
    }
  }

  if (modified && !DRY_RUN) {
    fs.writeFileSync(fullPath, content, 'utf-8');
  }

  return { modified, replacements };
}

/**
 * Main function
 */
function main() {
  console.log('Fix PM Path Mismatches');
  console.log('─'.repeat(70));
  if (DRY_RUN) {
    console.log('DRY RUN MODE - No files will be modified\n');
  }

  // Find all HTML files
  const htmlFiles = [];
  for (const dir of PROCESS_DIRS) {
    const dirPath = path.join(ROOT_DIR, dir);
    if (!fs.existsSync(dirPath)) continue;

    const files = fs.readdirSync(dirPath);
    for (const file of files) {
      if (file.endsWith('.html')) {
        htmlFiles.push(path.join(dir, file));
      }
    }
  }

  console.log(`Found ${htmlFiles.length} HTML files to process\n`);

  let totalModified = 0;
  let totalReplacements = 0;

  for (const file of htmlFiles) {
    const result = processFile(file);
    if (result && result.modified) {
      totalModified++;
      totalReplacements += result.replacements.length;
      console.log(`\n${file}:`);
      for (const r of result.replacements) {
        console.log(`  • "${r.old}" → "${r.new}"`);
      }
    }
  }

  console.log('\n' + '─'.repeat(70));
  console.log('Summary:');
  console.log(`  Files modified:      ${totalModified}`);
  console.log(`  Total replacements:  ${totalReplacements}`);

  if (DRY_RUN) {
    console.log('\nRun without --dry-run to apply changes.');
  }
}

main();
