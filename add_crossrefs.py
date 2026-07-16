#!/usr/bin/env python3
"""Add cross-references between related chapters in the Fields Medal book."""

import os
import re

# Define cross-reference relationships
# Key: chapter file (without .tex), Value: list of related chapters with descriptions
CROSS_REFS = {
    "chapter_1966_alexander_grothendieck": [
        ("chapter_1978_pierre_rene_deligne", "Grothendieck's student who proved the Weil conjectures"),
        ("chapter_1966_michael_francis_atiyah", "Atiyah-Singer index theorem uses Grothendieck's K-theory"),
        ("chapter_1974_david_bryant_mumford", "Mumford extended Grothendieck's algebraic geometry"),
        ("chapter_2002_vladimir_voevodsky", "Voevodsky extended motivic cohomology"),
        ("chapter_1978_daniel_g._quillen", "Quillen's K-theory builds on Grothendieck's foundational work"),
    ],
    "chapter_1978_pierre_rene_deligne": [
        ("chapter_1966_alexander_grothendieck", "Deligne was Grothendieck's student"),
        ("chapter_1954_jean_pierre_serre", "Serre's work on sheaf cohomology preceded Deligne"),
        ("chapter_1978_charles_louis_fefferman", "Fefferman proved the disk multiplier theorem"),
        ("chapter_1998_curtis_mcmullen", "McMullen's work on Hodge theory connects to Deligne"),
    ],
    "chapter_1954_jean_pierre_serre": [
        ("chapter_1978_pierre_rene_deligne", "Deligne extended Serre's work on algebraic varieties"),
        ("chapter_1966_alexander_grothendieck", "Grothendieck generalized Serre's cohomology"),
        ("chapter_1954_kunihiko_kodaira", "Kodaira's work on harmonic integrals relates to Serre"),
        ("chapter_1974_david_bryant_mumford", "Mumford used Serre's results in algebraic geometry"),
    ],
    "chapter_1986_simon_donaldson": [
        ("chapter_1986_michael_freedman", "Freedman's work on 4-manifolds complements Donaldson"),
        ("chapter_1966_michael_francis_atiyah", "Atiyah-Singer index theorem is foundational to Donaldson"),
        ("chapter_1990_edward_witten", "Witten applied Donaldson invariants to physics"),
    ],
    "chapter_1986_michael_freedman": [
        ("chapter_1986_simon_donaldson", "Donaldson's invariants distinguish exotic structures"),
        ("chapter_2006_grigori_perelman_declined", "Perelman proved Poincare, related to Freedman's classification"),
        ("chapter_2018_peter_scholze", "Scholze's work on p-adic geometry relates to Freedman"),
    ],
    "chapter_1990_edward_witten": [
        ("chapter_1986_simon_donaldson", "Witten applied Donaldson's invariants"),
        ("chapter_2006_terence_tao", "Tao worked on related harmonic analysis"),
        ("chapter_2018_peter_scholze", "Scholze's work connects to string theory"),
        ("chapter_1998_maxim_kontsevich", "Kontsevich's work on moduli spaces relates to Witten"),
    ],
    "chapter_1994_pierre_louis_lions": [
        ("chapter_2006_terence_tao", "Tao extended Lions' work on PDEs"),
        ("chapter_2002_laurent_lafforgue", "Lafforgue worked on Langlands"),
        ("chapter_2010_cedric_villani", "Villani is Lions' student"),
    ],
    "chapter_2006_terence_tao": [
        ("chapter_1994_pierre_louis_lions", "Lions' work on PDEs influenced Tao"),
        ("chapter_1998_timothy_gowers", "Gowers' work on compressed sensing relates to Tao"),
        ("chapter_2018_akshay_venkatesh", "Venkatesh collaborated with Tao"),
        ("chapter_2014_manjul_bhargava", "Bhargava's work on arithmetic relates to Tao"),
    ],
    "chapter_2018_peter_scholze": [
        ("chapter_2002_vladimir_voevodsky", "Voevodsky's motivic cohomology connects to Scholze"),
        ("chapter_1966_alexander_grothendieck", "Scholze's perfectoid spaces extend Grothendieck's vision"),
        ("chapter_1986_michael_freedman", "Freedman's topological methods relate to Scholze"),
        ("chapter_2022_june_huh", "Huh's work on log-concavity relates to Scholze"),
    ],
    "chapter_2002_vladimir_voevodsky": [
        ("chapter_1966_alexander_grothendieck", "Voevodsky extended Grothendieck's motivic cohomology"),
        ("chapter_2018_peter_scholze", "Scholze's work on perfectoid spaces connects to Voevodsky"),
        ("chapter_1978_daniel_g._quillen", "Quillen's K-theory relates to motivic cohomology"),
    ],
    "chapter_1966_michael_francis_atiyah": [
        ("chapter_1966_alexander_grothendieck", "Atiyah-Singer uses Grothendieck's K-theory"),
        ("chapter_1986_simon_donaldson", "Atiyah-Donaldson invariant"),
        ("chapter_1978_daniel_g._quillen", "Quillen collaborated with Atiyah"),
    ],
    "chapter_1978_daniel_g._quillen": [
        ("chapter_1966_alexander_grothendieck", "Quillen's K-theory builds on Grothendieck"),
        ("chapter_1966_michael_francis_atiyah", "Quillen collaborated with Atiyah"),
        ("chapter_2002_vladimir_voevodsky", "Voevodsky used model categories"),
    ],
    "chapter_2010_cedric_villani": [
        ("chapter_1994_pierre_louis_lions", "Villani is Lions' student"),
        ("chapter_2006_terence_tao", "Tao's work on PDEs relates to Villani"),
    ],
    "chapter_1982_shing_tung_yau": [
        ("chapter_2006_terence_tao", "Tao worked on related PDEs"),
        ("chapter_1954_kunihiko_kodaira", "Kodaira's work on harmonic integrals relates to Yau"),
    ],
    "chapter_2014_maryam_mirzakhani": [
        ("chapter_1982_william_thurston", "Thurston's work on Teichmüller theory influenced Mirzakhani"),
        ("chapter_2006_wendelin_werner", "Werner's work on SLE relates to Mirzakhani"),
    ],
    "chapter_2006_wendelin_werner": [
        ("chapter_2022_hugo_duminil_copin", "Duminil-Copin's work on percolation relates to SLE"),
        ("chapter_2014_maryam_mirzakhani", "Both work on geometric probability"),
        ("chapter_2010_stanislav_smirnov", "Smirnov's work on percolation relates to SLE"),
    ],
    "chapter_2010_stanislav_smirnov": [
        ("chapter_2006_wendelin_werner", "Smirnov's percolation work relates to SLE"),
        ("chapter_2022_hugo_duminil_copin", "Duminil-Copin extended Smirnov's work"),
    ],
    "chapter_2014_artur_avila": [
        ("chapter_1994_jean_christophe_yoccoz", "Yoccoz's work on renormalization influenced Avila"),
        ("chapter_1990_vladimir_drinfeld", "Drinfeld's work on vertex algebras relates to Avila"),
    ],
    "chapter_1994_jean_christophe_yoccoz": [
        ("chapter_2014_artur_avila", "Avila extended Yoccoz's work"),
        ("chapter_1994_jean_bourgain", "Bourgain worked on related problems"),
    ],
    "chapter_2014_manjul_bhargava": [
        ("chapter_1950_atle_selberg", "Selberg's trace formula relates to Bhargava"),
        ("chapter_1974_enrico_bombieri", "Bombieri's sieve methods relate to Bhargava"),
        ("chapter_2006_terence_tao", "Tao's analytic number theory relates to Bhargava"),
    ],
    "chapter_2022_james_maynard": [
        ("chapter_2014_manjul_bhargava", "Both work on number theory"),
        ("chapter_1950_atle_selberg", "Selberg's work on prime gaps influenced Maynard"),
    ],
    "chapter_2022_june_huh": [
        ("chapter_1974_david_bryant_mumford", "Mumford's work on algebraic geometry relates to Huh"),
        ("chapter_2018_peter_scholze", "Scholze's work connects to log-concavity"),
    ],
    "chapter_1998_timothy_gowers": [
        ("chapter_2006_terence_tao", "Gowers and Tao collaborated"),
        ("chapter_1990_edward_witten", "Gowers' work on compressed sensing relates to Witten"),
    ],
    "chapter_1998_maxim_kontsevich": [
        ("chapter_1990_edward_witten", "Witten's work on topological field theory relates"),
        ("chapter_1982_alain_connes", "Connes' noncommutative geometry relates to Kontsevich"),
    ],
    "chapter_1982_alain_connes": [
        ("chapter_1998_maxim_kontsevich", "Kontsevich's work relates to Connes"),
        ("chapter_1978_daniel_g._quillen", "Connes used cyclic homology from K-theory"),
    ],
    "chapter_1974_david_bryant_mumford": [
        ("chapter_1966_alexander_grothendieck", "Mumford extended Grothendieck's algebraic geometry"),
        ("chapter_1954_jean_pierre_serre", "Serre's work on algebraic varieties influenced Mumford"),
        ("chapter_2022_june_huh", "Huh's work on log-concavity relates to Mumford"),
    ],
    "chapter_1950_atle_selberg": [
        ("chapter_1974_enrico_bombieri", "Bombieri extended Selberg's sieve methods"),
        ("chapter_2014_manjul_bhargava", "Bhargava used Selberg's methods"),
        ("chapter_2022_james_maynard", "Maynard extended Selberg's work on prime gaps"),
    ],
    "chapter_1974_enrico_bombieri": [
        ("chapter_1950_atle_selberg", "Bombieri extended Selberg's work"),
        ("chapter_2014_manjul_bhargava", "Bhargava built on Bombieri's methods"),
    ],
    "chapter_2018_akshay_venkatesh": [
        ("chapter_2006_terence_tao", "Venkatesh collaborated with Tao"),
        ("chapter_1982_shing_tung_yau", "Venkatesh's work on harmonic analysis relates"),
    ],
    "chapter_2010_elon_lindenstrauss": [
        ("chapter_1990_edward_witten", "Lindenstrauss's work on ergodic theory relates"),
        ("chapter_2006_terence_tao", "Tao's work on ergodic theory relates"),
    ],
    "chapter_1970_serge_novikov": [
        ("chapter_1966_michael_francis_atiyah", "Atiyah's work on topology relates to Novikov"),
        ("chapter_1982_shing_tung_yau", "Yau's work on differential geometry relates"),
    ],
    "chapter_1966_stephen_smale": [
        ("chapter_1982_shing_tung_yau", "Smale's work on differential topology influenced Yau"),
        ("chapter_1994_efim_zelmanov", "Zelmanov's work on Lie algebras relates"),
    ],
    "chapter_1966_paul_joseph_cohen": [
        ("chapter_1970_john_griggs_thompson", "Cohen's work on set theory relates to Thompson"),
        ("chapter_1950_atle_selberg", "Cohen's work on Diophantine approximation relates"),
    ],
    "chapter_1950_laurent_schwartz": [
        ("chapter_1962_lars_hormander", "Hormander extended Schwartz's distribution theory"),
        ("chapter_1982_shing_tung_yau", "Yau's work on PDEs uses Schwartz's theory"),
    ],
    "chapter_1962_lars_hormander": [
        ("chapter_1950_laurent_schwartz", "Hormander extended Schwartz's distribution theory"),
        ("chapter_2006_terence_tao", "Tao used Hormander's work on oscillatory integrals"),
    ],
    "chapter_2022_maryna_viazovska": [
        ("chapter_1950_atle_selberg", "Viazovska's work on sphere packing relates to Selberg"),
        ("chapter_2006_andrei_okounkov", "Okounkov's work on modular forms relates"),
    ],
    "chapter_2018_caucher_birkar": [
        ("chapter_1990_shigefumi_mori", "Birkar's work on minimal models extends Mori's program"),
        ("chapter_2006_andrei_okounkov", "Birkar's work on birational geometry relates"),
    ],
    "chapter_1990_shigefumi_mori": [
        ("chapter_1974_david_bryant_mumford", "Mori's work extends Mumford's algebraic geometry"),
        ("chapter_2018_caucher_birkar", "Birkar extended Mori's minimal model program"),
    ],
    "chapter_1962_john_willard_milnor": [
        ("chapter_1954_kunihiko_kodaira", "Milnor's work on exotic spheres relates to Kodaira"),
        ("chapter_1982_alain_connes", "Connes' work on K-theory relates to Milnor"),
    ],
    "chapter_1954_kunihiko_kodaira": [
        ("chapter_1954_jean_pierre_serre", "Serre's work on cohomology relates to Kodaira"),
        ("chapter_1982_shing_tung_yau", "Yau's work on Calabi-Yau relates to Kodaira"),
    ],
    "chapter_1998_curtis_mcmullen": [
        ("chapter_1978_pierre_rene_deligne", "McMullen's work on Hodge theory relates to Deligne"),
        ("chapter_1986_michael_freedman", "McMullen's work on 3-manifolds relates"),
    ],
    "chapter_2010_ngo_bao_chau": [
        ("chapter_1966_alexander_grothendieck", "Ngô's work uses Grothendieck's techniques"),
        ("chapter_1978_pierre_rene_deligne", "Deligne's work on the Weil conjectures relates"),
    ],
    "chapter_2014_martin_hairer": [
        ("chapter_2006_terence_tao", "Hairer's work on stochastic PDEs relates to Tao"),
        ("chapter_1994_pierre_louis_lions", "Lions' work on PDEs relates to Hairer"),
    ],
    "chapter_2018_alessio_figalli": [
        ("chapter_2006_terence_tao", "Figalli's work on PDEs relates to Tao"),
        ("chapter_1982_shing_tung_yau", "Yau's work on differential geometry relates"),
    ],
    "chapter_1994_jean_bourgain": [
        ("chapter_2006_terence_tao", "Bourgain and Tao collaborated"),
        ("chapter_1994_pierre_louis_lions", "Bourgain's work on PDEs relates to Lions"),
    ],
    "chapter_1978_charles_louis_fefferman": [
        ("chapter_1982_shing_tung_yau", "Fefferman's work on PDEs relates to Yau"),
        ("chapter_1962_lars_hormander", "Fefferman used Hormander's work on PDEs"),
    ],
    "chapter_1970_heisuke_hironaka": [
        ("chapter_1966_alexander_grothendieck", "Hironaka's work on resolution relates to Grothendieck"),
        ("chapter_1974_david_bryant_mumford", "Mumford's work on singularities relates"),
    ],
    "chapter_1986_gerd_faltings": [
        ("chapter_1958_klaus_friedrich_roth", "Faltings extended Roth's theorem"),
        ("chapter_1974_enrico_bombieri", "Bombieri's work on diophantine equations relates"),
    ],
    "chapter_1958_klaus_friedrich_roth": [
        ("chapter_1986_gerd_faltings", "Faltings extended Roth's theorem"),
        ("chapter_1970_alan_baker", "Baker's work on linear forms relates to Roth"),
    ],
    "chapter_1970_alan_baker": [
        ("chapter_1958_klaus_friedrich_roth", "Baker extended Roth's theorem"),
        ("chapter_1986_gerd_faltings", "Faltings used Baker's methods"),
    ],
    "chapter_1986_gerd_faltings": [
        ("chapter_1958_klaus_friedrich_roth", "Faltings extended Roth's theorem"),
        ("chapter_1974_enrico_bombieri", "Bombieri's work on Diophantine equations relates"),
        ("chapter_1970_alan_baker", "Baker's work on linear forms relates"),
    ],
    "chapter_1978_gregori_alexandrovitch_margulis": [
        ("chapter_1966_stephen_smale", "Margulis's work on dynamics relates to Smale"),
        ("chapter_1994_jean_bourgain", "Bourgain's work on harmonic analysis relates"),
    ],
    "chapter_1990_vladimir_drinfeld": [
        ("chapter_1966_alexander_grothendieck", "Drinfeld's work on groups over rings relates"),
        ("chapter_2010_ngo_bao_chau", "Ngô's work on the fundamental lemma relates"),
    ],
    "chapter_1994_efim_zelmanov": [
        ("chapter_1970_john_griggs_thompson", "Zelmanov's work on Lie algebras relates to Thompson"),
        ("chapter_1966_stephen_smale", "Smale's work on dynamical systems relates"),
    ],
    "chapter_1970_john_griggs_thompson": [
        ("chapter_1994_efim_zelmanov", "Zelmanov extended Thompson's work on finite groups"),
        ("chapter_1970_serge_novikov", "Novikov's work on topology relates"),
    ],
    "chapter_1990_vaughan_jones": [
        ("chapter_2006_wendelin_werner", "Werner's SLE work relates to Jones polynomial"),
        ("chapter_2010_stanislav_smirnov", "Smirnov's work on percolation relates"),
    ],
    "chapter_2006_andrei_okounkov": [
        ("chapter_2022_maryna_viazovska", "Viazovska's work on sphere packing relates"),
        ("chapter_2018_caucher_birkar", "Birkar's work on birational geometry relates"),
        ("chapter_1998_maxim_kontsevich", "Okounkov's work on moduli spaces relates"),
    ],
    "chapter_2022_hugo_duminil_copin": [
        ("chapter_2006_wendelin_werner", "Duminil-Copin's work relates to Werner's SLE"),
        ("chapter_2010_stanislav_smirnov", "Duminil-Copin extended Smirnov's percolation work"),
    ],
    "chapter_2022_june_huh": [
        ("chapter_1974_david_bryant_mumford", "Huh's work on algebraic geometry relates to Mumford"),
        ("chapter_2018_peter_scholze", "Scholze's work connects to log-concavity"),
    ],
    "chapter_1936_jesse_douglas": [
        ("chapter_1982_shing_tung_yau", "Douglas's Plateau problem relates to Yau"),
    ],
    "chapter_1936_lars_valerian_ahlfors": [
        ("chapter_1954_kunihiko_kodaira", "Ahlfors's work on Riemann surfaces relates to Kodaira"),
        ("chapter_1958_rene_thom", "Thom's cobordism relates to Ahlfors"),
    ],
    "chapter_1958_rene_thom": [
        ("chapter_1986_simon_donaldson", "Thom's cobordism relates to Donaldson"),
        ("chapter_1966_stephen_smale", "Smale's work on h-cobordism relates to Thom"),
    ],
    "chapter_1982_william_thurston": [
        ("chapter_1986_simon_donaldson", "Thurston's work on 3-manifolds relates to Donaldson"),
        ("chapter_1986_michael_freedman", "Freedman's work on 4-manifolds relates to Thurston"),
        ("chapter_2014_maryam_mirzakhani", "Mirzakhani used Thurston's work"),
    ],
    "chapter_1970_serge_novikov": [
        ("chapter_1966_michael_francis_atiyah", "Atiyah's work on topology relates to Novikov"),
    ],
    "chapter_1998_richard_borcherds": [
        ("chapter_1998_maxim_kontsevich", "Borcherds and Kontsevich both work on vertex algebras"),
        ("chapter_1978_gregori_alexandrovitch_margulis", "Borcherds' work on lattices relates to Margulis"),
    ],
    "chapter_1990_vladimir_drinfeld": [
        ("chapter_1966_alexander_grothendieck", "Drinfeld's work on groups relates to Grothendieck"),
        ("chapter_2010_ngo_bao_chau", "Ngô's work on the fundamental lemma relates"),
    ],
    "chapter_2006_grigori_perelman_declined": [
        ("chapter_1986_michael_freedman", "Freedman's work on Poincare conjecture relates"),
        ("chapter_1982_shing_tung_yau", "Perelman proved the Poincare conjecture"),
        ("chapter_1986_simon_donaldson", "Donaldson's invariants relate to Perelman's work"),
    ],
    "chapter_1970_john_griggs_thompson": [
        ("chapter_1994_efim_zelmanov", "Zelmanov extended Thompson's work"),
        ("chapter_1998_richard_borcherds", "Borcherds' work on vertex algebras relates"),
    ],
}

def add_crossrefs():
    """Add cross-reference sections to chapters."""
    base_dir = "chapters"
    
    for chapter, refs in CROSS_REFS.items():
        filepath = os.path.join(base_dir, f"{chapter}.tex")
        if not os.path.exists(filepath):
            print(f"SKIP: {chapter} not found")
            continue
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Skip if already has cross-references
        if "See Also" in content or "Related Chapters" in content:
            print(f"SKIP: {chapter} already has cross-refs")
            continue
        
        # Build cross-reference block
        crossref_block = [
            "\n\\begin{center}\\rule{0.5\\linewidth}{0.5pt}\\end{center}\n",
            "\n",
            "\\section*{See Also}\n",
            "\\addcontentsline{toc}{section}{See Also}\n",
            "\n",
            "This chapter relates to the following work by other Fields Medalists:\n",
            "\\begin{itemize}\n",
        ]
        
        for ref_chapter, description in refs:
            ref_file = os.path.join(base_dir, f"{ref_chapter}.tex")
            if os.path.exists(ref_file):
                # Extract label from ref_chapter
                with open(ref_file, 'r') as f:
                    first_line = f.readline()
                label_match = re.search(r'\\label\{([^}]+)\}', first_line)
                if label_match:
                    ref_label = label_match.group(1)
                    crossref_block.append(
                        f'  \\item \\textbf{{\\hyperref[{ref_label}]{{See Chapter on related work}}}} --- {description}.\n'
                    )
                else:
                    crossref_block.append(
                        f'  \\item {description}.\n'
                    )
            else:
                crossref_block.append(
                    f'  \\item {description}.\n'
                )
        
        crossref_block.append("\\end{itemize}\n")
        crossref_block.append("\n")
        
        # Insert before the final end or references section
        # Find the last \end{longtable} or \emph{(End of report)}
        insert_pos = len(content)
        for pattern in [r'\\emph{\(End of report\)}', r'\\end\{longtable\}', r'\\section\{References']:
            match = re.search(pattern, content)
            if match:
                insert_pos = match.start()
                break
        
        new_content = content[:insert_pos] + "".join(crossref_block) + content[insert_pos:]
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        
        print(f"Added cross-refs to {chapter}")

if __name__ == "__main__":
    add_crossrefs()
