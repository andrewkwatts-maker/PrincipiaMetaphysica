"""
Update all files to remove "peer review" claims and replace with "pending peer review"
Also update acknowledgments with user's specific requested text.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import os

def update_peer_review_language():
    """Remove claims of being 'ready for peer review' and replace with 'pending peer review'"""

    replacements = [
        # beginners-guide.html
        (
            "h:/Github/PrincipiaMetaphysica/beginners-guide.html",
            [
                (r'is ready for peer review with concrete testable predictions\.',
                 'presents a complete theoretical framework pending peer review, with concrete testable predictions.'),
                (r'<strong>Ready for peer review:</strong>',
                 '<strong>Pending peer review:</strong>'),
            ]
        ),
    ]

    changes_made = []

    for filepath, patterns in replacements:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            for old_pattern, new_text in patterns:
                content = re.sub(old_pattern, new_text, content, flags=re.IGNORECASE)

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                changes_made.append(filepath)
                print(f"OK: Updated {filepath}")

    return changes_made

def update_acknowledgments():
    """Update acknowledgments with user's specific requested text"""

    filepath = "h:/Github/PrincipiaMetaphysica/references.html"

    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Tim Ward & Shane Sutton
    old_tim_shane = r'Special thanks to <strong style="color: var\(--text-primary\);">Tim Ward</strong> and <strong style="color: var\(--text-primary\);">Shane Sutton</strong>, whose Bible studies, theological insights, and spiritual mentorship invested deeply in my spiritual growth\. Your patient guidance and thought-provoking discussions taught me to think deeply about fundamental questions—skills that proved invaluable in this work\.'

    new_tim_shane = '''Special thanks to <strong style="color: var(--text-primary);">Tim Ward</strong> and <strong style="color: var(--text-primary);">Shane Sutton</strong>, whose Bible studies helped grow my understanding beyond religion to a grounded and rigorous belief in Jesus Christ alone. Tim for presenting the universal salvation of mankind, and Shane for presenting the path laid out by Christ in the Beatitudes on the Sermon on the Mount—forming me from a religious person to a believer in Christ alone.'''

    content = re.sub(old_tim_shane, new_tim_shane, content)

    # Replace Derek Bradley with Andrew Pahuru
    old_derek = r'<li><strong style="color: var\(--text-primary\);">Derek Bradley</strong> \(Aurora44\) – for insights into cutting-edge engineering and innovation</li>'

    new_andrew = '''<li><strong style="color: var(--text-primary);">Andrew Pahuru</strong> – for giving me a first chance in software engineering</li>'''

    content = re.sub(old_derek, new_andrew, content)

    # Update Jacob Sainty
    old_jacob = r'<li><strong style="color: var\(--text-primary\);">Jacob Sainty</strong> \(Boeing\) – for believing in my abilities and providing opportunities to excel in aerospace engineering</li>'

    new_jacob = '''<li><strong style="color: var(--text-primary);">Jacob Sainty</strong> (Boeing) – for believing in my abilities and growing my potential and understanding of software development</li>'''

    content = re.sub(old_jacob, new_jacob, content)

    # Update Jared Leendertz
    old_jared = r'<li><strong style="color: var\(--text-primary\);">Jared Leendertz</strong> – for technical insights and collaborative problem-solving</li>'

    new_jared = '''<li><strong style="color: var(--text-primary);">Jared Leendertz</strong> – for technical insights into rapid problem solving in the software space</li>'''

    content = re.sub(old_jared, new_jared, content)

    # Update Mathew Alexander
    old_mathew = r'<li><strong style="color: var\(--text-primary\);">Mathew Alexander</strong> – for professional mentorship and opportunities to grow</li>'

    new_mathew = '''<li><strong style="color: var(--text-primary);">Mathew Alexander</strong> – for presenting insights into hidden variables interpretation of quantum physics</li>'''

    content = re.sub(old_mathew, new_mathew, content)

    # Update Nathaniel du Preez-Wilkinson
    old_nathaniel = r'<li><strong style="color: var\(--text-primary\);">Nathaniel du Preez-Wilkinson</strong> – for collaborative excellence and unique perspectives</li>'

    new_nathaniel = '''<li><strong style="color: var(--text-primary);">Nathaniel du Preez-Wilkinson</strong> – for exemplifying rigor and process, believing in me when the chips were down</li>'''

    content = re.sub(old_nathaniel, new_nathaniel, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"OK: Updated acknowledgments in {filepath}")
    return filepath

if __name__ == "__main__":
    print("Updating 'peer review' language...")
    peer_review_changes = update_peer_review_language()

    print("\nUpdating acknowledgments...")
    ack_change = update_acknowledgments()

    print("\n=== SUMMARY ===")
    print(f"Peer review language updated in {len(peer_review_changes)} file(s)")
    print(f"Acknowledgments updated: {'Yes' if ack_change else 'No'}")
    print("\nAll updates complete.")
