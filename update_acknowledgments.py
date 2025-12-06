#!/usr/bin/env python3
"""
Update references.html with comprehensive acknowledgments.
"""

import re

# Read the file
with open('references.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new acknowledgments section
new_acknowledgments = '''        <!-- Personal Acknowledgments -->
        <section class="ref-category" id="acknowledgments" style="margin-top: 3rem; background: linear-gradient(135deg, rgba(139, 127, 255, 0.08), rgba(255, 126, 182, 0.05)); border: 1px solid rgba(139, 127, 255, 0.2);">
            <h3 style="color: #8b7fff; border-bottom-color: rgba(139, 127, 255, 0.3);">Personal Acknowledgments</h3>

            <div style="color: var(--text-secondary); line-height: 1.9; font-size: 1rem;">
                <p style="margin-bottom: 1.5rem; font-style: italic; color: var(--text-primary);">
                    This work would not have been possible without the support of remarkable individuals who believed in exploring the deepest questions about reality.
                </p>

                <!-- Family -->
                <h4 style="color: #8b7fff; margin: 2rem 0 1rem 0; font-size: 1.15rem; font-weight: 600;">Family</h4>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #ff7eb6;">
                    <h4 style="color: #ff7eb6; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Elizabeth May Watts (Lucy)</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        Most importantly, I thank my wife, Elizabeth May Watts (Lucy), for her unwavering love, support, and belief in me throughout this journey. Lucy's encouragement during the challenging times, her faith in my potential when I doubted myself, and her gentle yet persistent challenges to reach further and aspire to my fullest potential have been the foundation upon which this work was built. She saw possibilities in me that I could not see in myself. Her love, patience, and belief made it possible to pursue what seemed impossible. This work exists because she believed it could—and believed in me to create it.
                    </p>
                </div>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #79c0ff;">
                    <h4 style="color: #79c0ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Greg & Judi Watts</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        To my parents, Greg and Judi Watts: thank you for your love and care in raising me, for the countless hours you invested in my growth, and for teaching me to aspire and pursue excellence in all I do. You trained me up in the way I should go, and those foundations have carried me further than you could have imagined. This work is a reflection of the values you instilled.
                    </p>
                </div>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #a371f7;">
                    <h4 style="color: #a371f7; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">My Brother</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        To my brother: thank you for your support in my younger years, for challenging me to face my fears head-on, and for encouraging me to give things a go and push myself beyond my perceived limits. Those early lessons in courage and persistence shaped who I became.
                    </p>
                </div>

                <!-- Friends & Mentors -->
                <h4 style="color: #8b7fff; margin: 2rem 0 1rem 0; font-size: 1.15rem; font-weight: 600;">Friends & Intellectual Companionship</h4>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #8b7fff;">
                    <h4 style="color: #8b7fff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Richard George Reid</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        I am deeply grateful to Richard George Reid, whose friendship and intellectual companionship over the years provided invaluable perspective. Richard's willingness to engage with unconventional ideas, his thoughtful critique, and his unique insights helped sanity-test and refine many of the concepts about the nature of reality that ultimately shaped this framework. His support in exploring what conventional wisdom often dismissed has been an irreplaceable gift to this work.
                    </p>
                </div>

                <!-- Spiritual Community -->
                <h4 style="color: #8b7fff; margin: 2rem 0 1rem 0; font-size: 1.15rem; font-weight: 600;">Spiritual Community</h4>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #56d364;">
                    <h4 style="color: #56d364; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Seventh-day Adventist Church Community</h4>
                    <p style="margin-bottom: 0.75rem; color: var(--text-secondary);">
                        To the wider Seventh-day Adventist church community: thank you for your investment in my life as a child and young adult. The time, energy, and resources you dedicated to my development shaped my character and worldview in profound ways. I am grateful for your commitment to nurturing young minds and spirits.
                    </p>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        Special thanks to <strong style="color: var(--text-primary);">Tim Ward</strong> and <strong style="color: var(--text-primary);">Shane Sutton</strong>, whose Bible studies, theological insights, and spiritual mentorship invested deeply in my spiritual growth. Your patient guidance and thought-provoking discussions taught me to think deeply about fundamental questions—skills that proved invaluable in this work.
                    </p>
                </div>

                <!-- Professional Mentors -->
                <h4 style="color: #8b7fff; margin: 2rem 0 1rem 0; font-size: 1.15rem; font-weight: 600;">Professional Mentors & Colleagues</h4>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #ffa657;">
                    <h4 style="color: #ffa657; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Professional Development</h4>
                    <p style="margin-bottom: 0.75rem; color: var(--text-secondary);">
                        I am deeply grateful to those who invested in my professional growth, believed in my potential, and provided unique opportunities and insights that allowed me to develop my craft over the years:
                    </p>
                    <ul style="margin: 0.75rem 0 0 1.5rem; color: var(--text-secondary); line-height: 1.8;">
                        <li><strong style="color: var(--text-primary);">Jacob Sainty</strong> (Boeing) – for believing in my abilities and providing opportunities to excel in aerospace engineering</li>
                        <li><strong style="color: var(--text-primary);">Frederic Chapelon</strong> (Dematic) – for mentorship in complex systems design and engineering rigor</li>
                        <li><strong style="color: var(--text-primary);">Derek Bradley</strong> (Aurora44) – for insights into cutting-edge engineering and innovation</li>
                        <li><strong style="color: var(--text-primary);">Nattapol Luechai</strong> – for collaborative excellence and technical expertise</li>
                        <li><strong style="color: var(--text-primary);">Bryan Yan</strong> – for support and professional guidance</li>
                        <li><strong style="color: var(--text-primary);">Jared Leendertz</strong> – for technical insights and collaborative problem-solving</li>
                        <li><strong style="color: var(--text-primary);">Mathew Alexander</strong> – for professional mentorship and opportunities to grow</li>
                        <li><strong style="color: var(--text-primary);">Alice Sheaves</strong> – for encouragement and belief in my potential</li>
                        <li><strong style="color: var(--text-primary);">Nathaniel du Preez-Wilkinson</strong> – for collaborative excellence and unique perspectives</li>
                    </ul>
                    <p style="margin-top: 0.75rem; margin-bottom: 0; color: var(--text-secondary);">
                        Each of you contributed to the skills, discipline, and confidence that made this theoretical work possible. The analytical rigor, problem-solving approaches, and persistence I learned through our collaborations proved essential to this framework.
                    </p>
                </div>

                <!-- AI Tools -->
                <h4 style="color: #8b7fff; margin: 2rem 0 1rem 0; font-size: 1.15rem; font-weight: 600;">AI Collaboration</h4>

                <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #d2a8ff;">
                    <h4 style="color: #d2a8ff; margin-top: 0; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem;">Claude, Grok, and Gemini</h4>
                    <p style="margin-bottom: 0; color: var(--text-secondary);">
                        Special acknowledgment to the AI systems that served as intellectual sparring partners throughout this work: <strong style="color: var(--text-primary);">Claude</strong> (Anthropic) and <strong style="color: var(--text-primary);">Grok</strong> (xAI) for countless hours wrestling with complex concepts, challenging assumptions, and helping refine the mathematical framework—your tireless engagement pushed this work to levels of rigor I could not have achieved alone. Thank you to <strong style="color: var(--text-primary);">Gemini</strong> (Google) for providing the occasional crucial tweak and alternative perspective that unlocked new pathways forward. This collaboration between human creativity and AI capability represents a new frontier in theoretical physics research.
                    </p>
                </div>

                <p style="margin-top: 2rem; margin-bottom: 0; text-align: center; font-style: italic; color: var(--text-muted); font-size: 0.95rem;">
                    To all who contributed to this journey—family, friends, mentors, community, and AI partners—<br>
                    thank you for believing in the pursuit of truth and walking this path with me.
                </p>
            </div>
        </section>'''

# Find and replace the acknowledgments section
pattern = r'(<!-- Personal Acknowledgments -->.*?</section>)'
content = re.sub(pattern, new_acknowledgments, content, flags=re.DOTALL)

# Write back
with open('references.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Comprehensive acknowledgments added to references.html")
print("Added sections for:")
print("  - Family (Lucy, Greg & Judi Watts, Brother)")
print("  - Richard George Reid")
print("  - SDA Church Community (Tim Ward, Shane Sutton)")
print("  - Professional Mentors (9 colleagues)")
print("  - AI Collaboration (Claude, Grok, Gemini)")
