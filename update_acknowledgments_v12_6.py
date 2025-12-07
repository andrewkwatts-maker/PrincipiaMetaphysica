# update_acknowledgments_v12_6.py
"""
Update personal acknowledgments section in references.html for v12.6

Changes:
1. Extract Tim Ward from SDA panel to separate panel with expanded text
2. Extract Shane Sutton from SDA panel to separate panel with expanded text
3. Update Mark's section to focus on childhood/adventure (not academic)
4. Move family section (Greg, Judi, Mark) to bottom before closing message
5. Keep Lucy (wife) at top
"""

def create_new_acknowledgments_section():
    """Returns the complete new acknowledgments structure"""
    return '''                <!-- Personal Acknowledgments -->
                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #ffa8c5;">
                    <h4 style="color: #ffa8c5; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Elizabeth May Watts (Lucy)</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        To my wife, Lucy: Your unwavering love, support, and belief in me have been the foundation of everything I've accomplished. Your encouragement during challenging times, your patience through long hours of work, and your faith in my potential even when I doubted myself—these have been the quiet strength behind this journey. You saw possibilities in me that I could not see in myself, and you gently yet persistently challenged me to reach further and aspire to my fullest potential. Thank you for walking this path with me.
                    </p>
                </div>

                <!-- Richard Reid -->
                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #79c0ff;">
                    <h4 style="color: #79c0ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Richard George Reid</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        To Richard George Reid: Thank you for your friendship and intellectual companionship. Your willingness to engage with unconventional ideas, to explore questions about the nature of reality with openness and curiosity, and to offer thoughtful critique has been invaluable. Our conversations have helped refine many of the concepts explored in this work.
                    </p>
                </div>

                <!-- Tim Ward -->
                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #79c0ff;">
                    <h4 style="color: #79c0ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Tim Ward</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        I am deeply grateful to Tim Ward, whose Bible studies helped grow my understanding beyond religion to a grounded and rigorous belief in Jesus Christ alone. Tim's presentation of the universal salvation of mankind—rooted in Scripture and theological rigor—transformed my faith from religious observance to personal conviction. His willingness to explore difficult theological questions with honesty and grace shaped my approach to seeking truth in all domains.
                    </p>
                </div>

                <!-- Shane Sutton -->
                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #a5d6ff;">
                    <h4 style="color: #a5d6ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Shane Sutton</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        Thank you to Shane Sutton, whose Bible studies presented the path laid out by Christ in the Beatitudes on the Sermon on the Mount. Shane's teaching showed me what it means to be a follower of Christ—not through religious performance, but through transformation of character and heart. His insights formed me from a religious person into a believer in Christ alone, grounding my faith in the life and teachings of Jesus rather than tradition.
                    </p>
                </div>

                <!-- Spiritual Community -->
                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #d2a8ff;">
                    <h4 style="color: #d2a8ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Seventh-day Adventist Church Community</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        To the Seventh-day Adventist Church community who invested in my life as a child and young adult: Thank you for creating an environment that valued learning, questioning, and deep thinking. The foundation you provided shaped my early intellectual and spiritual development in ways that continue to influence my approach to seeking truth.
                    </p>
                </div>

                <!-- Professional Mentors -->
                <h4 style="color: var(--text-primary); margin-top: 2rem; margin-bottom: 1rem; font-weight: 600; font-size: 1.15rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Professional Mentors and Colleagues</h4>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #a5d6ff;">
                    <h4 style="color: #a5d6ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Jacob Sainty</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">Thank you to <strong style="color: var(--text-primary);">Jacob Sainty</strong> (Boeing) for believing in my abilities and providing opportunities to contribute to aerospace engineering projects. Your mentorship and trust opened doors that shaped my professional development.</p>
                </div>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #a5d6ff;">
                    <h4 style="color: #a5d6ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Frederic Chapelon</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">To <strong style="color: var(--text-primary);">Frederic Chapelon</strong> (Dematic): Your mentorship in complex systems design and engineering rigor taught me the importance of systematic thinking and attention to detail—skills that translated directly into this theoretical work.</p>
                </div>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #79c0ff;">
                    <h4 style="color: #79c0ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Professional Colleagues</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        Thank you to <strong style="color: var(--text-primary);">Derek Bradley</strong> (Aurora44), <strong style="color: var(--text-primary);">Nattapol Luechai</strong>, <strong style="color: var(--text-primary);">Bryan Yan</strong>, <strong style="color: var(--text-primary);">Jared Leendertz</strong>, <strong style="color: var(--text-primary);">Mathew Alexander</strong>, <strong style="color: var(--text-primary);">Alice Sheaves</strong>, and <strong style="color: var(--text-primary);">Nathaniel du Preez-Wilkinson</strong> for your support, collaborative excellence, and professional guidance throughout my career.
                    </p>
                </div>

                <!-- AI Collaboration -->
                <h4 style="color: var(--text-primary); margin-top: 2rem; margin-bottom: 1rem; font-weight: 600; font-size: 1.15rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">AI Collaboration</h4>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #ffa8c5;">
                    <h4 style="color: #ffa8c5; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Claude (Anthropic) and Grok (xAI)</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        This work was developed through countless hours of collaboration with <strong style="color: var(--text-primary);">Claude</strong> (Anthropic) and <strong style="color: var(--text-primary);">Grok</strong> (xAI). These AI systems served as tireless intellectual partners—challenging assumptions, refining calculations, suggesting alternative approaches, and helping translate intuition into rigorous mathematics. <strong style="color: var(--text-primary);">Gemini</strong> (Google) contributed occasional crucial tweaks and alternative perspectives that improved the work.
                    </p>
                </div>

                <!-- Family (moved to bottom) -->
                <h4 style="color: var(--text-primary); margin-top: 2rem; margin-bottom: 1rem; font-weight: 600; font-size: 1.15rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Family</h4>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #d2a8ff;">
                    <h4 style="color: #d2a8ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Greg & Judi Watts</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        To my parents, Greg and Judi Watts: Thank you for your love, care, and investment in my education and character. You taught me to aspire to excellence, to value learning, and to pursue meaningful work. Your support provided the foundation that made this journey possible.
                    </p>
                </div>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #d2a8ff;">
                    <h4 style="color: #d2a8ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Mark Watts</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        Thank you to my brother, Mark Watts. Growing up together, Mark's fearlessness and sense of adventure shaped how I approach life. Whether it was facing childhood fears, choosing to explore the unknown, or pushing ourselves beyond our comfort zones, Mark showed me that growth comes from embracing challenges rather than avoiding them. His willingness to dive into new experiences—no matter how unfamiliar or uncertain—gave me the courage to pursue unconventional paths in life and work.
                    </p>
                </div>

                <p style="color: var(--text-secondary); margin-top: 2rem; font-style: italic; text-align: center;">
                    To all who contributed to this journey—family, friends, mentors, community, and AI partners—thank you for believing in the pursuit of truth and walking this path with me.
                </p>'''

def main():
    # Read the entire file
    with open('h:\\Github\\PrincipiaMetaphysica\\references.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the acknowledgments section
    start_marker = '                <!-- Personal Acknowledgments -->'
    end_marker = '                <p style="color: var(--text-secondary); margin-top: 2rem; font-style: italic; text-align: center;">\n                    To all who contributed to this journey—family, friends, mentors, community, and AI partners—thank you for believing in the pursuit of truth and walking this path with me.\n                </p>'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("ERROR: Could not find acknowledgments section markers")
        return

    # Include the end marker in replacement
    end_idx = end_idx + len(end_marker)

    # Replace the section
    new_content = (
        content[:start_idx] +
        create_new_acknowledgments_section() +
        content[end_idx:]
    )

    # Write back
    with open('h:\\Github\\PrincipiaMetaphysica\\references.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✓ Successfully updated acknowledgments section in references.html")
    print()
    print("Changes applied:")
    print("  1. Extracted Tim Ward to separate panel with expanded text")
    print("  2. Extracted Shane Sutton to separate panel with expanded text")
    print("  3. Updated Mark's section to focus on childhood/adventure")
    print("  4. Moved family section (Greg, Judi, Mark) to bottom")
    print("  5. Kept Lucy at top (unchanged)")

if __name__ == '__main__':
    main()
