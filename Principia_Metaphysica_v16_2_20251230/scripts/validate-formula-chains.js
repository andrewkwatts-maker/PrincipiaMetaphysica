#!/usr/bin/env node
/**
 * Formula Derivation Chain Validator
 * ===================================
 *
 * Validates that all PM formulas have complete derivation chains
 * linking back to established physics.
 *
 * Usage:
 *   node scripts/validate-formula-chains.js
 *
 * Output:
 *   - Console report of validation results
 *   - JSON report file in reports/formula-chain-validation.json
 *
 * Exit codes:
 *   0 - All chains valid
 *   1 - Some chains invalid
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');

// Load the formula registry using require
const registryPath = path.join(__dirname, '..', 'js', 'formula-registry.js');
const { FORMULA_REGISTRY } = require(registryPath);

// ================================================================
// VALIDATION FUNCTIONS
// ================================================================

/**
 * Find a formula by ID across all categories
 */
function findFormula(id) {
    for (const category of ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS']) {
        for (const key of Object.keys(FORMULA_REGISTRY[category] || {})) {
            if (FORMULA_REGISTRY[category][key].id === id) {
                return {
                    formula: FORMULA_REGISTRY[category][key],
                    category: category
                };
            }
        }
    }
    return null;
}

/**
 * Trace derivation chain from a formula to established physics
 */
function traceDerivationChain(formulaId, visited = new Set()) {
    const result = findFormula(formulaId);

    if (!result) {
        return {
            valid: false,
            error: `Formula not found: ${formulaId}`,
            chain: [],
            depth: 0
        };
    }

    const { formula, category } = result;

    // ESTABLISHED formulas are the root - chain is complete
    if (category === 'ESTABLISHED') {
        return {
            valid: true,
            chain: [{ id: formulaId, category: 'ESTABLISHED', label: formula.label }],
            establishedRoot: formulaId,
            depth: 0
        };
    }

    // Check for circular references
    if (visited.has(formulaId)) {
        return {
            valid: false,
            error: `Circular reference detected: ${formulaId}`,
            chain: [],
            depth: 0
        };
    }
    visited.add(formulaId);

    // Formula must have derivation field
    if (!formula.derivation) {
        return {
            valid: false,
            error: `No derivation defined for: ${formulaId}`,
            chain: [{ id: formulaId, category, label: formula.label }],
            depth: 0
        };
    }

    const chain = [{ id: formulaId, category, label: formula.label }];
    const establishedRoots = [];
    let maxDepth = 0;

    // Check established physics references
    if (formula.derivation.establishedPhysics && formula.derivation.establishedPhysics.length > 0) {
        for (const estId of formula.derivation.establishedPhysics) {
            const estResult = findFormula(estId);
            if (!estResult) {
                return {
                    valid: false,
                    error: `Established physics not found: ${estId}`,
                    chain,
                    depth: 1
                };
            }
            if (estResult.category !== 'ESTABLISHED') {
                return {
                    valid: false,
                    error: `${estId} is not in ESTABLISHED category`,
                    chain,
                    depth: 1
                };
            }
            establishedRoots.push(estId);
            chain.push({ id: estId, category: 'ESTABLISHED', label: estResult.formula.label });
        }
    }

    // Check parent formulas
    if (formula.derivation.parentFormulas && formula.derivation.parentFormulas.length > 0) {
        for (const parentId of formula.derivation.parentFormulas) {
            const parentChain = traceDerivationChain(parentId, new Set(visited));
            if (!parentChain.valid) {
                return {
                    valid: false,
                    error: `Parent chain invalid: ${parentChain.error}`,
                    chain: chain.concat(parentChain.chain),
                    depth: parentChain.depth + 1
                };
            }
            chain.push(...parentChain.chain);
            if (parentChain.establishedRoot) {
                establishedRoots.push(parentChain.establishedRoot);
            }
            maxDepth = Math.max(maxDepth, parentChain.depth + 1);
        }
    }

    // Must have at least one path to established physics
    if (establishedRoots.length === 0) {
        return {
            valid: false,
            error: `No path to established physics for: ${formulaId}`,
            chain,
            depth: maxDepth
        };
    }

    return {
        valid: true,
        chain,
        establishedRoots,
        depth: maxDepth
    };
}

/**
 * Validate all derivation chains
 */
function validateAllChains() {
    const report = {
        timestamp: new Date().toISOString(),
        version: FORMULA_REGISTRY._meta?.version || 'unknown',
        summary: {
            valid: true,
            totalFormulas: 0,
            validChains: 0,
            invalidChains: 0,
            maxDepth: 0
        },
        byCategory: {},
        issues: [],
        chains: []
    };

    // Process ESTABLISHED (no validation needed)
    const establishedCount = Object.keys(FORMULA_REGISTRY.ESTABLISHED || {}).length;
    report.byCategory.ESTABLISHED = {
        count: establishedCount,
        note: 'Foundation formulas - no derivation needed',
        formulas: Object.values(FORMULA_REGISTRY.ESTABLISHED || {}).map(f => ({
            id: f.id,
            label: f.label,
            attribution: f.attribution
        }))
    };
    report.summary.totalFormulas += establishedCount;

    // Process derived categories
    for (const category of ['THEORY', 'DERIVED', 'PREDICTIONS']) {
        report.byCategory[category] = {
            valid: 0,
            invalid: 0,
            formulas: []
        };

        for (const key of Object.keys(FORMULA_REGISTRY[category] || {})) {
            const formula = FORMULA_REGISTRY[category][key];
            report.summary.totalFormulas++;

            const chainResult = traceDerivationChain(formula.id);

            const formulaReport = {
                id: formula.id,
                label: formula.label,
                valid: chainResult.valid,
                depth: chainResult.depth,
                establishedRoots: chainResult.establishedRoots || [],
                error: chainResult.error || null
            };

            report.byCategory[category].formulas.push(formulaReport);

            if (chainResult.valid) {
                report.summary.validChains++;
                report.byCategory[category].valid++;
                report.summary.maxDepth = Math.max(report.summary.maxDepth, chainResult.depth);

                report.chains.push({
                    formulaId: formula.id,
                    category,
                    chain: chainResult.chain.map(c => c.id),
                    establishedRoots: chainResult.establishedRoots,
                    depth: chainResult.depth
                });
            } else {
                report.summary.valid = false;
                report.summary.invalidChains++;
                report.byCategory[category].invalid++;
                report.issues.push({
                    formulaId: formula.id,
                    category,
                    label: formula.label,
                    error: chainResult.error
                });
            }
        }
    }

    return report;
}

/**
 * Print report to console
 */
function printReport(report) {
    console.log('\n' + '='.repeat(70));
    console.log('FORMULA DERIVATION CHAIN VALIDATION REPORT');
    console.log('='.repeat(70));
    console.log(`Timestamp: ${report.timestamp}`);
    console.log(`Version: ${report.version}`);
    console.log('-'.repeat(70));

    console.log('\nSUMMARY:');
    console.log(`  Total formulas: ${report.summary.totalFormulas}`);
    console.log(`  Valid chains: ${report.summary.validChains}`);
    console.log(`  Invalid chains: ${report.summary.invalidChains}`);
    console.log(`  Max chain depth: ${report.summary.maxDepth}`);
    console.log(`  Overall: ${report.summary.valid ? '✓ PASS' : '✗ FAIL'}`);

    console.log('\n' + '-'.repeat(70));
    console.log('BY CATEGORY:');

    // ESTABLISHED
    const est = report.byCategory.ESTABLISHED;
    console.log(`\n  ESTABLISHED (${est.count} formulas) - ${est.note}`);
    for (const f of est.formulas.slice(0, 5)) {
        console.log(`    • ${f.id}: ${f.label} ${f.attribution}`);
    }
    if (est.formulas.length > 5) {
        console.log(`    ... and ${est.formulas.length - 5} more`);
    }

    // Other categories
    for (const category of ['THEORY', 'DERIVED', 'PREDICTIONS']) {
        const cat = report.byCategory[category];
        const status = cat.invalid === 0 ? '✓' : '✗';
        console.log(`\n  ${category} (${cat.valid} valid, ${cat.invalid} invalid) ${status}`);

        for (const f of cat.formulas) {
            const icon = f.valid ? '✓' : '✗';
            console.log(`    ${icon} ${f.id}: ${f.label}`);
            if (f.valid) {
                console.log(`      → Roots: [${f.establishedRoots.join(', ')}] (depth: ${f.depth})`);
            } else {
                console.log(`      → ERROR: ${f.error}`);
            }
        }
    }

    if (report.issues.length > 0) {
        console.log('\n' + '-'.repeat(70));
        console.log('ISSUES TO FIX:');
        for (const issue of report.issues) {
            console.log(`\n  ✗ ${issue.formulaId} [${issue.category}]`);
            console.log(`    Label: ${issue.label}`);
            console.log(`    Error: ${issue.error}`);
        }
    }

    console.log('\n' + '='.repeat(70));
}

/**
 * Save report to JSON file
 */
function saveReport(report) {
    const reportsDir = path.join(__dirname, '..', 'reports');
    if (!fs.existsSync(reportsDir)) {
        fs.mkdirSync(reportsDir, { recursive: true });
    }

    const reportPath = path.join(reportsDir, 'formula-chain-validation.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`\nReport saved to: ${reportPath}`);
}

// ================================================================
// MAIN
// ================================================================

function main() {
    console.log('Loading formula registry...');

    // Validate
    const report = validateAllChains();

    // Print to console
    printReport(report);

    // Save to file
    saveReport(report);

    // Exit with appropriate code
    process.exit(report.summary.valid ? 0 : 1);
}

main();
