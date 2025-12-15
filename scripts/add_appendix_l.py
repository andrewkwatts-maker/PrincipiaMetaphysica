#!/usr/bin/env python3
"""Add Appendix L to principia-metaphysica-paper.html"""

appendix_l_content = '''
            <!-- ============================================================ -->
            <!-- APPENDIX L: COMPLETE PM VALUES TABLE -->
            <!-- ============================================================ -->
            <h2 class="section-title" id="appendix-l">Appendix L: Complete PM Values Summary</h2>

            <h3 class="subsection-title">L.1 Topological Parameters (Exact)</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Value</th>
                    <th>Formula</th>
                    <th>Status</th>
                </tr>
                <tr>
                    <td>$D_{\\text{bulk}}$</td>
                    <td>26</td>
                    <td>Virasoro: $c = D - 26 = 0$</td>
                    <td>Exact</td>
                </tr>
                <tr>
                    <td>$D_{\\text{shadow}}$</td>
                    <td>13</td>
                    <td>Sp(2,&#x211D;): $(24,2) \\to (12,1)$</td>
                    <td>Exact</td>
                </tr>
                <tr>
                    <td>$D_{G_2}$</td>
                    <td>7</td>
                    <td>G$_2$ holonomy manifold</td>
                    <td>Exact</td>
                </tr>
                <tr>
                    <td>$b_2$</td>
                    <td>4</td>
                    <td>$H^2(X,\\mathbb{Z})$ rank</td>
                    <td>Exact</td>
                </tr>
                <tr>
                    <td>$b_3$</td>
                    <td>24</td>
                    <td>Associative 3-cycles</td>
                    <td>Exact</td>
                </tr>
                <tr>
                    <td>$\\chi_{\\text{eff}}$</td>
                    <td>144</td>
                    <td>Flux-dressed Euler characteristic</td>
                    <td>Exact</td>
                </tr>
                <tr>
                    <td>$n_{\\text{gen}}$</td>
                    <td>3</td>
                    <td>$|\\chi_{\\text{eff}}|/48$</td>
                    <td>Exact</td>
                </tr>
            </table>

            <h3 class="subsection-title">L.2 Gauge Unification Parameters</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>PM Value</th>
                    <th>Experimental</th>
                    <th>Deviation</th>
                </tr>
                <tr>
                    <td>$M_{\\text{GUT}}$</td>
                    <td>$2.118 \\times 10^{16}$ GeV</td>
                    <td>$(2.0 \\pm 0.3) \\times 10^{16}$</td>
                    <td>0.39&sigma;</td>
                </tr>
                <tr>
                    <td>$1/\\alpha_{\\text{GUT}}$</td>
                    <td>23.54</td>
                    <td>$24.3 \\pm 0.5$</td>
                    <td>1.52&sigma;</td>
                </tr>
                <tr>
                    <td>$\\sin^2\\theta_W$</td>
                    <td>0.23121</td>
                    <td>$0.23122 \\pm 0.00003$</td>
                    <td>0.33&sigma;</td>
                </tr>
                <tr>
                    <td>$v_{\\text{EW}}$</td>
                    <td>173.97 GeV</td>
                    <td>174.0 GeV</td>
                    <td>0.02%</td>
                </tr>
                <tr>
                    <td>$m_h$</td>
                    <td>125.10 GeV</td>
                    <td>125.10 GeV</td>
                    <td>0.0&sigma;</td>
                </tr>
            </table>

            <h3 class="subsection-title">L.3 PMNS Matrix Parameters</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>PM Value</th>
                    <th>NuFIT 6.0</th>
                    <th>Status</th>
                </tr>
                <tr>
                    <td>$\\theta_{23}$</td>
                    <td>45.0&deg;</td>
                    <td>$45.0 \\pm 1.0$&deg;</td>
                    <td>DERIVED</td>
                </tr>
                <tr>
                    <td>$\\theta_{12}$</td>
                    <td>33.59&deg;</td>
                    <td>$33.41 \\pm 0.75$&deg;</td>
                    <td>DERIVED</td>
                </tr>
                <tr>
                    <td>$\\theta_{13}$</td>
                    <td>8.57&deg;</td>
                    <td>$8.57 \\pm 0.12$&deg;</td>
                    <td>CALIBRATED</td>
                </tr>
                <tr>
                    <td>$\\delta_{CP}$</td>
                    <td>235&deg;</td>
                    <td>$232 \\pm 30$&deg;</td>
                    <td>CALIBRATED</td>
                </tr>
            </table>

            <h3 class="subsection-title">L.4 Dark Energy Parameters</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>PM Value</th>
                    <th>DESI DR2</th>
                    <th>Deviation</th>
                </tr>
                <tr>
                    <td>$w_0$</td>
                    <td>$-0.8528$</td>
                    <td>$-0.83 \\pm 0.06$</td>
                    <td>0.38&sigma;</td>
                </tr>
                <tr>
                    <td>$w_a$</td>
                    <td>$-0.95$</td>
                    <td>$-0.75 \\pm 0.30$</td>
                    <td>0.66&sigma;</td>
                </tr>
                <tr>
                    <td>$d_{\\text{eff}}$</td>
                    <td>12.576</td>
                    <td>N/A</td>
                    <td>&mdash;</td>
                </tr>
            </table>

            <h3 class="subsection-title">L.5 Proton Decay &amp; Future Predictions</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>PM Value</th>
                    <th>Experimental</th>
                    <th>Test</th>
                </tr>
                <tr>
                    <td>$\\tau_p$</td>
                    <td>$3.91 \\times 10^{34}$ yr</td>
                    <td>$> 1.67 \\times 10^{34}$</td>
                    <td>Hyper-K</td>
                </tr>
                <tr>
                    <td>BR($e^+\\pi^0$)</td>
                    <td>0.25</td>
                    <td>Unknown</td>
                    <td>Hyper-K</td>
                </tr>
                <tr>
                    <td>$m_{\\text{KK}}$</td>
                    <td>5.0 TeV</td>
                    <td>Unknown</td>
                    <td>HL-LHC</td>
                </tr>
                <tr>
                    <td>$\\eta_{\\text{GW}}$</td>
                    <td>0.113</td>
                    <td>Unknown</td>
                    <td>LISA</td>
                </tr>
                <tr>
                    <td>Hierarchy</td>
                    <td>Normal (76%)</td>
                    <td>Unknown</td>
                    <td>JUNO</td>
                </tr>
            </table>

            <h3 class="subsection-title">L.6 Fermion Masses (Selected)</h3>
            <table>
                <tr>
                    <th>Particle</th>
                    <th>PM Value</th>
                    <th>PDG 2024</th>
                    <th>Error</th>
                </tr>
                <tr>
                    <td>$m_t$</td>
                    <td>172.7 GeV</td>
                    <td>172.69 GeV</td>
                    <td>&lt; 0.01%</td>
                </tr>
                <tr>
                    <td>$m_b$</td>
                    <td>4.18 GeV</td>
                    <td>4.18 GeV</td>
                    <td>&lt; 0.1%</td>
                </tr>
                <tr>
                    <td>$m_\\tau$</td>
                    <td>1.777 GeV</td>
                    <td>1.777 GeV</td>
                    <td>&lt; 0.01%</td>
                </tr>
            </table>

'''

def main():
    with open('principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the insertion point
    old_text = '''            <h3 class="subsection-title">K.4 Source of Truth</h3>
            <p>
                All parameter values trace to <code>theory_output.json</code> generated by <code>run_all_simulations.py</code>. Simulation code is available in the <code>simulations/</code> directory with complete derivation chains documented in v12.8 Python modules.
            </p>

            <hr style="margin: 3rem 0;">'''

    new_text = '''            <h3 class="subsection-title">K.4 Source of Truth</h3>
            <p>
                All parameter values trace to <code>theory_output.json</code> generated by <code>run_all_simulations.py</code>. Simulation code is available in the <code>simulations/</code> directory with complete derivation chains documented in v12.8 Python modules.
            </p>
''' + appendix_l_content + '''
            <hr style="margin: 3rem 0;">'''

    if old_text in content:
        content = content.replace(old_text, new_text)
        with open('principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print('SUCCESS: Added Appendix L with complete PM values tables')
    else:
        print('ERROR: Could not find insertion point')

if __name__ == '__main__':
    main()
