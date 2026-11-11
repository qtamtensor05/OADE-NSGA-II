# DTLZ1–4 benchmark results

dtlz_benchmark: RNSGA2 has 360/360 valid records, 30 paired seeds per configuration and 20,000 recorded evaluations per run including setup. Against RNSGA2, OADE outcomes are 21 wins, 3 comparisons with no detected difference and 0 losses, within the stated suite-by-metric Holm families.

Thirty paired seeds (42–71), population 100, requested cap 20,000 objective evaluations. RNSGA2 aspiration-point setup is included in its evaluation cap and runtime. Two-sided paired Wilcoxon signed-rank tests; Holm correction over m=72 comparisons separately per metric, alpha=0.05. Valid matched pairs range from 26 to 30. Invalid outputs remain in run-level evidence; quality summaries/tests use valid matched observations. Positive rank-biserial effect favors OADE. No detected difference is not equivalence. Mean ± sample SD and median/IQR describe run dispersion, not confidence intervals for paired effects.

Twelve configurations: M=2/3/5; DTLZ1 D=6/7/9, DTLZ2–4 D=11/12/14. Implementation identities and adaptations are in [baseline registry](baselines.md).

| Dataset | Records | Invalid | Comparisons | OADE W / ND / L |
|---|---:|---:|---:|---|
| dtlz_benchmark | 2520 | 18 | 144 | 91 / 40 / 13 |

### Quality and cost by implementation

| Problem | ID | Valid / scheduled | IGD median [Q25, Q75] ↓ | IGD mean ± SD | HV median [Q25, Q75] ↑ | HV mean ± SD | Mean seconds | Mean n_eval |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| dtlz1_m2 | OADE_NSGAII | 30 / 30 | 0.00223693 [0.00219213, 0.00227538] | 0.00228432 ± 0.000234932 | 0.233259 [0.233222, 0.233312] | 0.233218 ± 0.000264655 | 5.066 | 19961.8 |
| dtlz1_m2 | NSGA2 | 30 / 30 | 0.00261888 [0.0023214, 0.00344209] | 0.00294605 ± 0.000834274 | 0.232618 [0.231753, 0.233025] | 0.232349 ± 0.000851819 | 2.526 | 20000.0 |
| dtlz1_m2 | RNSGA2 | 30 / 30 | 0.114116 [0.0994078, 0.126388] | 0.134576 ± 0.107422 | 0.152214 [0.143392, 0.163838] | 0.145778 ± 0.0472495 | 5.023 | 20000.0 |
| dtlz1_m2 | DNSGA2 | 30 / 30 | 0.00302226 [0.00262374, 0.00377117] | 0.00375993 ± 0.00229934 | 0.232196 [0.231452, 0.232647] | 0.231582 ± 0.00205019 | 2.386 | 19910.0 |
| dtlz1_m2 | CGDE_NSGAII | 30 / 30 | 1.37225 [1.08836, 1.64118] | 1.36969 ± 0.372146 | 0 [0, 0] | 0 ± 0 | 178.924 | 20000.0 |
| dtlz1_m2 | NSGAII_SDR_OLS | 26 / 30 | 5.16514 [2.89086, 7.97266] | 5.53112 ± 3.60081 | 0 [0, 0] | 0.00380253 ± 0.0134597 | 4.056 | 20000.0 |
| dtlz1_m2 | CE_MOEA | 30 / 30 | 0.707356 [0.3541, 1.06262] | 0.922493 ± 0.963149 | 0 [0, 0.0184367] | 0.022708 ± 0.0527111 | 155.433 | 20000.0 |
| dtlz1_m3 | OADE_NSGAII | 30 / 30 | 0.0292465 [0.0277546, 0.030449] | 0.0292282 ± 0.00168634 | 0.18476 [0.184272, 0.185169] | 0.184658 ± 0.000785746 | 5.451 | 19948.1 |
| dtlz1_m3 | NSGA2 | 30 / 30 | 0.0966522 [0.0564712, 0.319946] | 0.191546 ± 0.173288 | 0.154107 [0.0425942, 0.172796] | 0.112703 ± 0.0678261 | 2.783 | 20000.0 |
| dtlz1_m3 | RNSGA2 | 30 / 30 | 0.555206 [0.270456, 0.77275] | 0.602627 ± 0.423859 | 0 [0, 0.074066] | 0.0379136 ± 0.0538027 | 5.544 | 20000.0 |
| dtlz1_m3 | DNSGA2 | 30 / 30 | 0.372719 [0.163158, 0.719845] | 0.506 ± 0.396752 | 0.0200939 [0, 0.116438] | 0.0540617 ± 0.0659192 | 2.517 | 19910.0 |
| dtlz1_m3 | CGDE_NSGAII | 30 / 30 | 1.3841 [1.22717, 1.68591] | 1.49409 ± 0.416214 | 0 [0, 0] | 0 ± 0 | 132.113 | 20000.0 |
| dtlz1_m3 | NSGAII_SDR_OLS | 28 / 30 | 7.89107 [4.23724, 11.8392] | 8.38492 ± 5.52748 | 0 [0, 0] | 0 ± 0 | 2.959 | 20000.0 |
| dtlz1_m3 | CE_MOEA | 30 / 30 | 1.85189 [1.2193, 2.99418] | 2.09402 ± 1.28447 | 0 [0, 0] | 0.00453396 ± 0.013748 | 141.386 | 20000.0 |
| dtlz1_m5 | OADE_NSGAII | 30 / 30 | 0.897246 [0.55165, 1.90794] | 2.55293 ± 4.97343 | 0 [0, 0.0022134] | 0.00919743 ± 0.0219176 | 6.912 | 19948.4 |
| dtlz1_m5 | NSGA2 | 30 / 30 | 40.1716 [29.5702, 45.7091] | 39.7519 ± 14.7814 | 0 [0, 0] | 0 ± 0 | 3.315 | 20000.0 |
| dtlz1_m5 | RNSGA2 | 30 / 30 | 12.5354 [7.26745, 23.7451] | 16.1939 ± 10.6005 | 0 [0, 0] | 0 ± 0 | 7.045 | 20000.0 |
| dtlz1_m5 | DNSGA2 | 30 / 30 | 34.7427 [26.0059, 46.0555] | 37.3031 ± 15.4556 | 0 [0, 0] | 0 ± 0 | 3.304 | 19910.0 |
| dtlz1_m5 | CGDE_NSGAII | 30 / 30 | 10.9549 [8.54082, 14.9197] | 12.2676 ± 4.97115 | 0 [0, 0] | 0 ± 0 | 170.738 | 20000.0 |
| dtlz1_m5 | NSGAII_SDR_OLS | 30 / 30 | 33.539 [24.5899, 39.364] | 32.6593 ± 11.9307 | 0 [0, 0] | 0 ± 0 | 4.163 | 20000.0 |
| dtlz1_m5 | CE_MOEA | 30 / 30 | 6.67881 [5.14325, 8.4391] | 6.89971 ± 2.47769 | 0 [0, 0] | 0 ± 0 | 189.200 | 20000.0 |
| dtlz2_m2 | OADE_NSGAII | 30 / 30 | 0.00496799 [0.00486521, 0.00517254] | 0.00504106 ± 0.000241459 | 0.418969 [0.41873, 0.419158] | 0.418953 ± 0.000315572 | 9.930 | 19961.8 |
| dtlz2_m2 | NSGA2 | 30 / 30 | 0.00507495 [0.004948, 0.00514335] | 0.0050504 ± 0.000180172 | 0.419428 [0.419255, 0.419567] | 0.419404 ± 0.000236281 | 5.075 | 20000.0 |
| dtlz2_m2 | RNSGA2 | 30 / 30 | 0.19939 [0.189347, 0.207151] | 0.194312 ± 0.0200274 | 0.222703 [0.218183, 0.229899] | 0.225693 ± 0.0112139 | 6.537 | 20000.0 |
| dtlz2_m2 | DNSGA2 | 30 / 30 | 0.00495565 [0.00484783, 0.00506085] | 0.00498284 ± 0.000221118 | 0.419372 [0.419238, 0.419514] | 0.419351 ± 0.000246651 | 4.610 | 19910.0 |
| dtlz2_m2 | CGDE_NSGAII | 30 / 30 | 0.00516141 [0.00505639, 0.00526767] | 0.00518464 ± 0.00016228 | 0.418062 [0.417774, 0.418253] | 0.418013 ± 0.000286784 | 274.229 | 20000.0 |
| dtlz2_m2 | NSGAII_SDR_OLS | 29 / 30 | 0.741921 [0.458251, 0.741929] | 0.605576 ± 0.237036 | 0.109998 [0.109974, 0.167532] | 0.148597 ± 0.0703604 | 6.829 | 20000.0 |
| dtlz2_m2 | CE_MOEA | 30 / 30 | 0.0051096 [0.00493559, 0.0052355] | 0.00511428 ± 0.000194978 | 0.418467 [0.418126, 0.418719] | 0.418435 ± 0.000395445 | 275.584 | 20000.0 |
| dtlz2_m3 | OADE_NSGAII | 30 / 30 | 0.0761624 [0.0744587, 0.0790648] | 0.0766053 ± 0.00275687 | 0.686555 [0.679577, 0.689053] | 0.684464 ± 0.00720538 | 5.632 | 19964.8 |
| dtlz2_m3 | NSGA2 | 30 / 30 | 0.0719822 [0.0703363, 0.0733377] | 0.0719165 ± 0.00249944 | 0.702512 [0.697905, 0.706922] | 0.7014 ± 0.00658344 | 2.758 | 20000.0 |
| dtlz2_m3 | RNSGA2 | 30 / 30 | 0.451482 [0.447048, 0.45645] | 0.450833 ± 0.00654874 | 0.250354 [0.246761, 0.254862] | 0.250539 ± 0.0061373 | 3.827 | 20000.0 |
| dtlz2_m3 | DNSGA2 | 30 / 30 | 0.0706756 [0.0695199, 0.0731905] | 0.0715652 ± 0.00328283 | 0.701723 [0.696538, 0.705375] | 0.700857 ± 0.0061776 | 2.753 | 19910.0 |
| dtlz2_m3 | CGDE_NSGAII | 30 / 30 | 0.0685057 [0.066549, 0.069633] | 0.0684255 ± 0.00207281 | 0.697312 [0.694908, 0.700624] | 0.697546 ± 0.00412858 | 126.939 | 20000.0 |
| dtlz2_m3 | NSGAII_SDR_OLS | 29 / 30 | 0.948479 [0.774583, 0.948491] | 0.842408 ± 0.170264 | 0.120994 [0.120952, 0.121] | 0.145896 ± 0.0757661 | 3.074 | 20000.0 |
| dtlz2_m3 | CE_MOEA | 30 / 30 | 0.0782059 [0.0769002, 0.0793314] | 0.0782169 ± 0.00295766 | 0.678944 [0.675982, 0.68301] | 0.67936 ± 0.00603614 | 136.811 | 20000.0 |
| dtlz2_m5 | OADE_NSGAII | 30 / 30 | 0.421374 [0.399584, 0.43866] | 0.42009 ± 0.0345094 | 0.451729 [0.420305, 0.51683] | 0.460191 ± 0.0846499 | 8.322 | 19953.1 |
| dtlz2_m5 | NSGA2 | 30 / 30 | 0.440291 [0.423882, 0.486842] | 0.457093 ± 0.0593325 | 0.447401 [0.376467, 0.495109] | 0.430292 ± 0.110118 | 4.393 | 20000.0 |
| dtlz2_m5 | RNSGA2 | 30 / 30 | 0.673287 [0.669457, 0.677883] | 0.66922 ± 0.0334772 | 0.247997 [0.240901, 0.255102] | 0.255631 ± 0.0403322 | 3.362 | 20000.0 |
| dtlz2_m5 | DNSGA2 | 30 / 30 | 0.454199 [0.435191, 0.508541] | 0.468075 ± 0.0474111 | 0.394025 [0.339668, 0.467542] | 0.391872 ± 0.0957259 | 3.682 | 19910.0 |
| dtlz2_m5 | CGDE_NSGAII | 30 / 30 | 0.625117 [0.559463, 0.710022] | 0.636379 ± 0.0941996 | 0.159267 [0.0941272, 0.212459] | 0.156506 ± 0.0919104 | 218.084 | 20000.0 |
| dtlz2_m5 | NSGAII_SDR_OLS | 30 / 30 | 1.12296 [0.998297, 1.12298] | 1.04636 ± 0.121364 | 0.146164 [0.0851567, 0.146404] | 0.12351 ± 0.0804767 | 5.905 | 20000.0 |
| dtlz2_m5 | CE_MOEA | 30 / 30 | 0.463712 [0.447163, 0.482906] | 0.466914 ± 0.0218494 | 0.352933 [0.311732, 0.402799] | 0.356086 ± 0.0732435 | 207.812 | 20000.0 |
| dtlz3_m2 | OADE_NSGAII | 30 / 30 | 1.07077 [0.18434, 2.24596] | 1.34808 ± 1.27211 | 0 [0, 0.182416] | 0.0997882 ± 0.158176 | 8.596 | 19959.6 |
| dtlz3_m2 | NSGA2 | 30 / 30 | 2.33485 [1.17342, 3.23118] | 2.64577 ± 1.99319 | 0 [0, 0] | 0.0115128 ± 0.0550477 | 3.694 | 20000.0 |
| dtlz3_m2 | RNSGA2 | 30 / 30 | 3.61272 [2.62611, 5.26791] | 4.65993 ± 3.10363 | 0 [0, 0] | 0 ± 0 | 2.093 | 20000.0 |
| dtlz3_m2 | DNSGA2 | 30 / 30 | 3.48291 [2.20491, 4.78615] | 3.94583 ± 2.37758 | 0 [0, 0] | 0 ± 0 | 3.807 | 19910.0 |
| dtlz3_m2 | CGDE_NSGAII | 30 / 30 | 113.031 [80.2563, 136.111] | 106.434 ± 41.4792 | 0 [0, 0] | 0 ± 0 | 235.126 | 20000.0 |
| dtlz3_m2 | NSGAII_SDR_OLS | 30 / 30 | 23.1548 [16.1641, 46.2697] | 33.4945 ± 25.6911 | 0 [0, 0] | 0 ± 0 | 6.411 | 20000.0 |
| dtlz3_m2 | CE_MOEA | 30 / 30 | 20.7956 [12.3754, 32.7941] | 23.3953 ± 12.7191 | 0 [0, 0] | 0 ± 0 | 192.977 | 20000.0 |
| dtlz3_m3 | OADE_NSGAII | 30 / 30 | 2.54603 [1.28543, 3.69341] | 2.52939 ± 1.49312 | 0 [0, 0] | 0.0407079 ± 0.15509 | 9.701 | 19952.5 |
| dtlz3_m3 | NSGA2 | 30 / 30 | 14.4721 [10.4887, 19.4408] | 15.3961 ± 5.7943 | 0 [0, 0] | 0 ± 0 | 4.580 | 20000.0 |
| dtlz3_m3 | RNSGA2 | 30 / 30 | 14.1763 [11.8774, 18.04] | 15.6956 ± 6.22559 | 0 [0, 0] | 0 ± 0 | 2.895 | 20000.0 |
| dtlz3_m3 | DNSGA2 | 30 / 30 | 20.0108 [16.1131, 23.678] | 20.0643 ± 7.58985 | 0 [0, 0] | 0 ± 0 | 4.300 | 19910.0 |
| dtlz3_m3 | CGDE_NSGAII | 30 / 30 | 108.711 [40.8755, 122.252] | 89.0957 ± 50.8062 | 0 [0, 0] | 0 ± 0 | 224.745 | 20000.0 |
| dtlz3_m3 | NSGAII_SDR_OLS | 30 / 30 | 47.1595 [27.5542, 68.452] | 51.3491 ± 28.1096 | 0 [0, 0] | 0 ± 0 | 5.944 | 20000.0 |
| dtlz3_m3 | CE_MOEA | 30 / 30 | 33.9003 [22.3697, 44.5179] | 35.291 ± 15.0291 | 0 [0, 0] | 0 ± 0 | 205.296 | 20000.0 |
| dtlz3_m5 | OADE_NSGAII | 30 / 30 | 72.7081 [61.9094, 99.7879] | 80.8224 ± 29.0538 | 0 [0, 0] | 0 ± 0 | 9.788 | 19949.5 |
| dtlz3_m5 | NSGA2 | 30 / 30 | 258.945 [208.386, 291.416] | 251.863 ± 58.4305 | 0 [0, 0] | 0 ± 0 | 4.742 | 20000.0 |
| dtlz3_m5 | RNSGA2 | 30 / 30 | 211.418 [185.659, 260.155] | 225.85 ± 69.262 | 0 [0, 0] | 0 ± 0 | 7.723 | 20000.0 |
| dtlz3_m5 | DNSGA2 | 30 / 30 | 239.561 [203.949, 294.646] | 244.852 ± 64.0692 | 0 [0, 0] | 0 ± 0 | 4.703 | 19910.0 |
| dtlz3_m5 | CGDE_NSGAII | 30 / 30 | 246.175 [215.593, 321.33] | 268.135 ± 76.9849 | 0 [0, 0] | 0 ± 0 | 257.292 | 20000.0 |
| dtlz3_m5 | NSGAII_SDR_OLS | 30 / 30 | 76.7487 [32.545, 115.686] | 75.5503 ± 44.3015 | 0 [0, 0] | 0 ± 0 | 6.818 | 20000.0 |
| dtlz3_m5 | CE_MOEA | 30 / 30 | 108.394 [98.5293, 122.621] | 106.133 ± 20.5765 | 0 [0, 0] | 0 ± 0 | 257.151 | 20000.0 |
| dtlz4_m2 | OADE_NSGAII | 30 / 30 | 0.00508111 [0.00501907, 0.00522288] | 0.00513331 ± 0.000212008 | 0.41878 [0.418497, 0.419161] | 0.418761 ± 0.000356253 | 2.736 | 19962.8 |
| dtlz4_m2 | NSGA2 | 30 / 30 | 0.00541158 [0.00508408, 0.74192] | 0.275331 ± 0.36109 | 0.419116 [0.11, 0.419377] | 0.305909 ± 0.151613 | 1.644 | 20000.0 |
| dtlz4_m2 | RNSGA2 | 30 / 30 | 0.515517 [0.288028, 0.727257] | 0.490558 ± 0.214511 | 0.144264 [0.110603, 0.245753] | 0.175908 ± 0.0707743 | 7.671 | 20000.0 |
| dtlz4_m2 | DNSGA2 | 30 / 30 | 0.00505298 [0.00493754, 0.00536529] | 0.103326 ± 0.254759 | 0.419356 [0.419211, 0.419583] | 0.378151 ± 0.106976 | 1.438 | 19910.0 |
| dtlz4_m2 | CGDE_NSGAII | 27 / 30 | 0.00521136 [0.00514621, 0.00537949] | 0.00528141 ± 0.000194838 | 0.418249 [0.417881, 0.418431] | 0.41814 ± 0.000370651 | 73.086 | 20000.0 |
| dtlz4_m2 | NSGAII_SDR_OLS | 27 / 30 | 0.741921 [0.74192, 0.741921] | 0.741922 ± 6.13884e-06 | 0.109998 [0.109997, 0.109999] | 0.109994 ± 1.79527e-05 | 2.701 | 20000.0 |
| dtlz4_m2 | CE_MOEA | 30 / 30 | 0.00518743 [0.00509338, 0.00523881] | 0.00520312 ± 0.000186965 | 0.418416 [0.418213, 0.418541] | 0.418381 ± 0.00026741 | 72.427 | 20000.0 |
| dtlz4_m3 | OADE_NSGAII | 30 / 30 | 0.0779631 [0.0765074, 0.081199] | 0.0786625 ± 0.00289827 | 0.681333 [0.675384, 0.683255] | 0.680528 ± 0.00718355 | 2.797 | 19959.1 |
| dtlz4_m3 | NSGA2 | 30 / 30 | 0.070048 [0.0682321, 0.0723059] | 0.0698968 ± 0.00297973 | 0.708161 [0.704947, 0.712186] | 0.707544 ± 0.00607245 | 1.517 | 20000.0 |
| dtlz4_m3 | RNSGA2 | 30 / 30 | 0.606444 [0.536213, 0.716396] | 0.632848 ± 0.146837 | 0.225999 [0.161425, 0.250114] | 0.233086 ± 0.0990346 | 5.457 | 20000.0 |
| dtlz4_m3 | DNSGA2 | 30 / 30 | 0.0686149 [0.0675897, 0.0703036] | 0.0691032 ± 0.00207763 | 0.708962 [0.706346, 0.710724] | 0.708986 ± 0.00445435 | 1.421 | 19910.0 |
| dtlz4_m3 | CGDE_NSGAII | 30 / 30 | 0.070445 [0.0686474, 0.0723051] | 0.116432 ± 0.142161 | 0.696439 [0.692581, 0.700315] | 0.673255 ± 0.0729688 | 72.682 | 20000.0 |
| dtlz4_m3 | NSGAII_SDR_OLS | 29 / 30 | 0.948479 [0.948478, 0.94848] | 0.948479 ± 1.25786e-06 | 0.120997 [0.120994, 0.120999] | 0.120996 ± 3.18031e-06 | 2.751 | 20000.0 |
| dtlz4_m3 | CE_MOEA | 30 / 30 | 0.0791935 [0.0781626, 0.0809048] | 0.0798476 ± 0.00302256 | 0.674578 [0.670581, 0.681741] | 0.675123 ± 0.00775663 | 72.406 | 20000.0 |
| dtlz4_m5 | OADE_NSGAII | 30 / 30 | 0.374592 [0.352625, 0.396819] | 0.372651 ± 0.0281246 | 0.62992 [0.584154, 0.712485] | 0.647577 ± 0.104992 | 3.040 | 19959.4 |
| dtlz4_m5 | NSGA2 | 30 / 30 | 0.796375 [0.745716, 0.883942] | 0.802355 ± 0.108677 | 0.020515 [0.00401936, 0.0457352] | 0.0381603 ± 0.0552811 | 1.596 | 20000.0 |
| dtlz4_m5 | RNSGA2 | 30 / 30 | 0.735402 [0.695731, 0.801986] | 0.73876 ± 0.105688 | 0.259453 [0.22495, 0.279895] | 0.337004 ± 0.215167 | 5.418 | 20000.0 |
| dtlz4_m5 | DNSGA2 | 30 / 30 | 0.756287 [0.714764, 0.868833] | 0.787657 ± 0.120281 | 0.0421815 [0.00878691, 0.0789341] | 0.0571582 ± 0.0630591 | 1.508 | 19910.0 |
| dtlz4_m5 | CGDE_NSGAII | 30 / 30 | 0.384126 [0.374388, 0.401491] | 0.38866 ± 0.0176401 | 0.653736 [0.608361, 0.685925] | 0.654599 ± 0.0588276 | 72.252 | 20000.0 |
| dtlz4_m5 | NSGAII_SDR_OLS | 27 / 30 | 1.12296 [1.12296, 1.12296] | 1.11631 ± 0.0251042 | 0.146405 [0.146387, 0.146408] | 0.150303 ± 0.0190501 | 2.683 | 20000.0 |
| dtlz4_m5 | CE_MOEA | 30 / 30 | 0.381483 [0.373178, 0.395807] | 0.383574 ± 0.0162317 | 0.643018 [0.57198, 0.65962] | 0.628771 ± 0.0786031 | 72.243 | 20000.0 |

### All configured paired comparisons

| Problem | Metric | Comparator | n | Holm p | Rank-biserial r | Result for OADE |
|---|---|---|---:|---:|---:|---|
| dtlz1_m2 | IGD | CE_MOEA | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m2 | IGD | CGDE_NSGAII | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m2 | IGD | DNSGA2 | 30 | 8.8140368e-06 | +0.931183 | reference_better |
| dtlz1_m2 | IGD | NSGA2 | 30 | 5.6371093e-05 | +0.883871 | reference_better |
| dtlz1_m2 | IGD | NSGAII_SDR_OLS | 26 | 8.6426735e-07 | +1.000000 | reference_better |
| dtlz1_m2 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | IGD | CE_MOEA | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | IGD | CGDE_NSGAII | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | IGD | DNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | IGD | NSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | IGD | NSGAII_SDR_OLS | 28 | 2.3841858e-07 | +1.000000 | reference_better |
| dtlz1_m3 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m5 | IGD | CE_MOEA | 30 | 0.0010066666 | +0.784946 | reference_better |
| dtlz1_m5 | IGD | CGDE_NSGAII | 30 | 2.1647662e-05 | +0.909677 | reference_better |
| dtlz1_m5 | IGD | DNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m5 | IGD | NSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m5 | IGD | NSGAII_SDR_OLS | 30 | 1.4156103e-07 | +0.995699 | reference_better |
| dtlz1_m5 | IGD | RNSGA2 | 30 | 0.00013141707 | +0.858065 | reference_better |
| dtlz2_m2 | IGD | CE_MOEA | 30 | 0.9546476 | +0.277419 | no_significant_difference |
| dtlz2_m2 | IGD | CGDE_NSGAII | 30 | 0.056397026 | +0.582796 | no_significant_difference |
| dtlz2_m2 | IGD | DNSGA2 | 30 | 1 | -0.230108 | no_significant_difference |
| dtlz2_m2 | IGD | NSGA2 | 30 | 1 | +0.027957 | no_significant_difference |
| dtlz2_m2 | IGD | NSGAII_SDR_OLS | 29 | 1.4156103e-07 | +1.000000 | reference_better |
| dtlz2_m2 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz2_m3 | IGD | CE_MOEA | 30 | 0.42533145 | +0.415054 | no_significant_difference |
| dtlz2_m3 | IGD | CGDE_NSGAII | 30 | 1.3411045e-07 | -1.000000 | comparison_better |
| dtlz2_m3 | IGD | DNSGA2 | 30 | 0.00013141707 | -0.858065 | comparison_better |
| dtlz2_m3 | IGD | NSGA2 | 30 | 8.8140368e-06 | -0.931183 | comparison_better |
| dtlz2_m3 | IGD | NSGAII_SDR_OLS | 29 | 1.4156103e-07 | +1.000000 | reference_better |
| dtlz2_m3 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz2_m5 | IGD | CE_MOEA | 30 | 0.00013835728 | +0.853763 | reference_better |
| dtlz2_m5 | IGD | CGDE_NSGAII | 30 | 1.4156103e-07 | +0.995699 | reference_better |
| dtlz2_m5 | IGD | DNSGA2 | 30 | 0.00051082298 | +0.810753 | reference_better |
| dtlz2_m5 | IGD | NSGA2 | 30 | 0.074339904 | +0.561290 | no_significant_difference |
| dtlz2_m5 | IGD | NSGAII_SDR_OLS | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz2_m5 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m2 | IGD | CE_MOEA | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m2 | IGD | CGDE_NSGAII | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m2 | IGD | DNSGA2 | 30 | 5.6371093e-05 | +0.883871 | reference_better |
| dtlz3_m2 | IGD | NSGA2 | 30 | 0.029824108 | +0.630108 | reference_better |
| dtlz3_m2 | IGD | NSGAII_SDR_OLS | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m2 | IGD | RNSGA2 | 30 | 3.548339e-05 | +0.896774 | reference_better |
| dtlz3_m3 | IGD | CE_MOEA | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m3 | IGD | CGDE_NSGAII | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m3 | IGD | DNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m3 | IGD | NSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m3 | IGD | NSGAII_SDR_OLS | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m3 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m5 | IGD | CE_MOEA | 30 | 0.030302731 | +0.625806 | reference_better |
| dtlz3_m5 | IGD | CGDE_NSGAII | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m5 | IGD | DNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m5 | IGD | NSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz3_m5 | IGD | NSGAII_SDR_OLS | 30 | 1 | -0.092473 | no_significant_difference |
| dtlz3_m5 | IGD | RNSGA2 | 30 | 1.4156103e-07 | +0.995699 | reference_better |
| dtlz4_m2 | IGD | CE_MOEA | 30 | 0.80317885 | +0.333333 | no_significant_difference |
| dtlz4_m2 | IGD | CGDE_NSGAII | 27 | 0.3853412 | +0.455026 | no_significant_difference |
| dtlz4_m2 | IGD | DNSGA2 | 30 | 1 | +0.010753 | no_significant_difference |
| dtlz4_m2 | IGD | NSGA2 | 30 | 0.011331404 | +0.681720 | reference_better |
| dtlz4_m2 | IGD | NSGAII_SDR_OLS | 27 | 4.61936e-07 | +1.000000 | reference_better |
| dtlz4_m2 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz4_m3 | IGD | CE_MOEA | 30 | 0.80317885 | +0.346237 | no_significant_difference |
| dtlz4_m3 | IGD | CGDE_NSGAII | 30 | 0.030302731 | -0.625806 | comparison_better |
| dtlz4_m3 | IGD | DNSGA2 | 30 | 1.3411045e-07 | -1.000000 | comparison_better |
| dtlz4_m3 | IGD | NSGA2 | 30 | 1.3411045e-07 | -1.000000 | comparison_better |
| dtlz4_m3 | IGD | NSGAII_SDR_OLS | 29 | 1.4156103e-07 | +1.000000 | reference_better |
| dtlz4_m3 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz4_m5 | IGD | CE_MOEA | 30 | 0.80317885 | +0.333333 | no_significant_difference |
| dtlz4_m5 | IGD | CGDE_NSGAII | 30 | 0.27264656 | +0.466667 | no_significant_difference |
| dtlz4_m5 | IGD | DNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz4_m5 | IGD | NSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz4_m5 | IGD | NSGAII_SDR_OLS | 27 | 4.61936e-07 | +1.000000 | reference_better |
| dtlz4_m5 | IGD | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m2 | HV | CE_MOEA | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m2 | HV | CGDE_NSGAII | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m2 | HV | DNSGA2 | 30 | 4.2002648e-06 | +0.952688 | reference_better |
| dtlz1_m2 | HV | NSGA2 | 30 | 5.9977174e-07 | +0.982796 | reference_better |
| dtlz1_m2 | HV | NSGAII_SDR_OLS | 26 | 1.2516975e-06 | +1.000000 | reference_better |
| dtlz1_m2 | HV | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | HV | CE_MOEA | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | HV | CGDE_NSGAII | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | HV | DNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | HV | NSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m3 | HV | NSGAII_SDR_OLS | 28 | 3.5017729e-07 | +1.000000 | reference_better |
| dtlz1_m3 | HV | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz1_m5 | HV | CE_MOEA | 30 | 0.048634768 | +1.000000 | reference_better |
| dtlz1_m5 | HV | CGDE_NSGAII | 30 | 0.048634768 | +1.000000 | reference_better |
| dtlz1_m5 | HV | DNSGA2 | 30 | 0.048634768 | +1.000000 | reference_better |
| dtlz1_m5 | HV | NSGA2 | 30 | 0.048634768 | +1.000000 | reference_better |
| dtlz1_m5 | HV | NSGAII_SDR_OLS | 30 | 0.048634768 | +1.000000 | reference_better |
| dtlz1_m5 | HV | RNSGA2 | 30 | 0.048634768 | +1.000000 | reference_better |
| dtlz2_m2 | HV | CE_MOEA | 30 | 0.00019549578 | +0.862366 | reference_better |
| dtlz2_m2 | HV | CGDE_NSGAII | 30 | 2.7939677e-07 | +0.991398 | reference_better |
| dtlz2_m2 | HV | DNSGA2 | 30 | 0.0012086052 | -0.802151 | comparison_better |
| dtlz2_m2 | HV | NSGA2 | 30 | 1.5422702e-05 | -0.926882 | comparison_better |
| dtlz2_m2 | HV | NSGAII_SDR_OLS | 29 | 2.0489097e-07 | +1.000000 | reference_better |
| dtlz2_m2 | HV | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz2_m3 | HV | CE_MOEA | 30 | 0.20345511 | +0.522581 | no_significant_difference |
| dtlz2_m3 | HV | CGDE_NSGAII | 30 | 2.7939677e-07 | -0.991398 | comparison_better |
| dtlz2_m3 | HV | DNSGA2 | 30 | 5.9977174e-07 | -0.982796 | comparison_better |
| dtlz2_m3 | HV | NSGA2 | 30 | 1.3411045e-07 | -1.000000 | comparison_better |
| dtlz2_m3 | HV | NSGAII_SDR_OLS | 29 | 2.0489097e-07 | +1.000000 | reference_better |
| dtlz2_m3 | HV | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz2_m5 | HV | CE_MOEA | 30 | 0.00022101961 | +0.858065 | reference_better |
| dtlz2_m5 | HV | CGDE_NSGAII | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz2_m5 | HV | DNSGA2 | 30 | 0.18602245 | +0.535484 | no_significant_difference |
| dtlz2_m5 | HV | NSGA2 | 30 | 1 | +0.208602 | no_significant_difference |
| dtlz2_m5 | HV | NSGAII_SDR_OLS | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz2_m5 | HV | RNSGA2 | 30 | 2.7939677e-07 | +0.991398 | reference_better |
| dtlz3_m2 | HV | CE_MOEA | 30 | 0.083640453 | +1.000000 | no_significant_difference |
| dtlz3_m2 | HV | CGDE_NSGAII | 30 | 0.083640453 | +1.000000 | no_significant_difference |
| dtlz3_m2 | HV | DNSGA2 | 30 | 0.083640453 | +1.000000 | no_significant_difference |
| dtlz3_m2 | HV | NSGA2 | 30 | 0.077392562 | +0.934066 | no_significant_difference |
| dtlz3_m2 | HV | NSGAII_SDR_OLS | 30 | 0.083640453 | +1.000000 | no_significant_difference |
| dtlz3_m2 | HV | RNSGA2 | 30 | 0.083640453 | +1.000000 | no_significant_difference |
| dtlz3_m3 | HV | CE_MOEA | 30 | 1 | +1.000000 | no_significant_difference |
| dtlz3_m3 | HV | CGDE_NSGAII | 30 | 1 | +1.000000 | no_significant_difference |
| dtlz3_m3 | HV | DNSGA2 | 30 | 1 | +1.000000 | no_significant_difference |
| dtlz3_m3 | HV | NSGA2 | 30 | 1 | +1.000000 | no_significant_difference |
| dtlz3_m3 | HV | NSGAII_SDR_OLS | 30 | 1 | +1.000000 | no_significant_difference |
| dtlz3_m3 | HV | RNSGA2 | 30 | 1 | +1.000000 | no_significant_difference |
| dtlz3_m5 | HV | CE_MOEA | 30 | 1 | +0.000000 | no_significant_difference |
| dtlz3_m5 | HV | CGDE_NSGAII | 30 | 1 | +0.000000 | no_significant_difference |
| dtlz3_m5 | HV | DNSGA2 | 30 | 1 | +0.000000 | no_significant_difference |
| dtlz3_m5 | HV | NSGA2 | 30 | 1 | +0.000000 | no_significant_difference |
| dtlz3_m5 | HV | NSGAII_SDR_OLS | 30 | 1 | +0.000000 | no_significant_difference |
| dtlz3_m5 | HV | RNSGA2 | 30 | 1 | +0.000000 | no_significant_difference |
| dtlz4_m2 | HV | CE_MOEA | 30 | 0.0016892627 | +0.789247 | reference_better |
| dtlz4_m2 | HV | CGDE_NSGAII | 27 | 0.0010884404 | +0.841270 | reference_better |
| dtlz4_m2 | HV | DNSGA2 | 30 | 0.39797244 | -0.470968 | no_significant_difference |
| dtlz4_m2 | HV | NSGA2 | 30 | 1 | +0.251613 | no_significant_difference |
| dtlz4_m2 | HV | NSGAII_SDR_OLS | 27 | 6.5565109e-07 | +1.000000 | reference_better |
| dtlz4_m2 | HV | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz4_m3 | HV | CE_MOEA | 30 | 0.18602245 | +0.535484 | no_significant_difference |
| dtlz4_m3 | HV | CGDE_NSGAII | 30 | 0.069122437 | -0.612903 | no_significant_difference |
| dtlz4_m3 | HV | DNSGA2 | 30 | 2.0489097e-07 | -0.995699 | comparison_better |
| dtlz4_m3 | HV | NSGA2 | 30 | 2.0489097e-07 | -0.995699 | comparison_better |
| dtlz4_m3 | HV | NSGAII_SDR_OLS | 29 | 2.0489097e-07 | +1.000000 | reference_better |
| dtlz4_m3 | HV | RNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz4_m5 | HV | CE_MOEA | 30 | 1 | +0.113978 | no_significant_difference |
| dtlz4_m5 | HV | CGDE_NSGAII | 30 | 1 | -0.070968 | no_significant_difference |
| dtlz4_m5 | HV | DNSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz4_m5 | HV | NSGA2 | 30 | 1.3411045e-07 | +1.000000 | reference_better |
| dtlz4_m5 | HV | NSGAII_SDR_OLS | 27 | 6.5565109e-07 | +1.000000 | reference_better |
| dtlz4_m5 | HV | RNSGA2 | 30 | 3.8936734e-05 | +0.905376 | reference_better |

Sources: results/dtlz_benchmark/algorithm_benchmark_*.csv. Runtime compares recorded implementations/environments, not algorithm-independent complexity.

Algorithm-block provenance: [composition](../results/provenance/multiobjective_composition.json). The remaining algorithms retain their archived source/environment uncertainty. No isolated adaptive-restart or Sobol benefit is inferred.

Execution and dataset checksums are recorded in [multiobjective composition](../results/provenance/multiobjective_composition.json); independent statistical checks and final PDF QA are in [validation](../results/provenance/multiobjective_validation.json). These checks verify the configured run records and analyses, not universal algorithm correctness or an isolated mechanism.
