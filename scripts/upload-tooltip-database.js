/**
 * Upload Tooltip Database to Firebase
 *
 * Creates comprehensive formula_database entries with:
 * - Symbol and HTML representation
 * - Description and units
 * - Experimental values for comparison
 * - PM derivation paths
 *
 * Run: node scripts/upload-tooltip-database.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');
const admin = require('firebase-admin');

const ROOT_DIR = path.join(__dirname, '..');

// Find service account key
const keyPaths = [
  path.join(__dirname, 'serviceAccountKey.json'),
  path.join(__dirname, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json'),
  path.join(ROOT_DIR, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json')
];

let serviceAccountPath = null;
for (const p of keyPaths) {
  if (fs.existsSync(p)) {
    serviceAccountPath = p;
    break;
  }
}

if (!serviceAccountPath) {
  console.error('Service account key not found!');
  process.exit(1);
}

const serviceAccount = require(serviceAccountPath);

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
}

const db = admin.firestore();

// Comprehensive tooltip database
const TOOLTIP_DATABASE = {
  // ═══════════════════════════════════════════════════════════════════
  // HIGGS SECTOR
  // ═══════════════════════════════════════════════════════════════════
  m_h: {
    symbol: 'm_h',
    htmlSymbol: 'm<sub>h</sub>',
    name: 'Higgs Boson Mass',
    description: 'Mass of the Higgs boson, arising from the Mexican hat potential in the SM Higgs mechanism',
    unit: 'GeV',
    pmPath: 'v11_final_observables.higgs_mass.m_h_GeV',
    experimental: {
      value: 125.25,
      error: 0.17,
      source: 'PDG 2024'
    },
    category: 'masses',
    derivation: 'Derived from moduli stabilization of Kähler modulus Re(T)'
  },

  v_EW: {
    symbol: 'v',
    htmlSymbol: 'v',
    name: 'Electroweak VEV',
    description: 'Vacuum expectation value of the Higgs field, sets the electroweak scale',
    unit: 'GeV',
    pmPath: 'v12_6_geometric_derivations.vev_pneuma.v_EW',
    experimental: {
      value: 246.22,
      error: 0.01,
      source: 'PDG 2024 (from G_F)'
    },
    category: 'scales',
    derivation: 'Derived from Calabi-Yau Kähler modulus calibration'
  },

  // ═══════════════════════════════════════════════════════════════════
  // PMNS MATRIX
  // ═══════════════════════════════════════════════════════════════════
  theta_23: {
    symbol: 'θ₂₃',
    htmlSymbol: 'θ<sub>23</sub>',
    name: 'Atmospheric Mixing Angle',
    description: 'PMNS matrix angle governing atmospheric neutrino oscillations',
    unit: 'degrees',
    pmPath: 'pmns_matrix.theta_23',
    experimental: {
      value: 45.0,
      error: 1.0,
      source: 'NuFIT 6.0 (2025)'
    },
    category: 'pmns',
    derivation: 'Maximal mixing from α₄ = α₅ brane symmetry'
  },

  theta_12: {
    symbol: 'θ₁₂',
    htmlSymbol: 'θ<sub>12</sub>',
    name: 'Solar Mixing Angle',
    description: 'PMNS matrix angle governing solar neutrino oscillations',
    unit: 'degrees',
    pmPath: 'pmns_matrix.theta_12',
    experimental: {
      value: 33.41,
      error: 0.75,
      source: 'NuFIT 6.0 (2025)'
    },
    category: 'pmns',
    derivation: 'Geometric from TCS G2 associative 3-cycle ratios'
  },

  theta_13: {
    symbol: 'θ₁₃',
    htmlSymbol: 'θ<sub>13</sub>',
    name: 'Reactor Mixing Angle',
    description: 'PMNS matrix angle governing reactor neutrino oscillations',
    unit: 'degrees',
    pmPath: 'pmns_matrix.theta_13',
    experimental: {
      value: 8.54,
      error: 0.12,
      source: 'NuFIT 6.0 (2025)'
    },
    category: 'pmns',
    derivation: 'Geometric from TCS G2 coassociative cycle structure'
  },

  delta_CP: {
    symbol: 'δ_CP',
    htmlSymbol: 'δ<sub>CP</sub>',
    name: 'Dirac CP Phase',
    description: 'CP-violating phase in the PMNS matrix',
    unit: 'degrees',
    pmPath: 'pmns_matrix.delta_CP',
    experimental: {
      value: 230,
      error: 36,
      source: 'NuFIT 6.0 (2025)'
    },
    category: 'pmns',
    derivation: 'From complex structure moduli phases'
  },

  // ═══════════════════════════════════════════════════════════════════
  // DARK ENERGY
  // ═══════════════════════════════════════════════════════════════════
  w0: {
    symbol: 'w₀',
    htmlSymbol: 'w<sub>0</sub>',
    name: 'Dark Energy Equation of State',
    description: 'Present-day equation of state parameter for dark energy (w = P/ρ)',
    unit: '',
    pmPath: 'dark_energy.w0_PM',
    experimental: {
      value: -0.827,
      error: 0.063,
      source: 'DESI DR2 (2024)'
    },
    category: 'cosmology',
    derivation: 'w₀ = -1 + 2/(3d_eff) where d_eff = 12 + (α₄+α₅)/2'
  },

  wa: {
    symbol: 'w_a',
    htmlSymbol: 'w<sub>a</sub>',
    name: 'Dark Energy Evolution',
    description: 'Time derivative of dark energy equation of state in w(a) = w₀ + wₐ(1-a)',
    unit: '',
    pmPath: 'dark_energy.wa_PM',
    experimental: {
      value: -0.75,
      error: 0.25,
      source: 'DESI DR2 (2024)'
    },
    category: 'cosmology',
    derivation: 'Derived from moduli rolling in Kähler potential'
  },

  // ═══════════════════════════════════════════════════════════════════
  // GUT PARAMETERS
  // ═══════════════════════════════════════════════════════════════════
  M_GUT: {
    symbol: 'M_GUT',
    htmlSymbol: 'M<sub>GUT</sub>',
    name: 'Grand Unification Scale',
    description: 'Energy scale where gauge couplings unify in SO(10)',
    unit: 'GeV',
    pmPath: 'proton_decay.M_GUT',
    experimental: {
      value: 2e16,
      error: 1e16,
      source: 'Theoretical expectation'
    },
    category: 'gut',
    derivation: 'Set by G2 manifold volume and string scale'
  },

  alpha_GUT_inv: {
    symbol: '1/α_GUT',
    htmlSymbol: '1/α<sub>GUT</sub>',
    name: 'Inverse GUT Coupling',
    description: 'Inverse of the unified gauge coupling at GUT scale',
    unit: '',
    pmPath: 'proton_decay.alpha_GUT_inv',
    experimental: {
      value: 24.3,
      error: 0.3,
      source: 'RG evolution from SM couplings'
    },
    category: 'gut',
    derivation: '1/(10π) = 24.30... from geometric considerations'
  },

  tau_p: {
    symbol: 'τ_p',
    htmlSymbol: 'τ<sub>p</sub>',
    name: 'Proton Lifetime',
    description: 'Predicted lifetime before proton decay via X/Y boson exchange',
    unit: 'years',
    pmPath: 'proton_decay.tau_p_median',
    experimental: {
      value: 1.67e34,
      error: 0,
      source: 'Super-K lower bound (2023)'
    },
    category: 'predictions',
    derivation: 'τ_p ∝ M_GUT⁴/m_p⁵ from dimension-6 operators'
  },

  // ═══════════════════════════════════════════════════════════════════
  // DIMENSIONS & TOPOLOGY
  // ═══════════════════════════════════════════════════════════════════
  D_bulk: {
    symbol: 'D',
    htmlSymbol: 'D',
    name: 'Bulk Spacetime Dimension',
    description: 'Total dimensionality of the two-time bulk spacetime',
    unit: '',
    pmPath: 'dimensions.D_bulk',
    experimental: null,
    category: 'dimensions',
    derivation: 'Critical dimension for bosonic string: 24+2 = 26'
  },

  D_after_sp2r: {
    symbol: 'D_13',
    htmlSymbol: 'D<sub>13</sub>',
    name: 'Dimension After Sp(2,R)',
    description: 'Effective dimension after Sp(2,R) gauge fixing removes one time',
    unit: '',
    pmPath: 'dimensions.D_after_sp2r',
    experimental: null,
    category: 'dimensions',
    derivation: '26 - 13 (Sp(2,R) removes half the dimensions)'
  },

  chi_eff: {
    symbol: 'χ',
    htmlSymbol: 'χ',
    name: 'Euler Characteristic',
    description: 'Euler characteristic of the TCS G2 manifold',
    unit: '',
    pmPath: 'topology.chi_eff',
    experimental: null,
    category: 'topology',
    derivation: 'χ = 144 for TCS G2 with b₂=4, b₃=24'
  },

  b3: {
    symbol: 'b₃',
    htmlSymbol: 'b<sub>3</sub>',
    name: 'Third Betti Number',
    description: 'Number of independent 3-cycles in the G2 manifold',
    unit: '',
    pmPath: 'topology.b3',
    experimental: null,
    category: 'topology',
    derivation: 'b₃ = 24 determines associative 3-cycle count'
  },

  n_gen: {
    symbol: 'n_gen',
    htmlSymbol: 'n<sub>gen</sub>',
    name: 'Number of Generations',
    description: 'Number of fermion generations (families) in the Standard Model',
    unit: '',
    pmPath: 'topology.n_gen',
    experimental: {
      value: 3,
      error: 0,
      source: 'Observed'
    },
    category: 'topology',
    derivation: 'n_gen = χ/24/2 = 144/24/2 = 3'
  },

  // ═══════════════════════════════════════════════════════════════════
  // KK STATES
  // ═══════════════════════════════════════════════════════════════════
  m_KK: {
    symbol: 'm_KK',
    htmlSymbol: 'm<sub>KK</sub>',
    name: 'KK Graviton Mass',
    description: 'Mass of first Kaluza-Klein graviton excitation',
    unit: 'TeV',
    pmPath: 'kk_graviton.mass_TeV',
    experimental: null,
    category: 'predictions',
    derivation: 'Set by compactification radius: m_KK ~ 1/R'
  },

  // ═══════════════════════════════════════════════════════════════════
  // QUARK MASSES
  // ═══════════════════════════════════════════════════════════════════
  m_t: {
    symbol: 'm_t',
    htmlSymbol: 'm<sub>t</sub>',
    name: 'Top Quark Mass',
    description: 'Pole mass of the top quark',
    unit: 'GeV',
    pmPath: 'v10_2_all_fermions.quarks.t.mass_GeV',
    experimental: {
      value: 172.69,
      error: 0.30,
      source: 'PDG 2024'
    },
    category: 'masses',
    derivation: 'Yukawa from moduli-matter coupling'
  },

  m_b: {
    symbol: 'm_b',
    htmlSymbol: 'm<sub>b</sub>',
    name: 'Bottom Quark Mass',
    description: 'Running mass of the bottom quark at m_b scale',
    unit: 'GeV',
    pmPath: 'v10_2_all_fermions.quarks.b.mass_GeV',
    experimental: {
      value: 4.18,
      error: 0.03,
      source: 'PDG 2024'
    },
    category: 'masses',
    derivation: 'Yukawa hierarchy from moduli ratios'
  },

  // ═══════════════════════════════════════════════════════════════════
  // LEPTON MASSES
  // ═══════════════════════════════════════════════════════════════════
  m_tau: {
    symbol: 'm_τ',
    htmlSymbol: 'm<sub>τ</sub>',
    name: 'Tau Lepton Mass',
    description: 'Mass of the tau lepton',
    unit: 'MeV',
    pmPath: 'v10_2_all_fermions.leptons.tau.mass_MeV',
    experimental: {
      value: 1776.86,
      error: 0.12,
      source: 'PDG 2024'
    },
    category: 'masses',
    derivation: 'Yukawa from Kähler moduli structure'
  },

  // ═══════════════════════════════════════════════════════════════════
  // GAUGE BOSONS
  // ═══════════════════════════════════════════════════════════════════
  m_Z: {
    symbol: 'm_Z',
    htmlSymbol: 'm<sub>Z</sub>',
    name: 'Z Boson Mass',
    description: 'Mass of the neutral weak boson',
    unit: 'GeV',
    pmPath: 'gauge_bosons.Z.mass_GeV',
    experimental: {
      value: 91.1876,
      error: 0.0021,
      source: 'PDG 2024'
    },
    category: 'masses',
    derivation: 'm_Z = v/2 × sqrt(g² + g\'²)'
  },

  m_W: {
    symbol: 'm_W',
    htmlSymbol: 'm<sub>W</sub>',
    name: 'W Boson Mass',
    description: 'Mass of the charged weak bosons',
    unit: 'GeV',
    pmPath: 'gauge_bosons.W.mass_GeV',
    experimental: {
      value: 80.377,
      error: 0.012,
      source: 'PDG 2024'
    },
    category: 'masses',
    derivation: 'm_W = v/2 × g'
  }
};

/**
 * Upload tooltip database to Firebase
 */
async function uploadTooltipDatabase() {
  console.log('Uploading Tooltip Database to Firebase');
  console.log('─'.repeat(70));

  const batch = db.batch();
  let count = 0;

  for (const [id, data] of Object.entries(TOOLTIP_DATABASE)) {
    const docRef = db.collection('formula_database').doc(id);
    batch.set(docRef, {
      ...data,
      id,
      uploadedAt: new Date().toISOString()
    });
    count++;
    console.log(`  Added: ${id} (${data.name})`);
  }

  await batch.commit();
  console.log(`\n✓ Uploaded ${count} tooltip entries to Firebase`);

  return count;
}

/**
 * Main execution
 */
async function main() {
  try {
    const count = await uploadTooltipDatabase();

    console.log('\n' + '─'.repeat(70));
    console.log('Tooltip Database Upload Complete');
    console.log(`Total entries: ${count}`);

    // Verify upload
    const snapshot = await db.collection('formula_database').get();
    console.log(`\nVerification: ${snapshot.size} documents in formula_database collection`);

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
