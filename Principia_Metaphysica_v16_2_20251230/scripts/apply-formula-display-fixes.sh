#!/bin/bash
#
# Apply Formula Display Fixes
# ============================
#
# This script applies the necessary changes to update formula display
# styling to match the old paper (principia-metaphysica-paper.html)
#
# Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

set -e  # Exit on error

echo "================================================"
echo "Formula Display Styling Fix - Patch Application"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Backup directory
BACKUP_DIR="backups/formula-display-fix-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo -e "${YELLOW}Step 1: Creating backups...${NC}"
cp formulas.html "$BACKUP_DIR/"
cp js/pm-formula-loader.js "$BACKUP_DIR/"
cp js/pm-formula-component.js "$BACKUP_DIR/"
echo -e "${GREEN}✓ Backups created in $BACKUP_DIR${NC}"
echo ""

echo -e "${YELLOW}Step 2: Adding CSS link to formulas.html...${NC}"
# Check if the CSS link already exists
if grep -q "formula-display-fix.css" formulas.html; then
    echo -e "${YELLOW}  CSS link already exists, skipping...${NC}"
else
    # Add the CSS link after styles.css
    sed -i 's|<link rel="stylesheet" href="css/styles.css">|<link rel="stylesheet" href="css/styles.css">\n    <link rel="stylesheet" href="css/formula-display-fix.css">|' formulas.html
    echo -e "${GREEN}✓ Added formula-display-fix.css link${NC}"
fi
echo ""

echo -e "${YELLOW}Step 3: Manual steps required...${NC}"
echo ""
echo "The following changes need to be made manually:"
echo ""
echo "1. ${YELLOW}formulas.html${NC} - Update renderFormulaCard() function (around line 1007):"
echo "   Replace:"
echo "     <!-- Equation -->"
echo "     <div class=\"formula-equation\">"
echo "         \${formula.latex ? \`\$\$\${formula.latex}\$\$\` : (formula.html || escapeHtml(formula.plainText || 'No equation available'))}"
echo "     </div>"
echo ""
echo "   With:"
echo "     <!-- Equation -->"
echo "     <div class=\"formula-equation\">"
echo "         \${formula.section ? \`<span class=\"equation-number\">(\${escapeHtml(formula.section)})</span>\` : ''}"
echo "         \${formula.latex ? \`\$\$\${formula.latex}\$\$\` : (formula.html || escapeHtml(formula.plainText || 'No equation available'))}"
echo "     </div>"
echo ""
echo "2. ${YELLOW}js/pm-formula-loader.js${NC} - Update render() function (around line 360):"
echo "   Replace:"
echo "     html += \`<div class=\"formula-display\" style=\"font-size: 1.2rem; padding: 0.5rem 0; text-align: center;\">"
echo "         \${formula.html || formula.latex || formula.plainText || ''}"
echo "     </div>\`;"
echo ""
echo "   With:"
echo "     const equationNumber = formula.section ? \`(\${formula.section})\` : '';"
echo "     html += \`<div class=\"formula-display\" style=\"font-size: 1.2rem; padding: 0.5rem 0; text-align: center; position: relative; clear: both;\">"
echo "         \${equationNumber ? \`<span class=\"equation-number\">\${equationNumber}</span>\` : ''}"
echo "         \${formula.html || formula.latex || formula.plainText || ''}"
echo "     </div>\`;"
echo ""
echo "3. ${YELLOW}js/pm-formula-component.js${NC} - Add equation-number style (around line 259):"
echo "   Add after .formula-display style:"
echo "     .equation-number {"
echo "         float: right;"
echo "         color: #666;"
echo "         font-size: 0.9rem;"
echo "         font-family: 'Crimson Text', Georgia, serif;"
echo "         margin-left: 1rem;"
echo "         line-height: 2;"
echo "     }"
echo ""
echo "4. ${YELLOW}Test the changes:${NC}"
echo "   - Open formulas.html in a browser"
echo "   - Verify equation numbers appear on the right"
echo "   - Check that formulas have clean backgrounds"
echo "   - Confirm derivation boxes use light gradients"
echo ""
echo "5. ${YELLOW}View the comparison:${NC}"
echo "   - Open examples/formula-styling-comparison.html"
echo "   - Compare old paper, current, and fixed styles"
echo ""

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Automatic steps completed!${NC}"
echo -e "${GREEN}Please complete the manual steps above.${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""
echo "To rollback if needed:"
echo "  cp $BACKUP_DIR/* ."
echo ""
