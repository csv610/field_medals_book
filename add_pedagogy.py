#!/usr/bin/env python3
"""Add pedagogical infrastructure to all chapter files."""
import re, os, sys

# Map of chapter filename -> (mathematician, year, field, prerequisites, objectives, exercises, summary)
CHAPTER_DATA = {
    "chapter_1936_jesse_douglas": {
        "name": "Jesse Douglas", "year": "1936",
        "field": "Calculus of Variations, Minimal Surfaces",
        "prereqs": "Multivariable calculus (partial derivatives, double integrals), basic topology of curves and surfaces, introductory real analysis.",
        "objectives": "Understand Plateau's problem and its historical significance; state the Douglas solution and its main ingredients; explain why minimal surfaces are important in geometry and physics.",
        "exercises": [
            r"Verify that the catenoid $z = \cosh^{-1}(r)$ has zero mean curvature by computing $H = \frac{1}{2}(k_1 + k_2)$.",
            r"Show that the functional $I(X) = \int_D \|X_u \times X_v\| \, du\, dv$ is invariant under reparametrization of $D$.",
            r"Compute the first variation of the area functional for a surface $X: D \to \mathbb{R}^3$ and derive the minimal surface equation $\Delta X = 0$.",
            r"Prove that a plane is a minimal surface by verifying the mean curvature vanishes identically.",
        ],
        "summary": "Douglas solved Plateau's problem in 1931, proving that every rectifiable simple closed curve in $\\mathbb{R}^3$ bounds a disk of least area. His approach used the Douglas functional, a variational principle on the unit disc, and introduced techniques that became foundational for geometric analysis."
    },
    "chapter_1936_lars_valerian_ahlfors": {
        "name": "Lars Ahlfors", "year": "1936",
        "field": "Complex Analysis",
        "prereqs": "Complex numbers, analytic functions, contour integration, basic knowledge of Riemann surfaces.",
        "objectives": "Explain the Ahlfors five-disk theorem and its significance; describe the connection between curvature and covering spaces; state the main results of Ahlfors's geometric function theory.",
        "exercises": [
            r"Prove that a bounded entire function is constant (Liouville's theorem) and explain how Ahlfors's work extends this to geometric settings.",
            r"Compute the hyperbolic metric on the unit disc $\mathbb{D}$ and verify that it is invariant under Möbius transformations.",
            r"Show that the Gaussian curvature of the Poincaré metric $ds = \frac{2|dz|}{1-|z|^2}$ on $\mathbb{D}$ is $K = -1$.",
            r"Verify the Ahlfors-Schwarz lemma: if $f: \mathbb{D} \to \mathbb{D}$ is holomorphic, then $f^*(ds_{\text{hyp}}) \leq ds_{\text{hyp}}$.",
        ],
        "summary": "Ahlfors revolutionized geometric function theory by applying hyperbolic geometry to complex analysis. His proof of the Riemann mapping theorem using extremal length, and his work on the value distribution theory of meromorphic functions, established the deep connection between complex analysis and differential geometry."
    },
    "chapter_1950_atle_selberg": {
        "name": "Atle Selberg", "year": "1950",
        "field": "Number Theory, Automorphic Forms",
        "prereqs": "Elementary number theory (congruences, Euler's totient function), basic complex analysis, Fourier series.",
        "objectives": "State the Selberg sieve and explain its principle; describe the trace formula and its significance; understand Selberg's contribution to the prime number theorem for arithmetic progressions.",
        "exercises": [
            r"Compute $\sum_{n \leq x} \Lambda(n) \frac{x}{n}$ for $x = 100$ to illustrate the prime number theorem.",
            r"Derive the elementary proof that $\sum_{p \leq x} \frac{1}{p} \sim \ln \ln x$ using Selberg's inequality.",
            r"Verify Selberg's symmetric formula for the theta function: $\theta(x) + \theta(y) = \theta(xy) + \theta(x/y)$ in a special case.",
            r"Show that the Selberg sieve gives an upper bound for the number of primes in an arithmetic progression that is $O(x / (\phi(q) \log \log x))$.",
        ],
        "summary": "Selberg developed the Selberg sieve, one of the most powerful elementary tools in analytic number theory, and proved the trace formula for automorphic forms. His elementary proof of the prime number theorem (independently of Erd\\H{o}s) showed that deep results about primes can be obtained without complex analysis."
    },
    "chapter_1950_laurent_schwartz": {
        "name": "Laurent Schwartz", "year": "1950",
        "field": "Functional Analysis, Distributions",
        "prereqs": "Measure theory (Lebesgue integral), basic functional analysis (Banach spaces, linear functionals), ordinary differential equations.",
        "objectives": "Define distributions as continuous linear functionals on test functions; explain why the Dirac delta function is a distribution; state the main theorem of distribution theory relevant to PDEs.",
        "exercises": [
            r"Verify that the Dirac delta $\delta$ defined by $\langle \delta, \varphi \rangle = \varphi(0)$ is a distribution of order 0.",
            r"Compute the distributional derivative of the Heaviside step function $H(x)$ and show it equals $\delta$.",
            r"Show that every locally integrable function defines a distribution via $T_f(\varphi) = \int f(x)\varphi(x)\,dx$.",
            r"Prove that the Fourier transform of a tempered distribution is well-defined and extends the classical Fourier transform.",
        ],
        "summary": "Schwartz created the theory of distributions, providing a rigorous framework for the Dirac delta and other ``generalized functions'' that physicists had been using informally. This theory resolved foundational issues in PDE theory and became indispensable in modern analysis, physics, and signal processing."
    },
    "chapter_1954_jean_pierre_serre": {
        "name": "Jean-Pierre Serre", "year": "1954",
        "field": "Algebraic Topology, Algebraic Geometry",
        "prereqs": "Point-set topology (fundamental group, covering spaces), basic homological algebra (chain complexes), abstract algebra (groups, rings, modules).",
        "objectives": "Explain the computation of $H^*(\mathbb{CP}^n, \mathbb{Z})$; describe Serre's contribution to the finiteness of homotopy groups; state the Cartan-Serre theorem.",
        "exercises": [
            r"Compute the singular homology groups $H_k(\mathbb{CP}^n, \mathbb{Z})$ for all $k$ using the cell structure.",
            r"Show that $\pi_k(S^n) = 0$ for $k < n$ using the Hurewicz theorem.",
            r"Verify that the Serre spectral sequence for the fibration $S^1 \to S^3 \to S^2$ converges to the correct homology.",
            r"Prove that a simply connected space with trivial rational homology has trivial rational homotopy groups.",
        ],
        "summary": "Serre transformed algebraic topology by introducing spectral sequences, computing homotopy groups of spheres, and establishing deep connections between algebraic geometry and topology. His foundational work on coherent sheaves and the Faisceaux Alg\\'{e}briques Coh\\'{e}rents (FAC) laid the groundwork for modern algebraic geometry."
    },
    "chapter_1954_kunihiko_kodaira": {
        "name": "Kunihiko Kodaira", "year": "1954",
        "field": "Algebraic Geometry, Differential Geometry",
        "prereqs": "Complex analysis (Riemann surfaces), differential geometry (connections, curvature), basic algebraic geometry (sheaves, cohomology).",
        "objectives": "Explain Kodaira's embedding theorem and its significance; describe the classification of compact Riemann surfaces; understand the role of harmonic forms in Kodaira's work.",
        "exercises": [
            r"Show that every compact Riemann surface is a projective algebraic variety (Kodaira embedding theorem in dimension 1).",
            r"Compute the dimension of the space of holomorphic 1-forms on a Riemann surface of genus $g$.",
            r"Verify that the Riemann-Roch theorem gives $\dim H^0(L) - \dim H^1(L) = \deg(L) - g + 1$ for a line bundle $L$ on a curve of genus $g$.",
            r"Prove that a compact complex manifold with a positive line bundle is projective (sketch Kodaira's argument).",
        ],
        "summary": "Kodaira proved that every compact complex manifold admitting a positive line bundle is projective algebraic, bridging differential geometry and algebraic geometry. His classification of compact surfaces and his work on harmonic forms on Riemannian manifolds established fundamental tools still used throughout geometry."
    },
    "chapter_1958_klaus_friedrich_roth": {
        "name": "Klaus Roth", "year": "1958",
        "field": "Number Theory, Diophantine Approximation",
        "prereqs": "Elementary number theory, basic real analysis (sequences, convergence), pigeonhole principle.",
        "objectives": "State Roth's theorem on diophantine approximation; explain why it is a deep generalization of Liouville's theorem; describe the application to the Thue-Siegel-Roth conjecture.",
        "exercises": [
            r"Prove Liouville's theorem: if $\alpha$ is irrational and algebraic of degree $n$, then $|\alpha - p/q| > c/q^n$ for all $p/q$.",
            r"Show that Roth's theorem implies that algebraic irrationals have irrationality measure 2 (best possible).",
            r"Verify that $\sum_{q=1}^{Q} \|q\alpha\| \leq C \log Q$ for any irrational $\alpha$ using Dirichlet's approximation.",
            r"Compute the continued fraction expansion of $\sqrt{2}$ and discuss how it relates to best rational approximations.",
        ],
        "summary": "Roth proved that for any algebraic irrational $\\alpha$ and any $\\epsilon > 0$, the inequality $|\\alpha - p/q| < 1/q^{2+\\epsilon}$ has only finitely many solutions. This settled the Thue-Siegel conjecture and remains the strongest result in metric diophantine approximation."
    },
    "chapter_1958_rene_thom": {
        "name": "Ren\\'{e} Thom", "year": "1958",
        "field": "Topology, Catastrophe Theory",
        "prereqs": "Differential topology (manifolds, transversality), basic singularity theory, multivariable calculus.",
        "objectives": "State the classification theorem for smooth manifolds of dimension $< 5$; explain the cobordism theory; describe the seven elementary catastrophes.",
        "exercises": [
            r"Classify all smooth compact connected surfaces without boundary up to diffeomorphism.",
            r"Show that two 3-manifolds are cobordant if and only if they are orientation-preserving diffeomorphic.",
            r"Verify that the cusp catastrophe $V(x) = x^4 + ax^2 + bx$ has exactly two fold lines and one cusp point.",
            r"Compute the cobordism ring $\\Omega_*^{SO}$ in low dimensions.",
        ],
        "summary": "Thom created cobordism theory, showing that manifolds can be classified by algebraic invariants, and developed catastrophe theory as a mathematical framework for studying abrupt changes in continuous systems. His work connected topology, differential geometry, and applications to the natural sciences."
    },
    "chapter_1962_john_willard_milnor": {
        "name": "John Milnor", "year": "1962",
        "field": "Differential Topology, Algebraic Topology",
        "prereqs": "Differential topology (smooth manifolds, tangent bundles), homotopy theory (fundamental group, covering spaces), basic algebraic topology.",
        "objectives": "Explain the discovery of exotic spheres; describe the h-cobordism theorem and its significance; understand Milnor K-theory as a generalization of the Brauer group.",
        "exercises": [
            r"Show that $S^7$ admits exotic smooth structures by verifying that the Milnor sphere is not diffeomorphic to the standard $S^7$.",
            r"Compute the K-theory groups $K_0(\\mathbb{R})$ and $K_1(\\mathbb{R})$ for the real numbers.",
            r"Prove that the diagonal map $\\Delta: M \\to M \\times M$ defines a non-trivial element in the cobordism ring for $M = \\mathbb{RP}^2$.",
            r"Verify that the Alexander polynomial of the trefoil knot is $t^2 - t + 1$.",
        ],
        "summary": "Milnor discovered exotic smooth structures on $S^7$, proved the h-cobordism theorem for dimensions $\\geq 5$, and created K-theory as an algebraic invariant of topological spaces. His expository elegance and breadth of contribution across differential topology, algebraic topology, and dynamical systems set the standard for modern mathematical research."
    },
    "chapter_1962_lars_hormander": {
        "name": "Lars H\\'{o}rmander", "year": "1962",
        "field": "Partial Differential Equations, Functional Analysis",
        "prereqs": "Real analysis (Lebesgue measure, $L^p$ spaces), Fourier analysis basics, basic functional analysis.",
        "objectives": "State the H\\'{o}rmander condition for hypoellipticity; explain the pseudodifferential operator framework; describe the $L^2$ theory of the $\overline{\partial}$ operator.",
        "exercises": [
            r"Verify that the Laplacian $\\Delta$ satisfies the H\\'{o}rmander condition $\\sum |a_{ij}(x)| \\leq C$.",
            r"Compute the Fourier transform of $e^{-|\\xi|^2}$ and verify the Parseval identity.",
            r"Show that $P(D) = -\\Delta + 1$ is elliptic by checking the principal symbol.",
            r"Prove that a distribution $u$ satisfying $Pu = f$ with $P$ hypoelliptic is smooth wherever $f$ is smooth.",
        ],
        "summary": "H\\'{o}rmander developed the modern $L^2$ theory of PDEs, introducing pseudodifferential operators and the Fourier integral operator framework. His characterization of hypoellipticity and his work on the $\overline{\partial}$-Neumann problem established the functional-analytic foundations of modern PDE theory."
    },
    "chapter_1966_alexander_grothendieck": {
        "name": "Alexander Grothendieck", "year": "1966",
        "field": "Algebraic Geometry, Category Theory",
        "prereqs": "Abstract algebra (rings, ideals, modules), basic category theory (functors, natural transformations), point-set topology.",
        "objectives": "Explain the scheme-theoretic generalization of algebraic geometry; describe the six operations of étale cohomology; understand motives as universal cohomology theories.",
        "exercises": [
            r"Show that $\\operatorname{Spec}(\\mathbb{Z})$ is a scheme and describe its closed points.",
            r"Prove that the product of two affine schemes $\\operatorname{Spec}(A) \\times \\operatorname{Spec}(B)$ is $\\operatorname{Spec}(A \\otimes_{\\mathbb{Z}} B)$.",
            r"Compute the étale fundamental group of $\\mathbb{A}^1_k$ for an algebraically closed field $k$.",
            r"Verify that the category of pure motives admits a tensor product by constructing the tensor product of correspondences.",
        ],
        "summary": "Grothendieck revolutionized algebraic geometry by introducing schemes, sheaf cohomology, and the language of categories. His \\'{E}l\\'{e}ments de G\\'{e}om\\'{e}trie Alg\\'{e}brique (EGA) and S\\'{e}minaire de G\\'{e}om\\'{e}trie Alg\\'{e}brique (SGA) reshaped the foundations of the field and his vision of motives continues to guide modern research."
    },
    "chapter_1966_michael_francis_atiyah": {
        "name": "Michael Atiyah", "year": "1966",
        "field": "Topology, Differential Geometry, Mathematical Physics",
        "prereqs": "Algebraic topology (K-theory, characteristic classes), differential geometry (vector bundles, connections), basic complex analysis.",
        "objectives": "State the Atiyah-Singer index theorem and explain its significance; describe K-theory as a generalized cohomology theory; explain the connection between topology and physics.",
        "exercises": [
            r"Compute the index of the Dirac operator on $S^2$ using the Atiyah-Singer formula.",
            r"Verify that the Chern character is a ring homomorphism $K^*(X) \\otimes \\mathbb{Q} \\to H^*(X; \\mathbb{Q})$.",
            r"Show that the tangent bundle of $S^2$ is not trivial by computing its first Chern class.",
            r"Prove the Bott periodicity theorem for $K^*(S^n)$ in the special case $n = 1$.",
        ],
        "summary": "Atiyah proved the Atiyah-Singer index theorem, connecting the analytical index of elliptic operators to topological invariants of the underlying manifold. Together with Singer, he unified analysis, topology, and geometry, and his work on K-theory and mathematical physics opened entirely new fields of research."
    },
    "chapter_1966_paul_joseph_cohen": {
        "name": "Paul Cohen", "year": "1966",
        "field": "Set Theory, Mathematical Logic",
        "prereqs": "Mathematical logic (axioms of ZFC, first-order logic), basic set theory (cardinal and ordinal numbers), familiarity with the continuum hypothesis.",
        "objectives": "Explain forcing and how it proves the independence of CH; describe the method of Boolean-valued models; understand the significance of the independence results.",
        "exercises": [
            r"Construct a countable transitive model of ZFC and explain why it exists.",
            r"Define a partial order that adds a generic subset of $\\omega_1$ and verify the countable chain condition.",
            r"Show that if $M \\models ZFC$ and $G$ is $M$-generic, then $M[G] \\models ZFC$.",
            r"Prove that $\\neg CH$ is consistent with ZFC by sketching the forcing argument.",
        ],
        "summary": "Cohen invented the method of forcing, proving that the Continuum Hypothesis is independent of ZFC set theory. This technique became the central tool of set theory and one of the most important methods in mathematical logic, resolving Hilbert's first problem and revealing the genuine independence of many mathematical statements."
    },
    "chapter_1966_stephen_smale": {
        "name": "Stephen Smale", "year": "1966",
        "field": "Differential Topology, Dynamical Systems",
        "prereqs": "Differential topology (manifolds, transversality, Morse theory), basic dynamical systems (flows, fixed points).",
        "objectives": "Explain the h-cobordism theorem and its proof strategy; describe Smale's horseshoe map and its implications for chaos; understand the generalized Poincar\\'{e} conjecture.",
        "exercises": [
            r"Construct the Smale horseshoe map explicitly and compute the invariant Cantor set.",
            r"Prove that the torus $T^2$ embeds in $\\mathbb{R}^3$ but $S^3$ does not embed in $\\mathbb{R}^4$ (for $n \\leq 6$).",
            r"Verify that the Lorenz attractor has a strange attractor by computing Lyapunov exponents numerically.",
            r"Show that a Morse function on a compact manifold has finitely many critical points, each of which is non-degenerate.",
        ],
        "summary": "Smale proved the higher-dimensional Poincar\\'{e} conjecture and the h-cobordism theorem, establishing the foundations of high-dimensional manifold topology. His discovery of the horseshoe map and his work on hyperbolic dynamics revealed the mathematical structure of chaotic systems."
    },
    "chapter_1970_alan_baker": {
        "name": "Alan Baker", "year": "1970",
        "field": "Number Theory, Transcendental Number Theory",
        "prereqs": "Elementary number theory, basic abstract algebra (field extensions, algebraic numbers), complex analysis.",
        "objectives": "State Baker's theorem on linear forms in logarithms; explain its applications to Diophantine equations; describe the effective bounds it provides.",
        "exercises": [
            r"Prove that $\\log 2$ is irrational using the pigeonhole principle.",
            r"Show that if $\\alpha_1, \\ldots, \\alpha_n$ are non-zero algebraic numbers, then $1, \\log \\alpha_1, \\ldots, \\log \\alpha_n$ are linearly independent over the algebraic numbers (Baker's theorem in the simplest case).",
            r"Use Baker's theorem to prove that the equation $2^x - 3^y = 1$ has only the solutions $(x,y) = (1,0)$ and $(2,1)$.",
            r"Compute an explicit lower bound for $|b_1 \\log \\alpha_1 + b_2 \\log \\alpha_2|$ for given algebraic $\\alpha_1, \\alpha_2$ and integers $b_1, b_2$.",
        ],
        "summary": "Baker proved deep results on linear forms in logarithms, providing effective lower bounds that have numerous applications to Diophantine equations. His theorem resolved classical problems such as the class number problem and effective versions of the Thue equation, becoming a fundamental tool in computational number theory."
    },
    "chapter_1970_heisuke_hironaka": {
        "name": "Heisuke Hironaka", "year": "1970",
        "field": "Algebraic Geometry, Resolution of Singularities",
        "prereqs": "Commutative algebra (local rings, primary decomposition), basic algebraic geometry (varieties, singularities), differential geometry.",
        "objectives": "State the resolution of singularities theorem in characteristic zero; explain the role of blow-ups; describe the Hironaka characteristic polyhedron.",
        "exercises": [
            r"Perform a blow-up of the singularity $y^2 - x^3 = 0$ at the origin and show it resolves the singularity.",
            r"Compute the exceptional divisor of a blow-up of $\\mathbb{A}^2$ at a point.",
            r"Show that the singularity $x^2 + y^3 + z^5 = 0$ in $\\mathbb{A}^3$ is isolated and compute its multiplicity.",
            r"Verify that a smooth variety over a field of characteristic zero has no singular points in any chart of an ambient projective space.",
        ],
        "summary": "Hironaka proved that every algebraic variety over a field of characteristic zero can be resolved to a smooth variety by a finite sequence of blow-ups along smooth centers. This landmark result settled a fundamental problem in algebraic geometry and introduced new techniques that continue to influence the field."
    },
    "chapter_1970_john_griggs_thompson": {
        "name": "John Thompson", "year": "1970",
        "field": "Group Theory, Finite Simple Groups",
        "prereqs": "Abstract algebra (groups, subgroups, normal subgroups, group actions), basic representation theory.",
        "objectives": "Explain the Feit-Thompson theorem (odd order theorem); describe the classification of finite simple groups; understand the role of Sylow theory in the proof.",
        "exercises": [
            r"Prove that every group of order $pq$ (with $p < q$ primes and $p \\nmid q-1$) is cyclic.",
            r"Show that a group of order $2p$ (with $p$ an odd prime) has a normal subgroup of order $p$.",
            r"Verify that the alternating group $A_5$ is simple by computing its conjugacy classes.",
            r"Prove that every group of odd order is solvable (sketch the Feit-Thompson argument).",
        ],
        "summary": "Thompson, together with Feit, proved the Feit-Thompson theorem: every finite group of odd order is solvable. This was a cornerstone of the classification of finite simple groups. Thompson's subsequent work on $N$-groups and the identification of the Thompson sporadic group were equally influential."
    },
    "chapter_1970_serge_novikov": {
        "name": "Sergei Novikov", "year": "1970",
        "field": "Topology, Differential Topology",
        "prereqs": "Algebraic topology (homology, cohomology, characteristic classes), differential topology (manifolds, surgery).",
        "objectives": "State the Novikov theorem on the topological invariance of rational Pontryagin classes; explain the surgery exact sequence; describe the s-cobordism theorem.",
        "exercises": [
            r"Compute the Pontryagin classes of $\\mathbb{CP}^n$ and verify they are topological invariants.",
            r"Show that two simply connected manifolds of dimension $\\geq 5$ are h-cobordant if and only if they are homeomorphic.",
            r"Construct the surgery exact sequence for a compact manifold of dimension 4.",
            r"Prove that the signature of a $4k$-dimensional manifold is a topological invariant.",
        ],
        "summary": "Novikov proved the topological invariance of rational Pontryagin classes, a fundamental result linking the topology and geometry of manifolds. His work on surgery theory and the topology of manifolds provided the framework for the modern classification of high-dimensional manifolds."
    },
    "chapter_1974_david_bryant_mumford": {
        "name": "David Mumford", "year": "1974",
        "field": "Algebraic Geometry",
        "prereqs": "Commutative algebra (graded rings, projective spectra), basic algebraic geometry (varieties, morphisms), complex analysis.",
        "objectives": "Explain the geometric invariant theory (GIT) and its applications; describe the Mumford compactness theorem; understand the connection between algebraic geometry and number theory.",
        "exercises": [
            r"Compute the invariant ring $k[x,y]^G$ for $G = \\mathbb{Z}/2\\mathbb{Z}$ acting by $(x,y) \\mapsto (-x,-y)$.",
            r"Show that the moduli space of elliptic curves is constructed as a quotient using GIT.",
            r"Verify that the Igusa blow-up resolves the singularity of a family of curves at a node.",
            r"Prove that the dimension of the moduli space of curves of genus $g \\geq 2$ is $3g-3$.",
        ],
        "summary": "Mumford created geometric invariant theory (GIT) as a tool for constructing moduli spaces, and his work on algebraic surfaces and curves established the foundations of modern birational geometry. His \\textit{Red Book of Varieties and Schemes} became a standard reference and his contributions to pattern theory extended his influence beyond pure mathematics."
    },
    "chapter_1974_enrico_bombieri": {
        "name": "Enrico Bombieri", "year": "1974",
        "field": "Number Theory, Algebraic Geometry",
        "prereqs": "Analytic number theory (prime number theorem, sieve methods), basic algebraic geometry (elliptic curves).",
        "objectives": "Explain the Bombieri-Vinogradov theorem and its significance; describe the large sieve method; understand Bombieri's contributions to the Mordell conjecture.",
        "exercises": [
            r"Prove the Bombieri-Vinogradov theorem for the prime number theorem in arithmetic progressions.",
            r"Derive the large sieve inequality for character sums.",
            r"Verify that an elliptic curve $E: y^2 = x^3 + ax + b$ over $\\mathbb{Q}$ has finite Mordell-Weil group modulo torsion.",
            r"Show that the Selberg sieve gives an upper bound for the twin prime conjecture that is $O(x / (\\log x)^2)$.",
        ],
        "summary": "Bombieri made fundamental contributions to analytic number theory (the Bombieri-Vinogradov theorem, the large sieve) and algebraic geometry (the Bombieri-Lang conjecture, contributions to the Mordell conjecture). His work bridged these fields and he was known for his extraordinary breadth and depth across mathematics."
    },
    "chapter_1978_charles_louis_fefferman": {
        "name": "Charles Fefferman", "year": "1978",
        "field": "Analysis, Partial Differential Equations",
        "prereqs": "Real analysis ($L^p$ spaces, Fourier analysis), basic PDE theory (wave equation, heat equation), functional analysis.",
        "objectives": "State the Carleson theorem on pointwise convergence of Fourier series; explain the regularity theory for the Navier-Stokes equations; describe the finite dimensional extension problem.",
        "exercises": [
            r"Prove the Carleson theorem: the Fourier series of an $L^2$ function converges pointwise almost everywhere.",
            r"Show that the Cauchy problem for the wave equation in $\\mathbb{R}^3$ has a unique solution in $C^2$.",
            r"Verify that the Dirichlet problem on the unit disc has a solution given by the Poisson integral.",
            r"Compute the first eigenvalue of the Laplacian on the unit disc with Dirichlet boundary conditions.",
        ],
        "summary": "Fefferman proved the almost everywhere convergence of Fourier series (Carleson's theorem) and developed powerful techniques in PDE regularity theory. His work on the Dirichlet problem, harmonic analysis, and the Navier-Stokes equations established new connections between real analysis and partial differential equations."
    },
    "chapter_1978_daniel_g._quillen": {
        "name": "Daniel Quillen", "year": "1978",
        "field": "Algebraic K-Theory, Homotopy Theory",
        "prereqs": "Algebraic topology (homotopy groups, fiber bundles), abstract algebra (groups, rings, modules), basic category theory.",
        "objectives": "Explain the plus construction and Q-construction for K-theory; describe the relationship between K-theory and algebraic geometry; understand the Quillen-Lichtenbaum conjecture.",
        "exercises": [
            r"Compute $K_0(\\mathbb{Z})$ and $K_1(\\mathbb{Z})$ using the definitions.",
            r"Show that the plus construction applied to $BGL(\\mathbb{Z})^+$ gives the correct homotopy groups for algebraic K-theory of $\\mathbb{Z}$.",
            r"Verify that the Q-construction gives the same $K$-groups as the plus construction for regular rings.",
            r"Compute the K-theory groups $K_*(\\mathbb{F}_q)$ for a finite field.",
        ],
        "summary": "Quillen defined higher algebraic K-theory using the plus construction and the Q-construction, providing a framework that unified and extended classical K-theory. His work on the Adams conjecture, the Quillen-Lichtenbaum conjecture, and homotopical algebra transformed algebraic K-theory into a central tool in modern algebra and topology."
    },
    "chapter_1978_gregori_alexandrovitch_margulis": {
        "name": "Gregori Margulis", "year": "1978",
        "field": "Lie Groups, Ergodic Theory, Number Theory",
        "prereqs": "Lie groups and Lie algebras (basic theory), measure theory, representation theory (character theory of finite groups).",
        "objectives": "State the Margulis superrigidity theorem; explain the arithmeticity of lattices; describe the construction of expander graphs using Property (T).",
        "exercises": [
            r"Show that $SL_n(\\mathbb{Z})$ is a lattice in $SL_n(\\mathbb{R})$ for $n \\geq 2$.",
            r"Prove that a lattice in a semisimple Lie group is arithmetic if and only if it is commensurable with an arithmetic subgroup.",
            r"Verify that the construction of expander graphs from Property (T) gives a family of $(n, d, \\lambda)$-expander graphs with $\\lambda$ bounded away from 1.",
            r"Show that the homogeneous space $SL_n(\\mathbb{R})/SL_n(\\mathbb{Z})$ has finite invariant measure.",
        ],
        "summary": "Margulis proved the arithmeticity and superrigidity theorems for lattices in semisimple Lie groups, and constructed the first explicit families of expander graphs. His work unified ergodic theory, Lie theory, and number theory, and his contributions to differential geometry and homogeneous dynamics continue to influence multiple fields."
    },
    "chapter_1978_pierre_rene_deligne": {
        "name": "Pierre Deligne", "year": "1978",
        "field": "Algebraic Geometry, Number Theory",
        "prereqs": "Algebraic geometry (schemes, sheaf cohomology), number theory (zeta functions, L-functions), basic representation theory.",
        "objectives": "State the Weil conjectures and explain Deligne's proof strategy; describe the relationship between the Riemann hypothesis and eigenvalues of Frobenius; understand the role of $\\ell$-adic cohomology.",
        "exercises": [
            r"Compute the zeta function of $\\mathbb{P}^1$ over $\\mathbb{F}_q$ and verify it satisfies the rationality conjecture.",
            r"Show that the eigenvalues of Frobenius on $H^1$ of an elliptic curve over $\\mathbb{F}_q$ have absolute value $\\sqrt{q}$ (Riemann hypothesis for curves).",
            r"Verify the functional equation $Z(X, t) = \\pm q^{\\chi/2} t^{\\chi} Z(X, 1/qt)$ for a smooth projective variety $X$.",
            r"Compute the Betti numbers of a smooth hypersurface of degree $d$ in $\\mathbb{P}^n$ using the Lefschetz hyperplane theorem.",
        ],
        "summary": "Deligne proved the Weil conjectures, establishing the deep connection between the topology of algebraic varieties over finite fields and the distribution of their rational points. His proof introduced new techniques in $\\ell$-adic cohomology and motivated the development of the theory of motives."
    },
    "chapter_1982_alain_connes": {
        "name": "Alain Connes", "year": "1982",
        "field": "Noncommutative Geometry, Operator Algebras",
        "prereqs": "Functional analysis (Banach algebras, $C^*$-algebras), basic measure theory, group theory.",
        "objectives": "Explain the classification of factors in von Neumann algebras; describe noncommutative geometry and its applications; understand the Connes trace theorem.",
        "exercises": [
            r"Show that the hyperfinite $\\text{II}_1$ factor is unique up to isomorphism.",
            r"Compute the von Neumann algebra $L(\\mathbb{F}_2)$ generated by the left regular representation of the free group on 2 generators.",
            "Verify that the Dixmier trace of a compact operator $T$ on $\\ell^2$ is given by $\\operatorname{Tr}_\\omega(T) = \\lim_{n \\to \\infty} \\frac{1}{\\log n} \\sum_{k=1}^n s_k(T)$.",
            r"Show that the noncommutative torus $A_\\theta$ is a $C^*$-algebra generated by two unitaries $U, V$ with $VU = e^{2\\pi i \\theta} UV$.",
        ],
        "summary": "Connes developed noncommutative geometry, creating a framework for studying ``noncommutative spaces'' through operator algebras. His classification of factors, the Connes trace theorem, and applications to number theory and physics (the Standard Model) established noncommutative geometry as a major branch of mathematics."
    },
    "chapter_1982_shing_tung_yau": {
        "name": "Shing-Tung Yau", "year": "1982",
        "field": "Differential Geometry, General Relativity",
        "prereqs": "Differential geometry (Riemannian manifolds, curvature), basic general relativity, partial differential equations (elliptic theory).",
        "objectives": "Explain the Calabi conjecture and its proof; describe the positive mass theorem; understand the role of geometric analysis in physics.",
        "exercises": [
            r"Verify that $\\mathbb{CP}^n$ admits a K\\'{a}hler-Einstein metric by computing the Ricci curvature.",
            r"Show that the Calabi-Yau metric on a K3 surface is Ricci-flat by checking the first Chern class vanishes.",
            r"Compute the scalar curvature of the standard sphere $S^n$ with the round metric.",
            r"Prove that a complete noncompact manifold with positive scalar curvature has a minimum at infinity.",
        ],
        "summary": "Yau proved the Calabi conjecture, showing that every K\\'{a}hler manifold with vanishing first Chern class admits a Ricci-flat metric. This result, with profound applications in string theory and mirror symmetry, together with the positive mass theorem, established the deep connections between differential geometry, PDEs, and mathematical physics."
    },
    "chapter_1982_william_thurston": {
        "name": "William Thurston", "year": "1982",
        "field": "3-Manifold Topology, Geometrization",
        "prereqs": "Algebraic topology (fundamental group, covering spaces), hyperbolic geometry (Fuchsian groups), basic differential geometry.",
        "objectives": "State the geometrization conjecture; explain the eight model geometries; describe the classification of foliations of 3-manifolds.",
        "exercises": [
            r"Show that $\\mathbb{H}^3$ is the unique complete simply connected 3-manifold of constant curvature $-1$.",
            r"Verify that the figure-eight knot complement admits a complete hyperbolic structure by computing the holonomy representation.",
            r"Construct a Reeb foliation of $S^3$ and verify it has a single compact leaf.",
            r"Prove that a closed 3-manifold with trivial fundamental group is homeomorphic to $S^3$ (Poincar\\'{e} conjecture in dimension 3, special case).",
        ],
        "summary": "Thurston proposed the geometrization conjecture, classifying all 3-manifolds in terms of eight model geometries. His work on hyperbolic 3-manifolds, foliation theory, and the mapping class group revolutionized low-dimensional topology and his vision ultimately guided Perelman's proof of the Poincar\\'{e} conjecture."
    },
    "chapter_1986_gerd_faltings": {
        "name": "Gerd Faltings", "year": "1986",
        "field": "Arithmetic Geometry, Number Theory",
        "prereqs": "Algebraic geometry (schemes, abelian varieties), number theory (elliptic curves, Galois representations), basic homological algebra.",
        "objectives": "Explain Faltings's proof of the Mordell conjecture; describe the Tate conjecture and its significance; understand the relationship between height functions and rational points.",
        "exercises": [
            r"Show that an abelian variety over a number field has finitely many rational points of bounded height.",
            r"Verify the Bogomolov conjecture for a set of algebraic points on an elliptic curve.",
            r"Compute the N\\'{e}ron-Tate height of a rational point on an elliptic curve over $\\mathbb{Q}$.",
            r"Prove that the Tate conjecture for abelian varieties over finite fields implies the Riemann hypothesis for their zeta functions.",
        ],
        "summary": "Faltings proved the Mordell conjecture (now Faltings's theorem): every curve of genus $g \\geq 2$ over a number field has only finitely many rational points. He also made fundamental contributions to the Tate conjecture, the Shafarevich conjecture, and $p$-adic Hodge theory."
    },
    "chapter_1986_michael_freedman": {
        "name": "Michael Freedman", "year": "1986",
        "field": "4-Manifold Topology",
        "prereqs": "Algebraic topology (intersection forms, characteristic classes), basic differential topology (handle decompositions).",
        "objectives": "State the topological classification theorem for simply connected 4-manifolds; explain the role of intersection forms; describe the relation to Donaldson's theorem.",
        "exercises": [
            r"Show that the intersection form of $\\mathbb{CP}^2$ is $\\begin{pmatrix} 1 \\end{pmatrix}$ and that of $\\overline{\\mathbb{CP}}^2$ is $\\begin{pmatrix} -1 \\end{pmatrix}$.",
            r"Verify that the $E_8$ lattice is positive definite and even, and classify all such forms of rank 8.",
            r"Prove that two simply connected 4-manifolds with the same intersection form are homeomorphic (Freedman's theorem).",
            r"Construct an exotic $\\mathbb{R}^4$ using Freedman's techniques.",
        ],
        "summary": "Freedman proved that simply connected 4-manifolds are classified up to homeomorphism by their intersection form and Kirby-Siebenmann invariant. This classification, together with Donaldson's differential-geometric results, revealed the extraordinary complexity of smooth 4-manifold topology and led to the discovery of exotic smooth structures on $\\mathbb{R}^4$."
    },
    "chapter_1986_simon_donaldson": {
        "name": "Simon Donaldson", "year": "1986",
        "field": "4-Manifold Topology, Gauge Theory",
        "prereqs": "Differential geometry (connections, curvature), algebraic topology (intersection forms, characteristic classes), basic PDE theory.",
        "objectives": "State Donaldson's theorem on intersection forms; explain the role of Yang-Mills instantons; describe the Donaldson invariants.",
        "exercises": [
            r"Show that the intersection form of a smooth, closed, simply connected 4-manifold must be diagonalizable over $\\mathbb{Z}$ if the manifold is smooth (Donaldson's theorem).",
            r"Compute the Donaldson invariant of $\\mathbb{CP}^2$.",
            r"Verify that $E_8$ cannot be realized by a smooth 4-manifold by applying Donaldson's theorem.",
            r"Construct the moduli space of anti-self-dual connections on a $U(1)$ bundle over a 4-manifold.",
        ],
        "summary": "Donaldson proved that the intersection form of a smooth, closed, simply connected 4-manifold must be diagonalizable, revealing a striking difference between smooth and topological 4-manifold theory. His invariants, derived from Yang-Mills gauge theory, provided the first tools for distinguishing smooth structures on 4-manifolds."
    },
    "chapter_1990_edward_witten": {
        "name": "Edward Witten", "year": "1990",
        "field": "Mathematical Physics, Topological Quantum Field Theory",
        "prereqs": "Quantum mechanics (Hilbert spaces, operators), differential geometry (connections, curvature), basic algebraic topology.",
        "objectives": "Explain Witten's interpretation of the Jones polynomial via Chern-Simons theory; describe topological quantum field theory; understand the relation between supersymmetry and Morse theory.",
        "exercises": [
            r"Verify that the Chern-Simons functional $\\operatorname{CS}(A) = \\frac{k}{4\\pi} \\int_M \\operatorname{tr}(A \\wedge dA + \\frac{2}{3} A \\wedge A \\wedge A)$ is gauge-invariant up to an integer multiple of $2\\pi i$.",
            r"Show that the Jones polynomial of the trefoil knot equals $-t^4 + t^3 + t$ by computing the Kauffman bracket.",
            r"Prove that the Witten genus of a string manifold is a modular form.",
            r"Verify that the path integral for Chern-Simons theory on $S^3$ gives the value $\\frac{1}{\\sqrt{k+2}} \\sin\\left(\\frac{\\pi}{k+2}\\right)$ for the unknot.",
        ],
        "summary": "Witten provided a physical interpretation of the Jones polynomial through Chern-Simons gauge theory, launching the field of topological quantum field theory (TQFT). His work connecting quantum field theory to knot theory, mirror symmetry, and quantum gravity established deep bridges between theoretical physics and pure mathematics."
    },
    "chapter_1990_shigefumi_mori": {
        "name": "Shigefumi Mori", "year": "1990",
        "field": "Algebraic Geometry, Birational Geometry",
        "prereqs": "Algebraic geometry (projective varieties, divisors, line bundles), basic commutative algebra (local rings, completion).",
        "objectives": "Explain the Mori fiber space program; describe the cone theorem; understand the classification of Fano varieties.",
        "exercises": [
            r"Show that the cone of effective curves on a smooth projective variety is generated by rational curves (Mori's bend-and-break).",
            r"Verify that $\\mathbb{CP}^n$ is a Mori fiber space by computing its anticanonical bundle.",
            r"Prove that a smooth projective variety with $K_X < 0$ contains a rational curve through every point.",
            r"Classify all smooth Fano 3-folds of Picard number 1.",
        ],
        "summary": "Mori proved the cone theorem, showing that the cone of curves on a projective variety is controlled by rational curves of small degree. His bend-and-break technique and the Mori fiber space program initiated the birational classification of algebraic varieties, analogous to the Enriques-Kodaira classification in dimension 2."
    },
    "chapter_1990_vaughan_jones": {
        "name": "Vaughan Jones", "year": "1990",
        "field": "Knot Theory, Von Neumann Algebras",
        "prereqs": "Elementary topology (knots, links, crossings), basic linear algebra (matrices, traces), introductory abstract algebra (groups, rings).",
        "objectives": "Define the Jones polynomial via the skein relation; explain its connection to the Temperley-Lieb algebra; describe applications to statistical mechanics.",
        "exercises": [
            r"Compute the Jones polynomial of the trefoil knot using the skein relation.",
            r"Verify that the Jones polynomial of the unknot is 1.",
            r"Show that the Jones polynomial distinguishes the trefoil knot from the unknot.",
            r"Compute the Jones polynomial of the Hopf link and verify it is different from two unlinked unknots.",
        ],
        "summary": "Jones discovered a new polynomial invariant of knots, the Jones polynomial, arising from his study of von Neumann algebras. This invariant revolutionized knot theory, revealed deep connections to statistical mechanics and quantum groups, and led to the discovery of the Jones index for subfactors."
    },
    "chapter_1990_vladimir_drinfeld": {
        "name": "Vladimir Drinfeld", "year": "1990",
        "field": "Number Theory, Quantum Groups",
        "prereqs": "Algebraic geometry (elliptic curves, algebraic groups), number theory (modular forms), abstract algebra (Hopf algebras).",
        "objectives": "Explain the Drinfeld module and its properties; describe quantum groups and their representations; understand the geometric Langlands correspondence.",
        "exercises": [
            r"Construct a Drinfeld module of rank 2 over $\\mathbb{F}_q[T]$ and compute its $j$-invariant.",
            r"Show that the Yang-Baxter equation is satisfied by the $R$-matrix of the quantum group $U_q(\\mathfrak{sl}_2)$.",
            r"Verify that the Carlitz module gives an analogue of the exponential function for function fields.",
            r"Prove that the category of representations of $U_q(\\mathfrak{sl}_2)$ is a braided monoidal category.",
        ],
        "summary": "Drinfeld introduced Drinfeld modules as characteristic $p$ analogues of elliptic curves, and developed the theory of quantum groups as deformations of universal enveloping algebras. His work on the geometric Langlands program and vertex algebras established profound connections between number theory, representation theory, and mathematical physics."
    },
    "chapter_1994_efim_zelmanov": {
        "name": "Efim Zelmanov", "year": "1994",
        "field": "Group Theory, Lie Algebras",
        "prereqs": "Abstract algebra (groups, Lie algebras, universal enveloping algebras), basic representation theory.",
        "objectives": "State the solution to the restricted Burnside problem; explain the role of Engel conditions in Lie algebra theory; describe the Kurosh problem for groups.",
        "exercises": [
            r"Verify that the free Lie algebra on 2 generators is infinite-dimensional.",
            r"Show that every finite-dimensional Lie algebra over a field of characteristic zero is a subalgebra of $\\mathfrak{gl}_n$ (Ado's theorem).",
            r"Prove that a Lie algebra satisfying the Engel condition is nilpotent.",
            r"Construct the universal enveloping algebra $U(\\mathfrak{sl}_2)$ and compute its center.",
        ],
        "summary": "Zelmanov solved the restricted Burnside problem, proving that finitely generated periodic groups of bounded exponent are finite. His proof introduced new techniques in Lie algebra theory and the theory of pro-$p$ groups, settling a problem that had been open for over 60 years and earning him the Fields Medal."
    },
    "chapter_1994_jean_bourgain": {
        "name": "Jean Bourgain", "year": "1994",
        "field": "Analysis, Additive Combinatorics, Number Theory",
        "prereqs": "Real analysis ($L^p$ spaces, Fourier analysis), basic harmonic analysis, combinatorics.",
        "objectives": "Explain the Kakeya conjecture and Bourgain's contributions; describe sum-product estimates; understand the applications to number theory.",
        "exercises": [
            r"Prove the sum-product estimate: $\\max(|A+A|, |A \\cdot A|) \\geq c|A|^{1+\\epsilon}$ for finite sets $A \\subset \\mathbb{F}_p$.",
            r"Show that the Kakeya set in $\\mathbb{R}^2$ has Hausdorff dimension at least 1.",
            r"Verify Bourgain's bound on the restriction theorem for the Fourier transform on the sphere.",
            r"Compute the $L^p$ norm of the directional maximal function for $p > 2$.",
        ],
        "summary": "Bourgain made fundamental contributions to harmonic analysis, additive combinatorics, and number theory. His work on the Kakeya conjecture, sum-product phenomena, and the restriction problem introduced powerful new techniques that bridged analysis and combinatorics, influencing areas from PDE theory to the distribution of primes."
    },
    "chapter_1994_jean_christophe_yoccoz": {
        "name": "Jean-Christophe Yoccoz", "year": "1994",
        "field": "Complex Dynamics, Number Theory",
        "prereqs": "Complex analysis (analytic functions, conformal maps), basic topology (continued fractions), introductory dynamics.",
        "objectives": "Explain the Yoccoz inequality and its role in Mandelbrot set connectivity; describe the classification of quadratic polynomials; understand small Mandelbrot components.",
        "exercises": [
            r"Show that the Mandelbrot set $\\mathcal{M}$ is connected by constructing a conformal isomorphism from the complement of $\\overline{\\mathbb{D}}$ to the complement of $\\mathcal{M}$.",
            r"Compute the external ray of the Mandelbrot set landing at the parameter $c = -1$.",
            r"Verify Yoccoz's inequality for the quadratic polynomial $f(z) = z^2 + c$ with $c$ in the main cardioid.",
            r"Prove that every small Mandelbrot component is a hyperbolic component.",
        ],
        "summary": "Yoccoz proved that every small Mandelbrot component is locally connected, settling a conjecture of Douady and Hubbard. His work on the classification of Julia sets and quadratic polynomials introduced the Yoccoz inequality and deepened the understanding of the parameter space of complex dynamics."
    },
    "chapter_1994_pierre_louis_lions": {
        "name": "Pierre-Louis Lions", "year": "1994",
        "field": "Partial Differential Equations, Applied Mathematics",
        "prereqs": "Real analysis ($L^p$ spaces, Sobolev spaces), basic PDE theory (elliptic and parabolic equations), calculus of variations.",
        "objectives": "Explain viscosity solutions and their role in nonlinear PDEs; describe the mean-field game framework; understand the Lasry-Lions monotonicity method.",
        "exercises": [
            r"Verify that the Hopf formula $u(x,t) = \\sup_y \\{g(y) - \\frac{|x-y|^2}{4t}\\}$ solves the heat equation with initial data $g$.",
            r"Show that the Hamilton-Jacobi equation $u_t + H(Du) = 0$ has a unique viscosity solution for convex $H$.",
            r"Prove that the Boltzmann equation preserves mass, momentum, and energy.",
            r"Compute the viscosity solution of the eikonal equation $|Du| = 1$ on the unit disc with Dirichlet boundary conditions.",
        ],
        "summary": "Lions developed the theory of viscosity solutions for nonlinear PDEs, providing a framework for well-posedness of equations arising in economics, physics, and geometry. His work on mean-field games, the Boltzmann equation, and the Lasry-Lions monotonicity method opened new directions in applied mathematics and mathematical economics."
    },
    "chapter_1998_curtis_mcmullen": {
        "name": "Curtis McMullen", "year": "1998",
        "field": "Hyperbolic 3-Manifolds, Complex Dynamics",
        "prereqs": "Hyperbolic geometry (Fuchsian and Kleinian groups), basic 3-manifold topology, complex analysis.",
        "objectives": "Explain the classification of Kleinian groups; describe the Bers conjecture and its resolution; understand the connection between 3-manifolds and complex dynamics.",
        "exercises": [
            r"Construct a quasi-Fuchsian group and verify that its limit set is a Jordan curve.",
            r"Compute the Hausdorff dimension of the limit set of a Schottky group.",
            r"Verify that the Riley slice in the space of Kleinian groups contains both punctured torus groups and handle groups.",
            r"Show that the Mandelbrot set is locally connected at the cusp parameter $c = 3/4$.",
        ],
        "summary": "McMullen resolved the Bers embedding conjecture and made fundamental contributions to hyperbolic 3-manifold topology, complex dynamics, and the study of Kleinian groups. His work on the classification of 3-manifolds, the ergodic theory of rational maps, and the geometry of the deformation space of Kleinian groups unified topology, dynamics, and geometry."
    },
    "chapter_1998_maxim_kontsevich": {
        "name": "Maxim Kontsevich", "year": "1998",
        "field": "Algebraic Geometry, Mathematical Physics, Topology",
        "prereqs": "Algebraic geometry (moduli spaces, deformation theory), topology (knot invariants, operads), basic mathematical physics (Feynman integrals).",
        "objectives": "Explain the Kontsevich formality theorem; describe the mirror symmetry conjecture for noncommutative geometry; understand the relation between Feynman integrals and knot invariants.",
        "exercises": [
            r"Verify the Kontsevich integral for the trefoil knot by computing the first few terms.",
            r"Show that the formality map $\\mathcal{U}: \\operatorname{Def}(A_\\bullet) \\to \\operatorname{Def}(\\operatorname{DG}_\\bullet)$ is a quasi-isomorphism for $A_\\bullet = C^\\infty(M)$.",
            r"Compute the intersection numbers $\\int_{\\overline{\\mathcal{M}}_{0,4}} \\psi_1^{a_1} \\cdots \\psi_n^{a_n}$ for small $n$.",
            r"Verify that the Kontsevich formality theorem implies deformation quantization of Poisson manifolds.",
        ],
        "summary": "Kontsevich proved the formality conjecture for deformation quantization of Poisson manifolds, establishing a deep connection between homological algebra and geometry. His work on intersection numbers on moduli spaces of curves, knot invariants, and mirror symmetry has influenced algebraic geometry, mathematical physics, and topology."
    },
    "chapter_1998_richard_borcherds": {
        "name": "Richard Borcherds", "year": "1998",
        "field": "Algebra, Vertex Algebras, Lie Algebras",
        "prereqs": "Abstract algebra (Lie algebras, associative algebras), basic representation theory, modular forms.",
        "objectives": "Explain the Moonshine conjecture and its proof via vertex algebras; describe the Monster group and its connection to modular functions; understand the Borcherds product formula.",
        "exercises": [
            r"Verify that the $j$-function $j(\\tau) = q^{-1} + 744 + 196884q + \\cdots$ is a modular function of weight 0.",
            r"Show that $196884 = 196883 + 1$, where 196883 is the dimension of the smallest non-trivial representation of the Monster group.",
            r"Construct the Moonshine vertex algebra $V^{\\natural}$ and compute its graded character.",
            r"Prove that the Conway-Norton conjecture follows from the moonshine module construction.",
        ],
        "summary": "Borcherds proved the Moonshine conjecture, establishing a deep connection between the Monster sporadic group and modular functions through the theory of vertex algebras. His introduction of Borcherds algebras (generalized Kac-Moody algebras) and his work on the Leech lattice and the Monster group revealed unexpected bridges between algebra, number theory, and mathematical physics."
    },
    "chapter_1998_timothy_gowers": {
        "name": "Timothy Gowers", "year": "1998",
        "field": "Combinatorics, Functional Analysis",
        "prereqs": "Basic combinatorics (pigeonhole principle, Ramsey theory), functional analysis (Banach spaces, Baire category theorem).",
        "objectives": "Explain the Szemer\\'{e}di regularity lemma and its applications; describe the proof of the density Hales-Jewett theorem; understand the dichotomy between structured and random in combinatorics.",
        "exercises": [
            r"Verify the Szemer\\'{e}di regularity lemma for a complete bipartite graph $K_{n,n}$.",
            r"Prove Roth's theorem: every subset of $\\{1, \\ldots, N\\}$ with density $> 2/\\log \\log N$ contains a 3-term arithmetic progression.",
            r"Construct a set of positive density in $\\mathbb{Z}$ containing no 3-term arithmetic progression (Behrend's construction).",
            r"Show that the density Hales-Jewett theorem implies Szemer\\'{e}di's theorem.",
        ],
        "summary": "Gowers proved that every set of positive upper density in $\\mathbb{Z}$ contains arbitrarily long arithmetic progressions (Szemer\\'{e}di's theorem) with quantitative bounds. His work introduced the Gowers norms, the regularity lemma for hypergraphs, and the Polymath project, establishing new paradigms for collaborative mathematical research."
    },
    "chapter_2002_laurent_lafforgue": {
        "name": "Laurent Lafforgue", "year": "2002",
        "field": "Number Theory, Automorphic Forms",
        "prereqs": "Algebraic geometry (stacks, moduli spaces), number theory (automorphic forms, L-functions), basic representation theory.",
        "objectives": "Explain Lafforgue's proof of the Langlands correspondence for function fields; describe the moduli space of shtukas; understand the role of étale cohomology.",
        "exercises": [
            r"Show that the number of points on an elliptic curve over $\\mathbb{F}_q$ can be expressed as $q + 1 - a_q$ where $a_q = \\alpha + \\bar{\\alpha}$ with $|\\alpha| = \\sqrt{q}$.",
            r"Verify that the Langlands correspondence for $\\operatorname{GL}_2$ over $\\mathbb{F}_q(T)$ is a bijection between cuspidal automorphic representations and irreducible 2-dimensional Galois representations.",
            r"Compute the L-function of a modular form of weight 2 and level 1.",
            r"Prove that the Hecke operators $T_p$ commute and are simultaneously diagonalizable on the space of cusp forms.",
        ],
        "summary": "Lafforgue proved the Langlands correspondence for function fields, establishing a deep bijection between automorphic representations of $\\operatorname{GL}_n$ over function fields and Galois representations. His construction of the moduli space of shtukas and his use of étale cohomology provided the geometric framework for this fundamental result in number theory."
    },
    "chapter_2002_vladimir_voevodsky": {
        "name": "Vladimir Voevodsky", "year": "2002",
        "field": "Algebraic Geometry, Homotopy Theory",
        "prereqs": "Algebraic geometry (motives, cohomology), homotopy theory (model categories, spectra), basic category theory.",
        "objectives": "Explain the univalence axiom and its implications; describe motivic cohomology; understand the proof of the Milnor conjecture.",
        "exercises": [
            r"Show that the Milnor K-theory of a field surjects onto its Galois cohomology with $\\mathbb{Z}/2$ coefficients.",
            r"Verify the Bloch-Kato conjecture for $n = 1$: $K_n^M(F)/2 \\cong H^n_{\\text{\\'{e}t}}(F, \\mathbb{Z}/2)$.",
            r"Construct the motivic stable homotopy category and verify it has the correct notion of weak equivalences.",
            r"Prove that the univalence axiom implies functional extensionality in Homotopy Type Theory.",
        ],
        "summary": "Voevodsky developed motivic cohomology and the theory of mixed motives, proving the Milnor conjecture and the Bloch-Kato conjecture. His work on Homotopy Type Theory and the univalence axiom created a new foundation for mathematics based on homotopy theory, with profound implications for computer-verified proofs."
    },
    "chapter_2006_andrei_okounkov": {
        "name": "Andrei Okounkov", "year": "2006",
        "field": "Representation Theory, Mathematical Physics",
        "prereqs": "Representation theory (symmetric groups, infinite-dimensional algebras), basic probability theory, complex analysis.",
        "objectives": "Explain the connection between random matrices and number theory; describe the representation theory of symmetric groups; understand the Borodin-Okounkov formula.",
        "exercises": [
            r"Compute the character table of the symmetric group $S_4$.",
            r"Verify the Weyl dimension formula for the irreducible representation of $\\mathfrak{sl}_2$ with highest weight $n$.",
            r"Show that the Plancherel measure on partitions of $n$ converges to the semicircle distribution as $n \\to \\infty$.",
            r"Compute the correlation kernel for the discrete sine kernel and verify it reproduces the GUE distribution.",
        ],
        "summary": "Okounkov established deep connections between representation theory, mathematical physics, and probability. His work on random matrices, the representation theory of symmetric groups, and the connection to the Riemann zeta function revealed unexpected links between algebra, analysis, and number theory."
    },
    "chapter_2006_grigori_perelman_declined": {
        "name": "Grigori Perelman", "year": "2006",
        "field": "Riemannian Geometry, Geometric Analysis",
        "prereqs": "Riemannian geometry (curvature, Ricci flow), PDE theory (parabolic equations), basic 3-manifold topology.",
        "objectives": "Explain the Ricci flow with surgery and its role in proving the Poincar\\'{e} conjecture; describe the use of entropy monotonicity; understand Perelman's no-local-collapsing theorem.",
        "exercises": [
            r"Verify that the Ricci flow equation $\\partial_t g_{ij} = -2R_{ij}$ preserves the volume form when the scalar curvature is constant.",
            r"Show that the Perelman $\\mathcal{W}$-functional is monotone under the Ricci flow.",
            r"Compute the evolution of the scalar curvature under Ricci flow for the round sphere $S^n$.",
            r"Prove that the Ricci flow on a 2-sphere with positive curvature is smooth for all time.",
        ],
        "summary": "Perelman proved the Poincar\\'{e} conjecture and Thurston's geometrization conjecture using Ricci flow with surgery. His introduction of the $\\mathcal{W}$-functional, the no-local-collapsing theorem, and the entropy monotonicity formula resolved the most important open problem in 3-manifold topology, though he declined the Fields Medal."
    },
    "chapter_2006_terence_tao": {
        "name": "Terence Tao", "year": "2006",
        "field": "Harmonic Analysis, PDEs, Additive Combinatorics, Number Theory",
        "prereqs": "Real analysis ($L^p$ spaces, Fourier analysis), basic PDE theory (well-posedness), introductory additive combinatorics.",
        "objectives": "Explain the Green-Tao theorem on primes in arithmetic progressions; describe the Kakeya conjecture and Tao's contributions; understand the transference principle.",
        "exercises": [
            r"Verify that the set of primes has positive upper density in the set of odd numbers (a heuristic argument).",
            r"Prove that every subset of $\\{1, \\ldots, N\\}$ of size $\\geq cN / \\log \\log N$ contains a 3-term arithmetic progression.",
            r"Show that the Kakeya maximal function is bounded on $L^p(\\mathbb{R}^2)$ for $p > 2$.",
            r"Compute the Gowers norm $\\|f\\|_{U^2}$ for a quadratic phase function $f(n) = e^{2\\pi i \\alpha n^2}$.",
        ],
        "summary": "Tao proved the Green-Tao theorem that the primes contain arbitrarily long arithmetic progressions, introduced powerful new techniques in additive combinatorics (the transference principle, Gowers norms), and made fundamental contributions to harmonic analysis, PDEs, and random matrix theory. His breadth and depth of work across multiple areas of mathematics is extraordinary."
    },
    "chapter_2006_wendelin_werner": {
        "name": "Wendelin Werner", "year": "2006",
        "field": "Probability, Conformal Invariance",
        "prereqs": "Probability theory (Brownian motion, Markov chains), basic complex analysis (conformal maps), introductory stochastic processes.",
        "objectives": "Explain Schramm-Loewner evolution and its parameter $\\kappa$; describe the relationship between SLE and conformal invariance; understand the Brownian intersection exponents.",
        "exercises": [
            r"Verify that SLE$_6$ is the scaling limit of the critical percolation exploration process.",
            r"Compute the Hausdorff dimension of the SLE$_\\kappa$ trace for $\\kappa < 8$.",
            r"Show that the SLE$_\\kappa$ curve is simple for $\\kappa \\leq 4$ and self-intersecting for $\\kappa > 4$.",
            r"Prove that the intersection exponent for two Brownian paths in $\\mathbb{R}^2$ is $1/3$.",
        ],
        "summary": "Werner proved that the scaling limit of critical percolation on the triangular lattice is conformally invariant, and developed the theory of Schramm-Loewner evolution (SLE) as a framework for understanding conformally invariant random curves. His work on Brownian intersection exponents and the Brownian loop soup connected probability theory to conformal field theory."
    },
    "chapter_2010_cedric_villani": {
        "name": "C\\'{e}dric Villani", "year": "2010",
        "field": "Optimal Transport, PDEs, Mathematical Physics",
        "prereqs": "Measure theory (probability measures, weak convergence), basic PDE theory (transport equations), functional analysis.",
        "objectives": "Explain the optimal transport framework and its applications; describe the Landau damping result; understand the entropy method for PDEs.",
        "exercises": [
            r"Show that the Wasserstein distance $W_1(\\mu, \\nu)$ metrizes weak convergence of probability measures on a compact space.",
            r"Verify the Brenier theorem: the optimal transport map from a Gaussian to any other measure is the gradient of a convex function.",
            r"Compute the entropy production for the Boltzmann equation in the relaxation-time approximation.",
            r"Prove the Talagrand transportation inequality for the Gaussian measure.",
        ],
        "summary": "Villani developed the theory of optimal transport and its applications to PDEs, Riemannian geometry, and mathematical physics. His work on Landau damping in plasma physics and the entropy method for dissipation inequalities established deep connections between analysis, probability, and geometry."
    },
    "chapter_2010_elon_lindenstrauss": {
        "name": "Elon Lindenstrauss", "year": "2010",
        "field": "Ergodic Theory, Number Theory",
        "prereqs": "Ergodic theory (measure-preserving transformations, ergodic theorems), basic number theory (Diophantine approximation).",
        "objectives": "Explain the ergodic proof of the arithmetic Bogomolov conjecture; describe the Littlewood conjecture and its resolution; understand the connection between dynamics and number theory.",
        "exercises": [
            r"Prove the Birkhoff ergodic theorem: for a measure-preserving transformation $T$ and $f \\in L^1$, $\\frac{1}{n} \\sum_{k=0}^{n-1} f(T^k x) \\to \\int f \\, d\\mu$ a.e.",
            r"Show that the geodesic flow on a hyperbolic surface is ergodic.",
            r"Verify that the Littlewood conjecture $\\liminf_{n \\to \\infty} n \\|n\\alpha\\| \\|n\\beta\\| = 0$ holds for almost every pair $(\\alpha, \\beta)$.",
            r"Compute the entropy of the geodesic flow on a compact surface of constant negative curvature.",
        ],
        "summary": "Lindenstrauss made fundamental contributions to ergodic theory and its applications to number theory. His ergodic proof of the arithmetic Bogomolov conjecture and his work on the Littlewood conjecture revealed deep connections between dynamical systems and Diophantine approximation, and his development of measure rigidity advanced the field of homogeneous dynamics."
    },
    "chapter_2010_ngo_bao_chau": {
        "name": "Ng\\{o} Bao Ch\\'{a}u", "year": "2010",
        "field": "Number Theory, Algebraic Geometry",
        "prereqs": "Algebraic geometry (stacks, intersection theory), number theory (automorphic forms, L-functions), representation theory.",
        "objectives": "Explain the fundamental lemma and its proof; describe the trace formula and its role in the Langlands program; understand the geometric interpretation of orbital integrals.",
        "exercises": [
            r"Verify the fundamental lemma for $\\operatorname{GL}_2$ by computing the orbital integrals explicitly.",
            r"Show that the trace formula equates a sum over orbital integrals to a sum over character values.",
            r"Compute the stable orbital integral for the identity coset in $\\operatorname{GL}_n$.",
            r"Prove that the fundamental lemma for $\\operatorname{GL}_n$ follows from the case of $\\operatorname{GL}_2$ using the endoscopic classification.",
        ],
        "summary": "Ng\\{o} proved the fundamental lemma, a key conjecture in the Langlands program connecting automorphic forms on different groups. His geometric proof using the Hitchin fibration introduced new techniques from algebraic geometry into number theory, resolving a problem that had been open for over 30 years."
    },
    "chapter_2010_stanislav_smirnov": {
        "name": "Stanislav Smirnov", "year": "2010",
        "field": "Probability, Mathematical Physics, Complex Analysis",
        "prereqs": "Probability theory (random walks, Markov chains), complex analysis (Schramm-Loewner evolution), basic statistical mechanics.",
        "objectives": "Explain the conformal invariance of critical percolation; describe the discrete complex analysis approach; understand the relationship between lattice models and conformal field theory.",
        "exercises": [
            r"Show that the harmonic measure on the boundary of a simply connected domain is conformally invariant.",
            r"Verify that the discrete Green's function on $\\mathbb{Z}^2$ converges to the continuous Green's function as the mesh size goes to 0.",
            r"Compute the crossing probability for critical percolation on a rectangle using Smirnov's formula.",
            r"Prove that the scaling limit of critical percolation interfaces is SLE$_6$.",
        ],
        "summary": "Smirnov proved the conformal invariance of critical planar percolation, establishing that the scaling limit of critical percolation on the square lattice is conformally invariant. His discrete complex analysis approach and his work on the Ising model provided the mathematical foundations for understanding conformally invariant lattice models."
    },
    "chapter_2014_artur_avila": {
        "name": "Artur Avila", "year": "2014",
        "field": "Dynamical Systems, Number Theory, Spectral Theory",
        "prereqs": "Dynamical systems (iteration of circle maps, renormalization), number theory (continued fractions), basic functional analysis.",
        "objectives": "Explain the solution of the Ten Martini Problem; describe the almost Mathieu operator and its spectral properties; understand the role of renormalization in dynamics.",
        "exercises": [
            r"Verify that the almost Mathieu operator $H_{\\lambda, \\theta} = \\Delta + 2\\lambda \\cos(2\\pi(n+\\theta))$ has pure point spectrum for $\\lambda > 2$.",
            r"Show that the rotation number of the Fibonacci circle map is the golden ratio.",
            r"Compute the Lyapunov exponent of the almost Mathieu operator for $\\lambda = 2$.",
            r"Prove that the set of parameters for which the almost Mathieu operator has absolutely continuous spectrum has Hausdorff dimension 1.",
        ],
        "summary": "Avila solved the Ten Martini Problem, proving that the spectrum of the almost Mathieu operator is a Cantor set for all irrational parameters. His work on the almost Mathieu operator, the golden ratio dynamics, and the one-dimensional Schr\\\"{o}dinger operators established new techniques in dynamical systems and spectral theory."
    },
    "chapter_2014_manjul_bhargava": {
        "name": "Manjul Bhargava", "year": "2014",
        "field": "Number Theory, Algebraic Geometry",
        "prereqs": "Elementary number theory (quadratic forms, class numbers), abstract algebra (rings of integers, group actions), basic algebraic geometry.",
        "objectives": "Explain higher composition laws and the Bhargava boxes; describe the average size of 2-Selmer groups; understand the connection between number fields and geometry.",
        "exercises": [
            r"Compute the 3-class group of the field $\\mathbb{Q}(\\sqrt{-23})$ and verify Gauss's class number problem for this case.",
            r"Show that the number of $\\mathbb{Z}$-isomorphism classes of quadratic rings of discriminant $D$ is finite.",
            r"Verify Bhargava's formula: the number of $\\mathbb{Z}$-lattices in $\\mathbb{Q}^n$ of index $N$ is $\\prod_{p|N} \\frac{p^n-1}{p-1}$.",
            r"Prove that the average number of 2-Selmer elements of elliptic curves over $\\mathbb{Q}$ is bounded (Bhargava-Shankar theorem).",
        ],
        "summary": "Bhargava invented higher composition laws, providing a new framework for counting number fields and solving classical problems in number theory. His proof that the average rank of elliptic curves over $\\mathbb{Q}$ is bounded (with Shankar) is a major advance toward the Birch and Swinnerton-Dyer conjecture, and his work on the geometric composition law connects number theory to algebraic geometry."
    },
    "chapter_2014_martin_hairer": {
        "name": "Martin Hairer", "year": "2014",
        "field": "Stochastic PDEs, Probability Theory",
        "prereqs": "Probability theory (Brownian motion, stochastic processes), PDE theory (heat equation, Sobolev spaces), basic functional analysis.",
        "objectives": "Explain regularity structures and their role in stochastic PDEs; describe the KPZ equation and its solutions; understand the theory of rough paths.",
        "exercises": [
            r"Verify that the stochastic heat equation $\\partial_t u = \\Delta u + \\xi$ with space-time white noise $\\xi$ has a unique mild solution.",
            r"Show that the Burgers equation $\\partial_t u = \\partial_x^2 u + u \\partial_x u$ develops shocks in finite time.",
            r"Compute the one-point function of the KPZ equation at stationarity.",
            r"Prove that the KPZ fixed point is a Markov process with explicit transition probabilities.",
        ],
        "summary": "Hairer developed the theory of regularity structures, providing a systematic framework for solving stochastic partial differential equations. His work on the KPZ equation, the Burgers equation, and the theory of rough paths established new foundations for the analysis of nonlinear stochastic PDEs and their scaling limits."
    },
    "chapter_2014_maryam_mirzakhani": {
        "name": "Maryam Mirzakhani", "year": "2014",
        "field": "Hyperbolic Geometry, Dynamics, Teichm\\\"{u}ller Theory",
        "prereqs": "Hyperbolic geometry (geodesics, Fenchel-Nielsen coordinates), basic Teichm\\\"{u}ller theory, ergodic theory.",
        "objectives": "Explain Mirzakhani's recurrence theorem for the geodesic flow; describe the counting of simple closed curves; understand the volume recursion for moduli spaces.",
        "exercises": [
            r"Show that the Fenchel-Nielsen coordinates give a global parametrization of Teichmüller space.",
            r"Verify the Mirzakhani volume recursion formula for $\\mathcal{M}_{0,4}$.",
            r"Compute the length spectrum of a hyperbolic surface of genus 2.",
            r"Prove that the mapping class group acts properly discontinuously on Teichmüller space.",
        ],
        "summary": "Mirzakhani proved the ergodicity of the Teichm\\\"{u}ller geodesic flow on moduli spaces of hyperbolic surfaces and established the volume recursion formula for moduli spaces. Her work on counting simple closed curves on surfaces and the dynamics of the mapping class group unified Teichm\\\"{u}ller theory, dynamics, and geometry."
    },
    "chapter_2018_akshay_venkatesh": {
        "name": "Akshay Venkatesh", "year": "2018",
        "field": "Number Theory, Automorphic Representations, Topology",
        "prereqs": "Number theory (automorphic forms, L-functions), algebraic topology (cohomology of arithmetic groups), basic representation theory.",
        "objectives": "Explain the trace formula and its applications to equidistribution; describe the work on torsion in cohomology; understand the connection between number theory and topology.",
        "exercises": [
            r"Verify the Weyl equidistribution theorem for the torus $\\mathbb{R}^n / \\mathbb{Z}^n$.",
            r"Show that the number of representations of an integer as a sum of four squares is related to the Dedekind zeta function.",
            r"Compute the cohomology of the arithmetic group $\\operatorname{SL}_2(\\mathbb{Z})$.",
            r"Prove that the torsion in $H_1(\\Gamma, \\mathbb{Z})$ for a congruence subgroup $\\Gamma \\subset \\operatorname{SL}_2(\\mathbb{Z})$ grows exponentially with the level.",
        ],
        "summary": "Venkatesh made deep contributions to the interplay between number theory, automorphic representations, and topology. His work on equidistribution, torsion cohomology, and the Gan-Gross-Prasad conjecture revealed new connections between the arithmetic of number fields and the topology of locally symmetric spaces."
    },
    "chapter_2018_alessio_figalli": {
        "name": "Alessio Figalli", "year": "2018",
        "field": "Optimal Transport, PDEs, Geometric Measure Theory",
        "prereqs": "Optimal transport (Wasserstein distance, Monge problem), PDE theory (elliptic equations), basic measure theory.",
        "objectives": "Explain the regularity of optimal transport maps; describe the free boundary problems; understand the connection between transport and geometry.",
        "exercises": [
            r"Prove that the optimal transport map for the quadratic cost is the gradient of a convex function (Brenier's theorem).",
            r"Show that the Monge-Amp\\`{e}re equation $\\det(D^2 u) = f$ has a unique solution under appropriate conditions.",
            r"Verify that the Wasserstein distance $W_2(\\mu, \\nu)$ is finite for two compactly supported probability measures on $\\mathbb{R}^n$.",
            r"Compute the optimal transport map between two Gaussian measures on $\\mathbb{R}^n$.",
        ],
        "summary": "Figalli made fundamental contributions to optimal transport theory, proving regularity results for optimal transport maps and establishing connections with the Monge-Amp\\`{e}re equation. His work on free boundary problems, transport inequalities, and applications to geometry and PDEs established new foundations for the field of optimal transport."
    },
    "chapter_2018_caucher_birkar": {
        "name": "Caucher Birkar", "year": "2018",
        "field": "Algebraic Geometry, Birational Geometry",
        "prereqs": "Algebraic geometry (projective varieties, divisors, linear systems), basic commutative algebra (local rings, completion).",
        "objectives": "Explain the boundedness of Fano varieties; describe the minimal model program in higher dimensions; understand the connection between birational geometry and number theory.",
        "exercises": [
            r"Show that the anticanonical divisor of $\\mathbb{P}^n$ is ample and compute its self-intersection.",
            r"Verify that the cone of curves on a Fano variety is generated by rational curves of bounded degree.",
            r"Prove that the moduli space of Fano varieties of bounded index and dimension is quasi-projective.",
            r"Classify all smooth Fano 3-folds of Picard number 1 (sketch Birkar's approach).",
        ],
        "summary": "Birkar proved the boundedness of Fano varieties, showing that the moduli space of Fano varieties of fixed dimension and index is a bounded family. His work on the minimal model program, the existence of minimal models, and the classification of algebraic varieties advanced the higher-dimensional birational classification program."
    },
    "chapter_2018_peter_scholze": {
        "name": "Peter Scholze", "year": "2018",
        "field": "Arithmetic Algebraic Geometry, p-adic Geometry",
        "prereqs": "Algebraic geometry (schemes, cohomology), number theory (p-adic numbers, local fields), basic representation theory.",
        "objectives": "Explain perfectoid spaces and the tilting correspondence; describe p-adic Hodge theory; understand the p-adic Langlands correspondence.",
        "exercises": [
            r"Show that the tilt of $\\mathbb{Q}_p(p^{1/p^\\infty})$ is $\\mathbb{F}_p((t))$.",
            r"Verify that the perfectoid ring $\\mathbb{Z}_p[[\\varprojlim_{x \\mapsto x^p} \\mathbb{Z}_p]]$ is a perfectoid ring.",
            r"Compute the Hodge-Tate weights of the Tate module of an elliptic curve over $\\mathbb{Q}_p$.",
            r"Prove that the pro-\\'{e}tale site of a perfectoid space is equivalent to the pro-finite-\\'{e}tale site.",
        ],
        "summary": "Scholze created perfectoid spaces, providing a bridge between characteristic 0 and characteristic $p$ in algebraic geometry. His work on p-adic Hodge theory, the p-adic Langlands correspondence, and condensed mathematics has reshaped arithmetic geometry and established new foundations for studying $p$-adic fields and their geometric applications."
    },
    "chapter_2022_hugo_duminil_copin": {
        "name": "Hugo Duminil-Copin", "year": "2022",
        "field": "Probability, Statistical Mechanics",
        "prereqs": "Probability theory (random walks, Markov chains), basic statistical mechanics (Ising model, Potts model), measure theory.",
        "objectives": "Explain the sharp phase transition of the Ising model; describe the self-avoiding walk and its critical exponent; understand the relationship between correlation functions and critical phenomena.",
        "exercises": [
            r"Compute the magnetization of the 2D Ising model below the critical temperature using Onsager's solution.",
            r"Show that the correlation length of the Ising model diverges at the critical temperature.",
            r"Verify the sharp threshold theorem: the probability of a connection in critical percolation decays polynomially.",
            r"Prove that the expected number of self-avoiding walks of length $n$ on $\\mathbb{Z}^d$ grows like $\\mu^n n^{\\gamma - 1}$ for some $\\mu > 1$ and $\\gamma \\geq 1$.",
        ],
        "summary": "Duminil-Copin proved the sharp phase transition for the Ising model, establishing the exact critical exponents and the sharp threshold behavior. His work on self-avoiding walks, the random-cluster model, and the relationship between correlation functions and critical phenomena advanced the mathematical understanding of phase transitions in statistical mechanics."
    },
    "chapter_2022_james_maynard": {
        "name": "James Maynard", "year": "2022",
        "field": "Analytic Number Theory, Additive Combinatorics",
        "prereqs": "Elementary number theory (primes, arithmetic progressions), basic analytic number theory (sieve methods, exponential sums).",
        "objectives": "Explain the Maynard-Tao theorem on bounded gaps between primes; describe the multidimensional sieve; understand the Goldston-Pintz-Yıldırım (GPY) method.",
        "exercises": [
            r"Verify that the GPY method gives $\\liminf_{n \\to \\infty} (p_{n+1} - p_n) \\leq 6$ under the Elliott-Halberstam conjecture.",
            r"Show that the Maynard weights improve the GPY bound from 6 to 24 unconditionally.",
            r"Compute the quantity $\\theta$ in the GPY method that controls the density of primes needed.",
            r"Prove that the Bombieri-Vinogradov theorem implies the GPY method gives bounded gaps between primes.",
        ],
        "summary": "Maynard proved that there are infinitely many bounded gaps between primes, establishing that $\\liminf_{n \\to \\infty} (p_{n+1} - p_n) \\leq 600$. His multidimensional refinement of the GPY method, combined with the Elliott-Halberstam conjecture, reduced this to 12, and his techniques have further applications to Diophantine approximation and the distribution of primes."
    },
    "chapter_2022_june_huh": {
        "name": "June Huh", "year": "2022",
        "field": "Combinatorics, Algebraic Geometry",
        "prereqs": "Combinatorics (chromatic polynomial, matroids), basic algebraic geometry (cohomology, Hodge theory), linear algebra.",
        "objectives": "Explain the Heron-Rota-Welsh conjecture and its proof; describe the Chow ring of a matroid; understand log-concavity of chromatic polynomials.",
        "exercises": [
            r"Compute the chromatic polynomial of the complete graph $K_4$ and verify it has alternating coefficients.",
            r"Show that the chromatic polynomial of any graph satisfies $|a_i|^2 \\geq |a_{i-1}| \\cdot |a_{i+1}|$ (log-concavity) for the special case of the cycle graph $C_n$.",
            r"Verify the log-concavity of the coefficients of the characteristic polynomial of the uniform matroid $U_{2,4}$.",
            r"Construct the Chow ring of a matroid and verify the hard Lefschetz property for a simple example.",
        ],
        "summary": "Huh proved the Heron-Rota-Welsh conjecture, establishing that the coefficients of the characteristic polynomial of any matroid form a log-concave sequence. His construction of a Hodge theory for matroids, using the Chow ring of a matroid, introduced techniques from algebraic geometry into combinatorics and resolved a conjecture that had been open for over 50 years."
    },
    "chapter_2022_maryna_viazovska": {
        "name": "Maryna Viazovska", "year": "2022",
        "field": "Number Theory, Discrete Geometry",
        "prereqs": "Fourier analysis (Fourier transform, convolution), basic number theory (lattices, quadratic forms), linear algebra.",
        "objectives": "Explain the E8 lattice and its optimality; describe the sphere packing problem and its history; understand the role of modular forms in the proof.",
        "exercises": [
            r"Compute the theta function of the E8 lattice and verify it is a modular form of weight 4.",
            r"Show that the density of the E8 lattice packing is $\\pi^4 / 384 \\approx 0.2537$.",
            r"Verify that the Leech lattice has kissing number 196560 by computing its theta function.",
            r"Prove that the E8 lattice is the unique even unimodular lattice in $\\mathbb{R}^8$.",
        ],
        "summary": "Viazovska proved that the E8 lattice gives the densest sphere packing in 8 dimensions, and (with collaborators) that the Leech lattice is optimal in 24 dimensions. Her proof uses modular forms and the theory of lattices to construct explicit linear programming bounds, settling the sphere packing problem in these dimensions after centuries of effort."
    },
}

def find_chapter_file(chapter_key):
    """Find the actual file path for a chapter key."""
    path = f"chapters/{chapter_key}.tex"
    if os.path.exists(path):
        return path
    return None

def find_first_section_line(lines):
    """Find the line number of the first \\section."""
    for i, line in enumerate(lines):
        if re.match(r'\\section\{', line.strip()):
            return i
    return None

def find_references_line(lines):
    """Find the line number of the References section."""
    # First try: standard \section{References...} pattern
    for i, line in enumerate(lines):
        if 'References and Further' in line and '\\section' in line:
            return i
    # Second try: just \section{References} pattern
    for i, line in enumerate(lines):
        if '\\section{References' in line:
            return i
    # Third try: markdown-style ## References inside longtable
    for i, line in enumerate(lines):
        if '## ' in line and 'References' in line:
            return i
    return None

def find_references_end(lines, ref_start):
    """Find the end of the references section (last non-empty line)."""
    last_content = ref_start
    for i in range(ref_start + 1, len(lines)):
        if lines[i].strip():
            last_content = i
    return last_content

def add_pedagogy(filepath, data):
    """Add prerequisites, learning objectives, exercises, and summary to a chapter."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Skip if already processed (has exercises)
    content = ''.join(lines)
    if '\\begin{exercise}' in content or '\\section*{Exercises}' in content:
        print(f"  SKIP: Already has pedagogy content")
        return False
    
    # Find insertion points
    first_section = find_first_section_line(lines)
    ref_section = find_references_line(lines)
    
    if first_section is None:
        print(f"  WARNING: No section found in {filepath}")
        return False
    
    # Build new content
    new_lines = list(lines)
    offset = 0
    
    # 1. Add prerequisites and learning objectives after the first section heading
    # Find the end of the first section's first paragraph
    insert_after = first_section + 1
    while insert_after < len(new_lines) and new_lines[insert_after].strip() == '':
        insert_after += 1
    # Skip past the first paragraph
    while insert_after < len(new_lines) and new_lines[insert_after].strip() != '':
        insert_after += 1
    
    pedagogy_block = [
        '\n',
        f'\\begin{{prereqs}} {data["prereqs"]} \\end{{prereqs}}\n',
        '\n',
        f'\\begin{{objectives}} {data["objectives"]} \\end{{objectives}}\n',
        '\n',
    ]
    
    for j, line in enumerate(pedagogy_block):
        new_lines.insert(insert_after + j, line)
    offset += len(pedagogy_block)
    
    # 2. Find references section (adjusted for offset)
    ref_section = find_references_line(new_lines)
    
    # If no references section found, try inserting before last ~20 lines
    if ref_section is None:
        # Look for "End of report" or end of longtable
        for i in range(len(new_lines) - 1, max(len(new_lines) - 50, 0), -1):
            if 'End of report' in new_lines[i] or '\\end{longtable}' in new_lines[i]:
                ref_section = i
                break
        if ref_section is None:
            ref_section = len(new_lines) - 10  # fallback: near end
    
    # 3. Add exercises before references
    exercises_block = [
        '\\begin{center}\\rule{0.5\\linewidth}{0.5pt}\\end{center}\n',
        '\n',
        '\\section*{Exercises}\n',
        '\\addcontentsline{toc}{section}{Exercises}\n',
        '\n',
    ]
    
    for j, ex in enumerate(data["exercises"], 1):
        exercises_block.append(f'\\begin{{exercise}} {ex} \\end{{exercise}}\n')
        exercises_block.append('\n')
    
    # 4. Add chapter summary
    exercises_block.append('\\begin{center}\\rule{0.5\\linewidth}{0.5pt}\\end{center}\n')
    exercises_block.append('\n')
    exercises_block.append('\\section*{Summary}\n')
    exercises_block.append('\\addcontentsline{toc}{section}{Summary}\n')
    exercises_block.append('\n')
    exercises_block.append(f'{data["summary"]}\n')
    exercises_block.append('\n')
    
    for j, line in enumerate(exercises_block):
        new_lines.insert(ref_section + j, line)
    
    with open(filepath, 'w') as f:
        f.writelines(new_lines)
    
    return True

def main():
    base_dir = "chapters"
    success = 0
    failed = 0
    
    for chapter_key, data in CHAPTER_DATA.items():
        filepath = find_chapter_file(chapter_key)
        if filepath is None:
            print(f"  SKIP: {chapter_key} - file not found")
            failed += 1
            continue
        
        print(f"Processing: {chapter_key} ({data['name']}, {data['year']})")
        if add_pedagogy(filepath, data):
            success += 1
        else:
            failed += 1
    
    print(f"\nDone: {success} succeeded, {failed} failed")

if __name__ == "__main__":
    main()
