/**
 * LaTeX Paper Generator
 *
 * Generates a complete LaTeX document from Firebase Firestore data.
 * All content is loaded from the centralized database.
 *
 * Usage: node scripts/generate-latex-paper.js [--output paper.tex]
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const OUTPUT_FILE = process.argv.find(a => a.startsWith('--output='))?.split('=')[1] || 'principia-metaphysica.tex';

// Initialize Firebase
function initFirebase() {
  const possiblePaths = [
    path.join(__dirname, 'serviceAccountKey.json'),
    path.join(__dirname, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json'),
    path.join(ROOT_DIR, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json')
  ];

  let serviceAccountPath = null;
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      serviceAccountPath = p;
      break;
    }
  }

  if (!serviceAccountPath) {
    console.error('ERROR: Service account key not found');
    process.exit(1);
  }

  const serviceAccount = require(serviceAccountPath);
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: "principia-metaphysica"
  });

  return admin.firestore();
}

/**
 * Load all data from Firebase
 */
async function loadAllData(db) {
  console.log('Loading data from Firebase...');

  const [formulasSnap, theoryDoc, expDoc, constantsSnap] = await Promise.all([
    db.collection('formulas').get(),
    db.collection('theory_constants').doc('current').get(),
    db.collection('experimental_data').doc('current').get(),
    db.collection('constants').get()
  ]);

  const formulas = {};
  formulasSnap.forEach(doc => {
    formulas[doc.id] = doc.data();
  });

  const constants = {};
  constantsSnap.forEach(doc => {
    constants[doc.id] = doc.data();
  });

  return {
    formulas,
    theoryConstants: theoryDoc.data(),
    experimentalData: expDoc.data(),
    constants
  };
}

/**
 * Convert HTML formula to LaTeX
 */
function htmlToLatex(html) {
  if (!html) return '';

  let latex = html;

  // Subscripts and superscripts
  latex = latex.replace(/<sub>/g, '_{');
  latex = latex.replace(/<\/sub>/g, '}');
  latex = latex.replace(/<sup>/g, '^{');
  latex = latex.replace(/<\/sup>/g, '}');

  // Greek letters
  const greekMap = {
    'α': '\\alpha', 'β': '\\beta', 'γ': '\\gamma', 'δ': '\\delta',
    'ε': '\\epsilon', 'ζ': '\\zeta', 'η': '\\eta', 'θ': '\\theta',
    'ι': '\\iota', 'κ': '\\kappa', 'λ': '\\lambda', 'μ': '\\mu',
    'ν': '\\nu', 'ξ': '\\xi', 'π': '\\pi', 'ρ': '\\rho',
    'σ': '\\sigma', 'τ': '\\tau', 'υ': '\\upsilon', 'φ': '\\phi',
    'χ': '\\chi', 'ψ': '\\psi', 'ω': '\\omega',
    'Γ': '\\Gamma', 'Δ': '\\Delta', 'Θ': '\\Theta', 'Λ': '\\Lambda',
    'Ξ': '\\Xi', 'Π': '\\Pi', 'Σ': '\\Sigma', 'Φ': '\\Phi',
    'Ψ': '\\Psi', 'Ω': '\\Omega'
  };

  for (const [char, replacement] of Object.entries(greekMap)) {
    latex = latex.replace(new RegExp(char, 'g'), replacement + ' ');
  }

  // Math symbols
  latex = latex.replace(/×/g, '\\times ');
  latex = latex.replace(/±/g, '\\pm ');
  latex = latex.replace(/≈/g, '\\approx ');
  latex = latex.replace(/≠/g, '\\neq ');
  latex = latex.replace(/≤/g, '\\leq ');
  latex = latex.replace(/≥/g, '\\geq ');
  latex = latex.replace(/∫/g, '\\int ');
  latex = latex.replace(/∑/g, '\\sum ');
  latex = latex.replace(/∏/g, '\\prod ');
  latex = latex.replace(/√/g, '\\sqrt');
  latex = latex.replace(/∂/g, '\\partial ');
  latex = latex.replace(/∇/g, '\\nabla ');
  latex = latex.replace(/∞/g, '\\infty ');
  latex = latex.replace(/→/g, '\\rightarrow ');
  latex = latex.replace(/←/g, '\\leftarrow ');
  latex = latex.replace(/↔/g, '\\leftrightarrow ');

  // Clean up HTML entities
  latex = latex.replace(/&nbsp;/g, ' ');
  latex = latex.replace(/&lt;/g, '<');
  latex = latex.replace(/&gt;/g, '>');
  latex = latex.replace(/&amp;/g, '\\&');

  return latex;
}

/**
 * Format a number for LaTeX
 */
function formatNumber(value, precision = 4) {
  if (typeof value !== 'number') return String(value);

  if (Math.abs(value) > 1e4 || (Math.abs(value) < 1e-4 && value !== 0)) {
    const exp = Math.floor(Math.log10(Math.abs(value)));
    const mantissa = value / Math.pow(10, exp);
    return `${mantissa.toFixed(precision)} \\times 10^{${exp}}`;
  }

  return value.toFixed(precision);
}

/**
 * Generate the LaTeX preamble
 */
function generatePreamble(data) {
  const version = data.theoryConstants.meta?.version || '12.7';

  return `% Principia Metaphysica - Complete Paper
% Version ${version}
% Generated from Firebase Firestore on ${new Date().toISOString()}
% Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

\\documentclass[12pt,a4paper]{article}

% Packages
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath,amssymb,amsthm}
\\usepackage{physics}
\\usepackage{graphicx}
\\usepackage{hyperref}
\\usepackage{booktabs}
\\usepackage{longtable}
\\usepackage{geometry}
\\usepackage{fancyhdr}
\\usepackage{xcolor}

% Page geometry
\\geometry{margin=1in}

% Header/footer
\\pagestyle{fancy}
\\fancyhf{}
\\rhead{Principia Metaphysica v${version}}
\\lhead{\\leftmark}
\\cfoot{\\thepage}

% Custom commands
\\newcommand{\\PM}{\\textsc{PM}}
\\newcommand{\\GUT}{\\mathrm{GUT}}
\\newcommand{\\SO}[1]{\\mathrm{SO}(#1)}
\\newcommand{\\SU}[1]{\\mathrm{SU}(#1)}
\\newcommand{\\GeV}{\\,\\mathrm{GeV}}
\\newcommand{\\TeV}{\\,\\mathrm{TeV}}

% Title
\\title{\\textbf{Principia Metaphysica}\\\\[0.5em]
  \\large Philosophiae Metaphysicae Principia Mathematica\\\\[1em]
  \\normalsize A Unified Geometric Framework for Deriving\\\\
  All Standard Model Parameters from First Principles}

\\author{Andrew Keith Watts\\\\
  \\small\\textit{Copyright \\textcopyright\\ 2025-2026. All rights reserved.}}

\\date{Version ${version} -- \\today}

\\begin{document}

\\maketitle

\\begin{abstract}
We present a unified geometric framework that derives all 58 Standard Model parameters
from a single \\(G_2\\) manifold compactification of 26-dimensional spacetime.
The framework employs a two-time \\(\\mathrm{Sp}(2,\\mathbb{R})\\) gauge symmetry that
eliminates ghost modes while preserving predictive power.

Key results: ${data.theoryConstants.validation?.predictions_within_1sigma || 45} of ${data.theoryConstants.validation?.total_predictions || 48}
predictions agree with experiment within \\(1\\sigma\\), with ${data.theoryConstants.validation?.exact_matches || 4}
exact central value matches. The framework predicts:
\\begin{itemize}
  \\item Dark energy equation of state \\(w_0 = ${formatNumber(data.theoryConstants.dark_energy?.w0_PM || -0.8528)}\\)
    (DESI DR2: \\(-0.83 \\pm 0.06\\), ${formatNumber(Math.abs(data.theoryConstants.dark_energy?.w0_deviation_sigma || 0.38), 2)}\\sigma)
  \\item GUT scale \\(M_{\\GUT} = ${formatNumber(data.theoryConstants.proton_decay?.M_GUT || 2.118e16)}\\GeV\\)
  \\item Proton lifetime \\(\\tau_p = ${formatNumber(data.theoryConstants.proton_decay?.tau_p_median || 3.87e34)}\\) years
  \\item Three generations from topology: \\(n_{\\mathrm{gen}} = \\chi_{\\mathrm{eff}}/48 = ${data.theoryConstants.topology?.n_gen || 3}\\)
\\end{itemize}

The framework is falsifiable: JUNO (2027) tests neutrino mass hierarchy,
HL-LHC (2029+) tests KK graviton predictions.
\\end{abstract}

\\tableofcontents
\\newpage

`;
}

/**
 * Generate the established physics section
 */
function generateEstablishedSection(data) {
  const established = Object.values(data.formulas).filter(f => f.category === 'ESTABLISHED');

  let latex = `\\section{Established Physics Foundation}

The Principia Metaphysica framework is built upon well-established physics,
extending rather than replacing the Standard Model and General Relativity.

\\subsection{General Relativity}

`;

  // Add GR formulas
  const grFormulas = established.filter(f =>
    f.id?.includes('einstein') || f.id?.includes('friedmann') || f.id?.includes('ricci')
  );

  for (const formula of grFormulas) {
    const latexFormula = formula.latex || htmlToLatex(formula.html);
    latex += `\\paragraph{${formula.label || formula.id}}
${formula.description || ''}

\\begin{equation}
  ${latexFormula}
\\end{equation}

`;
  }

  latex += `\\subsection{Quantum Field Theory}

`;

  // Add QFT formulas
  const qftFormulas = established.filter(f =>
    f.id?.includes('dirac') || f.id?.includes('yang-mills') || f.id?.includes('qcd')
  );

  for (const formula of qftFormulas) {
    const latexFormula = formula.latex || htmlToLatex(formula.html);
    latex += `\\paragraph{${formula.label || formula.id}}
${formula.description || ''}

\\begin{equation}
  ${latexFormula}
\\end{equation}

`;
  }

  return latex;
}

/**
 * Generate the theory formulas section
 */
function generateTheorySection(data) {
  const theory = Object.values(data.formulas).filter(f => f.category === 'THEORY');

  let latex = `\\section{Principia Metaphysica Theory}

\\subsection{26-Dimensional Framework}

The theory begins with a 26-dimensional spacetime with signature \\((24,2)\\),
incorporating two time dimensions that are gauge-fixed via \\(\\mathrm{Sp}(2,\\mathbb{R})\\) symmetry.

\\subsubsection{Dimensional Structure}
\\begin{itemize}
  \\item Total dimensions: \\(D_{\\mathrm{bulk}} = ${data.theoryConstants.dimensions?.D_bulk || 26}\\)
  \\item After Sp(2,R) gauge fixing: \\(D = ${data.theoryConstants.dimensions?.D_after_sp2r || 13}\\)
  \\item Internal dimensions: \\(D_{\\mathrm{internal}} = ${data.theoryConstants.dimensions?.D_internal || 7}\\)
  \\item Observable: \\(D_{\\mathrm{common}} = ${data.theoryConstants.dimensions?.D_common || 4}\\)
\\end{itemize}

\\subsection{Core Theory Formulas}

`;

  for (const formula of theory) {
    const latexFormula = formula.latex || htmlToLatex(formula.html);
    latex += `\\paragraph{${formula.label || formula.id}}
${formula.description || ''}

\\begin{equation}
  ${latexFormula}
\\end{equation}

`;
    if (formula.attribution) {
      latex += `\\textit{${formula.attribution}}\n\n`;
    }
  }

  return latex;
}

/**
 * Generate the derived results section
 */
function generateDerivedSection(data) {
  const derived = Object.values(data.formulas).filter(f => f.category === 'DERIVED');

  let latex = `\\section{Derived Results}

The following results are derived from the core theory without additional free parameters.

`;

  for (const formula of derived) {
    const latexFormula = formula.latex || htmlToLatex(formula.html);
    latex += `\\paragraph{${formula.label || formula.id}}
${formula.description || ''}

\\begin{equation}
  ${latexFormula}
\\end{equation}

`;
  }

  return latex;
}

/**
 * Generate the predictions section
 */
function generatePredictionsSection(data) {
  const predictions = Object.values(data.formulas).filter(f => f.category === 'PREDICTIONS');

  let latex = `\\section{Testable Predictions}

The framework makes specific, falsifiable predictions that can be tested by
current and near-future experiments.

\\subsection{Prediction Formulas}

`;

  for (const formula of predictions) {
    const latexFormula = formula.latex || htmlToLatex(formula.html);
    latex += `\\paragraph{${formula.label || formula.id}}
${formula.description || ''}

\\begin{equation}
  ${latexFormula}
\\end{equation}

`;
  }

  return latex;
}

/**
 * Generate the validation table
 */
function generateValidationTable(data) {
  const tc = data.theoryConstants;
  const exp = data.experimentalData;

  let latex = `\\section{Experimental Validation}

\\subsection{PMNS Matrix Parameters}

\\begin{table}[h]
\\centering
\\caption{PMNS Matrix Comparison with NuFIT 6.0 (2025)}
\\begin{tabular}{lccc}
\\toprule
Parameter & PM Value & NuFIT 6.0 & Deviation \\\\
\\midrule
\\(\\theta_{23}\\) & \\(${formatNumber(tc.pmns_matrix?.theta_23 || 45, 2)}^\\circ\\) & \\(${tc.pmns_nufit_comparison?.theta_23_nufit || 45}^\\circ \\pm ${tc.pmns_nufit_comparison?.theta_23_nufit_error || 1.1}^\\circ\\) & \\(${formatNumber(tc.pmns_matrix?.theta_23_sigma || 0, 2)}\\sigma\\) \\\\
\\(\\theta_{12}\\) & \\(${formatNumber(tc.pmns_matrix?.theta_12 || 33.59, 2)}^\\circ\\) & \\(${tc.pmns_nufit_comparison?.theta_12_nufit || 33.41}^\\circ \\pm ${tc.pmns_nufit_comparison?.theta_12_nufit_error || 0.75}^\\circ\\) & \\(${formatNumber(tc.pmns_matrix?.theta_12_sigma || 0.24, 2)}\\sigma\\) \\\\
\\(\\theta_{13}\\) & \\(${formatNumber(tc.pmns_matrix?.theta_13 || 8.57, 2)}^\\circ\\) & \\(${tc.pmns_nufit_comparison?.theta_13_nufit || 8.54}^\\circ \\pm ${tc.pmns_nufit_comparison?.theta_13_nufit_error || 0.12}^\\circ\\) & \\(${formatNumber(tc.pmns_matrix?.theta_13_sigma || 0.01, 2)}\\sigma\\) \\\\
\\(\\delta_{CP}\\) & \\(${formatNumber(tc.pmns_matrix?.delta_cp || 235, 0)}^\\circ\\) & \\(${tc.pmns_nufit_comparison?.delta_cp_nufit || 232}^\\circ \\pm ${tc.pmns_nufit_comparison?.delta_cp_nufit_error || 30}^\\circ\\) & \\(${formatNumber(tc.pmns_matrix?.delta_cp_sigma || 0.1, 2)}\\sigma\\) \\\\
\\bottomrule
\\end{tabular}
\\end{table}

\\subsection{Dark Energy}

\\begin{table}[h]
\\centering
\\caption{Dark Energy Comparison with DESI DR2 (2025)}
\\begin{tabular}{lccc}
\\toprule
Parameter & PM Value & DESI DR2 & Deviation \\\\
\\midrule
\\(w_0\\) & \\(${formatNumber(tc.dark_energy?.w0_PM || -0.8528, 4)}\\) & \\(-0.83 \\pm 0.06\\) & \\(${formatNumber(tc.dark_energy?.w0_deviation_sigma || 0.38, 2)}\\sigma\\) \\\\
\\(w_a\\) & \\(${formatNumber(tc.dark_energy?.wa_PM_effective || -0.95, 4)}\\) & \\(-0.75 \\pm 0.30\\) & \\(${formatNumber(tc.dark_energy?.wa_deviation_sigma || 0.66, 2)}\\sigma\\) \\\\
\\bottomrule
\\end{tabular}
\\end{table}

\\subsection{Summary Statistics}

\\begin{itemize}
  \\item Predictions within \\(1\\sigma\\): ${tc.validation?.predictions_within_1sigma || 45} of ${tc.validation?.total_predictions || 48} (${formatNumber(100 * (tc.validation?.predictions_within_1sigma || 45) / (tc.validation?.total_predictions || 48), 1)}\\%)
  \\item Exact central value matches: ${tc.validation?.exact_matches || 4}
  \\item Average deviation: \\(${formatNumber(tc.pmns_matrix?.average_sigma || 0.36, 2)}\\sigma\\)
\\end{itemize}

`;

  return latex;
}

/**
 * Generate the conclusion
 */
function generateConclusion() {
  return `\\section{Conclusion}

The Principia Metaphysica framework demonstrates that all 58 Standard Model parameters
can be derived from a single geometric structure---a \\(G_2\\) manifold compactification
of 26-dimensional spacetime with \\(\\mathrm{Sp}(2,\\mathbb{R})\\) gauge symmetry.

The framework is:
\\begin{itemize}
  \\item \\textbf{Predictive}: Only 2 fitted parameters, 56 derived from geometry
  \\item \\textbf{Falsifiable}: Specific predictions testable by JUNO (2027), HL-LHC (2029+)
  \\item \\textbf{Consistent}: All derivations trace back to established physics
\\end{itemize}

\\section*{Dedication}

\\begin{center}
Dedicated to my Dearest Wife, Elizabeth May Watts\\\\[0.5em]
\\&\\\\[0.5em]
The Ruler and Restorer of all,\\\\
The final Logos,\\\\
The Messiah,\\\\
Jesus of Nazareth
\\end{center}

\\bibliographystyle{unsrt}
\\bibliography{references}

\\end{document}
`;
}

/**
 * Main function
 */
async function main() {
  console.log('═'.repeat(70));
  console.log(' PRINCIPIA METAPHYSICA - LaTeX PAPER GENERATOR');
  console.log('═'.repeat(70));
  console.log(`Output: ${OUTPUT_FILE}\n`);

  const db = initFirebase();
  const data = await loadAllData(db);

  console.log(`Loaded: ${Object.keys(data.formulas).length} formulas`);
  console.log(`Loaded: ${Object.keys(data.constants).length} constants`);

  // Generate LaTeX document
  let latex = '';

  latex += generatePreamble(data);
  latex += generateEstablishedSection(data);
  latex += generateTheorySection(data);
  latex += generateDerivedSection(data);
  latex += generatePredictionsSection(data);
  latex += generateValidationTable(data);
  latex += generateConclusion();

  // Write to file
  const outputPath = path.join(ROOT_DIR, OUTPUT_FILE);
  fs.writeFileSync(outputPath, latex);

  console.log(`\n✓ LaTeX document generated: ${outputPath}`);
  console.log(`  Total lines: ${latex.split('\n').length}`);

  process.exit(0);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
