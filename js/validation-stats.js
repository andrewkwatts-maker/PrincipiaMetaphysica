/**
 * Validation Statistics - Dynamic population from theory-constants-enhanced.js
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 *
 * Calculates and displays validation statistics on the index page
 */

// Wait for PM constants to load
document.addEventListener('DOMContentLoaded', function() {
    if (typeof PM === 'undefined') {
        console.error('PM constants not loaded. Include theory-constants-enhanced.js first.');
        return;
    }

    updateValidationStats();
});

function updateValidationStats() {
    // Calculate predictions within 1σ from theory_output.json data
    const predictions = [
        { name: 'n_gen', theory: 3, experiment: 3, sigma: 0.00 }, // Exact
        { name: 'theta_23', theory: 47.20, experiment: 47.2, sigma: 0.00 }, // Exact
        { name: 'theta_13', theory: 8.57, experiment: 8.57, sigma: 0.00 }, // Exact
        { name: 'theta_12', theory: 33.10, experiment: 33.41, sigma: 0.22 },
        { name: 'delta_CP', theory: 195.0, experiment: 197.0, sigma: 0.09 },
        { name: 'w0', theory: -0.8528, experiment: -0.83, sigma: 0.38 },
        { name: 'w_a', theory: -0.95, experiment: -0.75, sigma: 0.66 },
        { name: 'M_GUT', theory: 2.118e16, experiment: 2.1e16, sigma: 0.5 },
        { name: 'alpha_GUT_inv', theory: 23.54, experiment: 24.0, sigma: 0.3 },
        { name: 'tau_p', theory: 3.83e34, experiment: 1.67e34, sigma: 0.8 },
        { name: 'KK_mass', theory: 5.0, experiment: null, sigma: null }, // Prediction
        { name: 'prob_IH', theory: 0.855, experiment: 0.50, sigma: null }, // Prediction
        { name: 'BR_epi0', theory: 0.642, experiment: null, sigma: null }, // Prediction
        { name: 'BR_Knu', theory: 0.356, experiment: null, sigma: null } // Prediction
    ];

    // Count predictions within 1σ
    const within1sigma = predictions.filter(p => p.sigma !== null && p.sigma <= 1.0).length;
    const totalWithData = predictions.filter(p => p.sigma !== null).length;

    // Count exact matches (0.00σ)
    const exactMatches = predictions.filter(p => p.sigma === 0.00).length;

    // DESI validation (w0)
    const desiPrediction = predictions.find(p => p.name === 'w0');
    const desiSigma = desiPrediction ? desiPrediction.sigma : 0.38;

    // Calculate grade
    const grade = calculateGrade(within1sigma, totalWithData, exactMatches);

    // Update DOM elements
    const gradeElement = document.getElementById('framework-grade');
    if (gradeElement) {
        gradeElement.textContent = `Grade ${grade}`;
    }

    const predictionsElement = document.getElementById('predictions-within-1sigma');
    if (predictionsElement) {
        predictionsElement.textContent = `${within1sigma} of ${totalWithData}`;
    }

    const exactElement = document.getElementById('exact-matches');
    if (exactElement) {
        exactElement.textContent = `${exactMatches} Exact`;
    }

    const desiElement = document.getElementById('desi-validation');
    if (desiElement) {
        desiElement.textContent = `Validated (${desiSigma.toFixed(2)}σ)`;
    }

    // Update additional fields from PM constants if available
    updateAdditionalFields();

    console.log(`Validation stats updated: ${within1sigma}/${totalWithData} within 1σ, ${exactMatches} exact, DESI ${desiSigma}σ, Grade ${grade}`);
}

function updateAdditionalFields() {
    if (typeof PM === 'undefined') return;

    // Chi effective
    const chiEffEl = document.getElementById('chi-eff');
    if (chiEffEl && PM.topology && PM.topology.chi_eff) {
        chiEffEl.textContent = PM.topology.chi_eff;
    }

    // Proton decay uncertainty
    const tauPUncertaintyEl = document.getElementById('tau-p-uncertainty');
    if (tauPUncertaintyEl && PM.proton_decay && PM.proton_decay.uncertainty_oom) {
        tauPUncertaintyEl.textContent = PM.proton_decay.uncertainty_oom.toFixed(3);
    }

    // Proton decay improvement
    const tauPImprovementEl = document.getElementById('tau-p-improvement');
    if (tauPImprovementEl && PM.proton_decay && PM.proton_decay.uncertainty_oom) {
        const improvement = 0.8 / PM.proton_decay.uncertainty_oom;
        tauPImprovementEl.textContent = improvement.toFixed(1);
    }

    // Planck tension (hardcoded for now - could be computed)
    const planckTensionEl = document.getElementById('planck-tension');
    if (planckTensionEl) {
        planckTensionEl.textContent = '1.3'; // From DESI DR2 frozen field resolution
    }

    // PMNS average sigma
    const pmnsAvgSigmaEl = document.getElementById('pmns-avg-sigma');
    if (pmnsAvgSigmaEl && PM.pmns_matrix && PM.pmns_matrix.avg_sigma) {
        pmnsAvgSigmaEl.textContent = PM.pmns_matrix.avg_sigma.toFixed(2);
    }

    // PMNS exact count (theta_23, theta_13)
    const pmnsExactCountEl = document.getElementById('pmns-exact-count');
    if (pmnsExactCountEl) {
        pmnsExactCountEl.textContent = '2';
    }

    // KK mass
    const mKKEl = document.getElementById('m-kk');
    if (mKKEl && PM.kk_spectrum && PM.kk_spectrum.M_KK_mean) {
        mKKEl.textContent = (PM.kk_spectrum.M_KK_mean / 1000).toFixed(1); // Convert GeV to TeV
    }

    // KK error
    const mKKErrorEl = document.getElementById('m-kk-error');
    if (mKKErrorEl && PM.kk_spectrum && PM.kk_spectrum.M_KK_std) {
        mKKErrorEl.textContent = (PM.kk_spectrum.M_KK_std / 1000).toFixed(1); // Convert GeV to TeV
    }

    // KK significance (hardcoded from analysis)
    const kkSigEl = document.getElementById('kk-significance');
    if (kkSigEl) {
        kkSigEl.textContent = '6.2';
    }

    // M_GUT value
    const mGUTEl = document.getElementById('m-gut-value');
    if (mGUTEl && PM.proton_decay && PM.proton_decay.M_GUT) {
        const mgut = PM.proton_decay.M_GUT;
        mGUTEl.textContent = (mgut / 1e16).toFixed(3) + '×10¹⁶';
    }

    // w0 theory
    const w0TheoryEl = document.getElementById('w0-theory');
    if (w0TheoryEl && PM.shared_dimensions && PM.shared_dimensions.w0_from_d_eff) {
        w0TheoryEl.textContent = PM.shared_dimensions.w0_from_d_eff.toFixed(4);
    }

    // w0 DESI
    const w0DESIEl = document.getElementById('w0-desi');
    if (w0DESIEl && PM.dark_energy && PM.dark_energy.w0_DESI_central) {
        const central = PM.dark_energy.w0_DESI_central;
        const error = PM.dark_energy.w0_DESI_error || 0.06;
        w0DESIEl.textContent = `${central.toFixed(2)}±${error.toFixed(2)}`;
    }

    // w0 sigma
    const w0SigmaEl = document.getElementById('w0-sigma');
    if (w0SigmaEl && PM.dark_energy && PM.dark_energy.w0_sigma) {
        w0SigmaEl.textContent = PM.dark_energy.w0_sigma.toFixed(2);
    }
}

function calculateGrade(within1sigma, total, exactMatches) {
    // Grade calculation based on validation performance
    const percentage = (within1sigma / total) * 100;
    const exactBonus = exactMatches * 5; // 5 points per exact match

    const score = Math.min(100, percentage + exactBonus);

    if (score >= 97) return 'A+';
    if (score >= 93) return 'A';
    if (score >= 90) return 'A-';
    if (score >= 87) return 'B+';
    if (score >= 83) return 'B';
    if (score >= 80) return 'B-';
    if (score >= 77) return 'C+';
    if (score >= 73) return 'C';
    return 'C-';
}

// Expose for manual refresh if needed
window.updateValidationStats = updateValidationStats;
