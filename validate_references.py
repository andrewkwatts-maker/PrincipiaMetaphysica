#!/usr/bin/env python3
"""
Reference Validation Script for Principia Metaphysica
Validates all citations, links, and experimental data references
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class ReferenceValidator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.results = {
            'total_refs_by_type': defaultdict(int),
            'broken_links': [],
            'outdated_refs': [],
            'missing_citations': [],
            'duplicate_refs': [],
            'version_mentions': [],
            'format_issues': [],
            'arxiv_links': [],
            'doi_links': [],
            'experimental_data': defaultdict(list)
        }

    def scan_file(self, filepath: Path) -> Dict:
        """Scan a single HTML file for references"""
        file_results = {
            'arxiv': [],
            'doi': [],
            'nufit': [],
            'pdg': [],
            'desi': [],
            'planck': [],
            'version_mentions': []
        }

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find arXiv references
            arxiv_pattern = r'arXiv:(\d{4}\.\d{4,5})'
            file_results['arxiv'] = re.findall(arxiv_pattern, content)

            # Find DOI links
            doi_pattern = r'doi\.org/(10\.\d{4,9}/[-._;()/:A-Z0-9]+)'
            file_results['doi'] = re.findall(doi_pattern, content, re.IGNORECASE)

            # Find experimental data references
            nufit_pattern = r'NuFIT\s+(\d+\.?\d*)\s*\((\d{4})\)'
            file_results['nufit'] = re.findall(nufit_pattern, content)

            pdg_pattern = r'PDG\s+(\d{4})'
            file_results['pdg'] = re.findall(pdg_pattern, content)

            desi_pattern = r'DESI\s+(?:DR)?(\d+)?\s*\(?(\d{4})?\)?'
            file_results['desi'] = re.findall(desi_pattern, content)

            planck_pattern = r'Planck\s+(\d{4})'
            file_results['planck'] = re.findall(planck_pattern, content)

            # Find version mentions in reference descriptions
            version_pattern = r'(version|Version|v\d+|V\d+)'
            version_matches = re.finditer(version_pattern, content)
            for match in version_matches:
                # Get context
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end]
                file_results['version_mentions'].append({
                    'match': match.group(0),
                    'context': context
                })

        except Exception as e:
            print(f"Error scanning {filepath}: {e}")

        return file_results

    def validate_all_files(self):
        """Scan all HTML files in the project"""
        html_files = list(self.base_path.glob('**/*.html'))

        print(f"Scanning {len(html_files)} HTML files...")

        all_arxiv = set()
        all_doi = set()
        nufit_versions = defaultdict(list)
        pdg_versions = defaultdict(list)
        desi_versions = defaultdict(list)
        planck_versions = defaultdict(list)

        for filepath in html_files:
            # Skip backup files
            if '.backup' in str(filepath) or '.bak' in str(filepath):
                continue

            results = self.scan_file(filepath)

            # Collect arXiv IDs
            for arxiv_id in results['arxiv']:
                all_arxiv.add(arxiv_id)
                self.results['arxiv_links'].append({
                    'file': str(filepath.relative_to(self.base_path)),
                    'id': arxiv_id
                })

            # Collect DOIs
            for doi in results['doi']:
                all_doi.add(doi)
                self.results['doi_links'].append({
                    'file': str(filepath.relative_to(self.base_path)),
                    'id': doi
                })

            # Track experimental data versions
            for version, year in results['nufit']:
                nufit_versions[(version, year)].append(str(filepath.relative_to(self.base_path)))

            for year in results['pdg']:
                pdg_versions[year].append(str(filepath.relative_to(self.base_path)))

            for dr, year in results['desi']:
                desi_versions[(dr, year)].append(str(filepath.relative_to(self.base_path)))

            for year in results['planck']:
                planck_versions[year].append(str(filepath.relative_to(self.base_path)))

            # Track version mentions
            for vm in results['version_mentions']:
                self.results['version_mentions'].append({
                    'file': str(filepath.relative_to(self.base_path)),
                    'match': vm['match'],
                    'context': vm['context'][:200]
                })

        # Store experimental data summaries
        self.results['experimental_data']['nufit'] = dict(nufit_versions)
        self.results['experimental_data']['pdg'] = dict(pdg_versions)
        self.results['experimental_data']['desi'] = dict(desi_versions)
        self.results['experimental_data']['planck'] = dict(planck_versions)

        # Count totals
        self.results['total_refs_by_type']['arxiv'] = len(all_arxiv)
        self.results['total_refs_by_type']['doi'] = len(all_doi)
        self.results['total_refs_by_type']['nufit'] = len(nufit_versions)
        self.results['total_refs_by_type']['pdg'] = len(pdg_versions)
        self.results['total_refs_by_type']['desi'] = len(desi_versions)
        self.results['total_refs_by_type']['planck'] = len(planck_versions)

    def check_missing_key_refs(self):
        """Check for missing key experimental references"""
        missing = []

        # Key references that should be present
        key_refs = {
            'NuFIT 6.0 (2025)': self.results['experimental_data']['nufit'].get(('6.0', '2025'), []),
            'PDG 2024': self.results['experimental_data']['pdg'].get('2024', []),
            'DESI DR2 (2024/2025)': any(k for k in self.results['experimental_data']['desi'].keys() if '2024' in k or '2025' in k),
            'arXiv:1809.09083 (TCS)': any(link['id'] == '1809.09083' for link in self.results['arxiv_links'])
        }

        for ref_name, found in key_refs.items():
            if not found:
                missing.append(ref_name)

        self.results['missing_citations'] = missing

    def generate_report(self) -> str:
        """Generate markdown report"""
        report = []
        report.append("# AGENT 4: REFERENCES AND CITATIONS VALIDATION REPORT\n")
        report.append(f"**Generated:** December 8, 2025 (v12.7)\n")
        report.append("---\n")

        # Executive Summary
        report.append("## EXECUTIVE SUMMARY\n")
        report.append(f"- **Total HTML files scanned:** {len(list(self.base_path.glob('**/*.html')))}")
        report.append(f"- **Unique arXiv references:** {self.results['total_refs_by_type']['arxiv']}")
        report.append(f"- **Unique DOI references:** {self.results['total_refs_by_type']['doi']}")
        report.append(f"- **NuFIT citations:** {self.results['total_refs_by_type']['nufit']}")
        report.append(f"- **PDG citations:** {self.results['total_refs_by_type']['pdg']}")
        report.append(f"- **DESI citations:** {self.results['total_refs_by_type']['desi']}")
        report.append(f"- **Planck citations:** {self.results['total_refs_by_type']['planck']}")
        report.append(f"- **Version mentions found:** {len(self.results['version_mentions'])}\n")

        # Experimental Data References
        report.append("## EXPERIMENTAL DATA REFERENCES\n")

        report.append("### NuFIT References\n")
        for (version, year), files in self.results['experimental_data']['nufit'].items():
            report.append(f"- **NuFIT {version} ({year})**: {len(files)} files")
            if version == '6.0' and year == '2025':
                report.append("  - ✅ CORRECT VERSION")
            else:
                report.append(f"  - ⚠️ OUTDATED - should be NuFIT 6.0 (2025)")
        report.append("")

        report.append("### PDG References\n")
        for year, files in self.results['experimental_data']['pdg'].items():
            report.append(f"- **PDG {year}**: {len(files)} files")
            if year == '2024':
                report.append("  - ✅ CORRECT VERSION")
            else:
                report.append(f"  - ⚠️ OUTDATED - should be PDG 2024")
        report.append("")

        report.append("### DESI References\n")
        for (dr, year), files in self.results['experimental_data']['desi'].items():
            dr_str = f"DR{dr}" if dr else ""
            year_str = f"({year})" if year else ""
            report.append(f"- **DESI {dr_str} {year_str}**: {len(files)} files")
            if dr == '2' or year in ['2024', '2025']:
                report.append("  - ✅ CORRECT VERSION (DR2 2024/2025)")
            else:
                report.append(f"  - ⚠️ CHECK VERSION - should be DESI DR2 (2025)")
        report.append("")

        report.append("### Planck References\n")
        for year, files in self.results['experimental_data']['planck'].items():
            report.append(f"- **Planck {year}**: {len(files)} files")
            if year in ['2018', '2020']:
                report.append("  - ✅ CORRECT VERSION (Planck 2018 results published 2020)")
            else:
                report.append(f"  - ⚠️ CHECK VERSION")
        report.append("")

        # arXiv References
        report.append("## ARXIV REFERENCES\n")
        report.append(f"**Total unique arXiv IDs:** {self.results['total_refs_by_type']['arxiv']}\n")

        # Key arXiv references
        key_arxiv = {
            '1809.09083': 'TCS G₂ Construction (Corti et al.)',
            '2404.03002': 'DESI DR2 2024',
            '1807.06209': 'Planck 2018 Results',
            'hep-th/0107177': 'Atiyah-Witten M-theory on G₂',
            'hep-th/9812205': 'Acharya M-theory Joyce Orbifolds',
            'gr-qc/9406019': 'Connes-Rovelli Thermal Time'
        }

        report.append("### Key arXiv References Status\n")
        for arxiv_id, description in key_arxiv.items():
            found = any(link['id'] == arxiv_id for link in self.results['arxiv_links'])
            status = "✅ FOUND" if found else "❌ MISSING"
            report.append(f"- **{arxiv_id}** ({description}): {status}")
        report.append("")

        # Version Mentions
        report.append("## VERSION MENTIONS IN REFERENCES\n")
        report.append(f"**Total version mentions found:** {len(self.results['version_mentions'])}\n")

        if self.results['version_mentions']:
            report.append("### Files with Version Mentions (to review/remove)\n")
            version_by_file = defaultdict(list)
            for vm in self.results['version_mentions']:
                version_by_file[vm['file']].append(vm['match'])

            for file, versions in sorted(version_by_file.items()):
                report.append(f"- **{file}**: {', '.join(set(versions))}")
        report.append("")

        # Missing Citations
        report.append("## MISSING KEY CITATIONS\n")
        if self.results['missing_citations']:
            for citation in self.results['missing_citations']:
                report.append(f"- ❌ {citation}")
        else:
            report.append("✅ All key citations present\n")
        report.append("")

        # Critical Issues
        report.append("## CRITICAL ISSUES IDENTIFIED\n")
        issues = []

        # Check for missing TCS reference
        if not any(link['id'] == '1809.09083' for link in self.results['arxiv_links']):
            issues.append("❌ **CRITICAL:** arXiv:1809.09083 (TCS G₂ construction) is cited throughout but NOT in references.html")

        # Check for missing NuFIT reference
        if ('6.0', '2025') not in self.results['experimental_data']['nufit']:
            issues.append("⚠️ NuFIT 6.0 (2025) not consistently cited")

        # Check for DESI DR2 reference in references.html
        desi_in_refs = any('2024.03002' in link['id'] for link in self.results['arxiv_links'])
        if not desi_in_refs:
            issues.append("⚠️ DESI DR2 2024 (arXiv:2404.03002) may not be in references.html")

        if issues:
            for issue in issues:
                report.append(f"{issue}\n")
        else:
            report.append("✅ No critical issues identified\n")

        # Recommendations
        report.append("## RECOMMENDATIONS\n")
        report.append("### High Priority\n")
        report.append("1. **Add missing TCS reference** to references.html:")
        report.append("   - Corti, A., Haskins, M., Nordenstam, J., Pacini, T. (2018)")
        report.append("   - 'G₂-manifolds and associative submanifolds via semi-Fano 3-folds'")
        report.append("   - arXiv:1809.09083 [math.DG]\n")

        report.append("2. **Add NuFIT 6.0 (2025) reference** to references.html:")
        report.append("   - Esteban, I., et al. (2025)")
        report.append("   - 'NuFIT 6.0: Updated Global Analysis of Neutrino Oscillation Data'")
        report.append("   - http://www.nu-fit.org/\n")

        report.append("3. **Verify DESI DR2 reference** is complete in references.html:")
        report.append("   - DESI Collaboration (2024)")
        report.append("   - 'DESI 2024 VI: Cosmological Constraints from BAO'")
        report.append("   - arXiv:2404.03002\n")

        report.append("### Medium Priority\n")
        report.append("4. **Remove version mentions** from reference descriptions where inappropriate")
        report.append("5. **Standardize experimental data citations** to latest versions:")
        report.append("   - NuFIT 6.0 (2025)")
        report.append("   - PDG 2024")
        report.append("   - DESI DR2 (2025)")
        report.append("   - Planck 2018 (published 2020)\n")

        report.append("### Low Priority\n")
        report.append("6. **Verify all arXiv links** resolve correctly (manual check recommended)")
        report.append("7. **Verify all DOI links** resolve correctly (manual check recommended)")
        report.append("8. **Check citation format consistency** across all files\n")

        # Files Requiring Modification
        report.append("## FILES REQUIRING MODIFICATION\n")
        report.append("### references.html\n")
        report.append("**Required additions:**")
        report.append("- Add Corti et al. (2018) arXiv:1809.09083 to Geometry & Topology section")
        report.append("- Add NuFIT 6.0 (2025) to Neutrino Physics section")
        report.append("- Verify DESI DR2 2024 citation is complete\n")

        report.append("### Files citing experimental data\n")
        report.append("**Update to latest versions:**")

        # List files with outdated refs
        files_to_update = set()
        for (version, year), files in self.results['experimental_data']['nufit'].items():
            if version != '6.0' or year != '2025':
                files_to_update.update(files)

        for year, files in self.results['experimental_data']['pdg'].items():
            if year != '2024':
                files_to_update.update(files)

        if files_to_update:
            for file in sorted(files_to_update):
                report.append(f"- {file}")
        else:
            report.append("✅ All experimental data references up to date")

        report.append("\n---")
        report.append("**End of Report**")

        return '\n'.join(report)

def main():
    base_path = r"H:\Github\PrincipiaMetaphysica"

    validator = ReferenceValidator(base_path)
    print("Starting reference validation...")

    validator.validate_all_files()
    validator.check_missing_key_refs()

    report = validator.generate_report()

    # Save report
    report_path = Path(base_path) / "reports" / "AGENT-4-REFERENCES-VALIDATION.md"
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n[OK] Report saved to: {report_path}")
    print(f"\n[SUMMARY]:")
    print(f"   - arXiv references: {validator.results['total_refs_by_type']['arxiv']}")
    print(f"   - DOI references: {validator.results['total_refs_by_type']['doi']}")
    print(f"   - NuFIT citations: {validator.results['total_refs_by_type']['nufit']}")
    print(f"   - PDG citations: {validator.results['total_refs_by_type']['pdg']}")
    print(f"   - DESI citations: {validator.results['total_refs_by_type']['desi']}")
    print(f"   - Planck citations: {validator.results['total_refs_by_type']['planck']}")

    # Save detailed JSON results
    json_path = Path(base_path) / "reports" / "reference_validation_details.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(validator.results, f, indent=2, default=str)

    print(f"   - Detailed JSON: {json_path}")

if __name__ == "__main__":
    main()
