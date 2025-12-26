#!/usr/bin/env python3
"""
Fix MathJax configuration in principia-metaphysica-paper.html
to prevent "Math input error" from pm-value spans in code blocks.
"""

import re

# Read the HTML file
with open('principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace the MathJax configuration
old_config = r"options: \{\s+skipHtmlTags: \['script', 'noscript', 'style', 'textarea', 'pre'\]\s+\}"

new_config = """options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
                skipHtmlClasses: 'pm-value|pm-loaded|pm-loading|pm-error|mathjax-ignore',
                ignoreHtmlClass: 'mathjax-ignore'
            },
            startup: {
                // Wait for PM constants to load before initial typeset
                ready: () => {
                    MathJax.startup.defaultReady();
                    if (window.PM && window.PM._loaded) {
                        console.log('MathJax: PM already loaded, proceeding with typeset');
                    } else {
                        console.log('MathJax: Waiting for PM constants to load...');
                    }
                }
            }"""

# Replace
html_new = re.sub(old_config, new_config, html)

if html_new != html:
    # Write back
    with open('principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
        f.write(html_new)
    print("DONE: Fixed MathJax configuration")
    print("   - Added 'code' to skipHtmlTags")
    print("   - Added skipHtmlClasses to ignore pm-value elements")
    print("   - Added startup.ready() to coordinate with PM loader")
else:
    print("ERROR: Failed to find pattern to replace")
    print("   Looking for:", old_config[:50])
