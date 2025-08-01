"""
Constants for CVSS4 computations and checks.
Translated from the RedHatProductSecurity cvss-v4-calculator repository:
https://github.com/RedHatProductSecurity/cvss-v4-calculator
"""

from __future__ import unicode_literals

try:
    from collections import OrderedDict
except ImportError:
    # noinspection PyUnresolvedReferences
    from ordereddict import OrderedDict

# Small enough value which can be added to a value which will be rounded to 1 decimal place so the
# result is rounded correctly despite floating point inaccuracies.
EPSILON = 10**-6

# CVSS4 requires vector metrics to follow a specific order as defined in the specification.
# Vectors that do not adhere to this order are considered invalid and may be rejected.
# This module does not enforce field ordering for CVSS4 vector inputs but will reorder them
# to produce valid CVSS4 vectors.
# The lists below follow the required CVSS4 ordering.
# Note that METRICS_ABBREVIATIONS is used to create the clean_vector().
# Specification: https://www.first.org/cvss/v4-0/specification-document#Vector-String

METRICS = [
    "AV",
    "AC",
    "AT",
    "PR",
    "UI",
    "VC",
    "VI",
    "VA",
    "SC",
    "SI",
    "SA",
    "E",
    "CR",
    "IR",
    "AR",
    "MAV",
    "MAC",
    "MAT",
    "MPR",
    "MUI",
    "MVC",
    "MVI",
    "MVA",
    "MSC",
    "MSI",
    "MSA",
    "S",
    "AU",
    "R",
    "V",
    "RE",
    "U",
]

METRICS_MANDATORY = [
    "AV",
    "AC",
    "AT",
    "PR",
    "UI",
    "VC",
    "VI",
    "VA",
    "SC",
    "SI",
    "SA",
]

METRICS_ABBREVIATIONS = OrderedDict(
    [
        ("AV", "Attack Vector"),
        ("AC", "Attack Complexity"),
        ("AT", "Attack Requirement"),
        ("PR", "Privileges Required"),
        ("UI", "User Interaction"),
        ("VC", "Vulnerable System Impact Confidentiality"),
        ("VI", "Vulnerable System Impact Integrity"),
        ("VA", "Vulnerable System Impact Availability"),
        ("SC", "Subsequent System Impact Confidentiality"),
        ("SI", "Subsequent System Impact Integrity"),
        ("SA", "Subsequent System Impact Availability"),
        ("E", "Exploit Maturity"),
        ("CR", "Confidentiality Req."),
        ("IR", "Integrity Req."),
        ("AR", "Availability Req."),
        ("MAV", "Modified Attack Vector"),
        ("MAC", "Modified Attack Complexity"),
        ("MAT", "Modified Attack Requirement"),
        ("MPR", "Modified Privileges Required"),
        ("MUI", "Modified User Interaction"),
        ("MVC", "Modified Vulnerable System Impact Confidentiality"),
        ("MVI", "Modified Vulnerable System Impact Integrity"),
        ("MVA", "Modified Vulnerable System Impact Availability"),
        ("MSC", "Modified Subsequent System Impact Confidentiality"),
        ("MSI", "Modified Subsequent System Impact Integrity"),
        ("MSA", "Modified Subsequent System Impact Availability"),
        ("S", "Safety"),
        ("AU", "Automatable"),
        ("R", "Recovery"),
        ("V", "Value Density"),
        ("RE", "Vulnerability Response Effort"),
        ("U", "Provider Urgency"),
    ]
)

METRICS_ABBREVIATIONS_JSON = OrderedDict(
    [
        ("AV", "attackVector"),
        ("AC", "attackComplexity"),
        ("AT", "attackRequirement"),
        ("PR", "privilegesRequired"),
        ("UI", "userInteraction"),
        ("VC", "vulnerableSystemImpactConfidentiality"),
        ("VI", "vulnerableSystemImpactIntegrity"),
        ("VA", "vulnerableSystemImpactAvailability"),
        ("SC", "subsequentSystemImpactConfidentiality"),
        ("SI", "subsequentSystemImpactIntegrity"),
        ("SA", "subsequentSystemImpactAvailability"),
        ("E", "exploitMaturity"),
        ("CR", "confidentialityRequirements"),
        ("IR", "integrityRequirements"),
        ("AR", "availabilityRequirements"),
        ("MAV", "modifiedAttackVector"),
        ("MAC", "modifiedAttackComplexity"),
        ("MAT", "modifiedAttackRequirement"),
        ("MPR", "modifiedPrivilegesRequired"),
        ("MUI", "modifiedUserInteraction"),
        ("MVC", "modifiedVulnerableSystemImpactConfidentiality"),
        ("MVI", "modifiedVulnerableSystemImpactIntegrity"),
        ("MVA", "modifiedVulnerableSystemImpactAvailability"),
        ("MSC", "modifiedSubsequentSystemImpactConfidentiality"),
        ("MSI", "modifiedSubsequentSystemImpactIntegrity"),
        ("MSA", "modifiedSubsequentSystemImpactAvailability"),
        ("S", "safety"),
        ("AU", "automatable"),
        ("R", "recovery"),
        ("V", "valueDensity"),
        ("RE", "vulnerabilityResponseEffort"),
        ("U", "providerUrgency"),
    ]
)

METRICS_VALUE_NAMES = OrderedDict(
    [
        (
            "AV",
            OrderedDict([("N", "Network"), ("A", "Adjacent"), ("L", "Local"), ("P", "Physical")]),
        ),
        ("AC", OrderedDict([("L", "Low"), ("H", "High")])),
        ("AT", OrderedDict([("N", "None"), ("P", "Present")])),
        ("PR", OrderedDict([("N", "None"), ("L", "Low"), ("H", "High")])),
        ("UI", OrderedDict([("N", "None"), ("P", "Passive"), ("A", "Active")])),
        ("VC", OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")])),
        ("VI", OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")])),
        ("VA", OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")])),
        ("SC", OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")])),
        ("SI", OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")])),
        ("SA", OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")])),
        (
            "E",
            OrderedDict(
                [("X", "Not Defined"), ("A", "Attacked"), ("P", "POC"), ("U", "Unreported")]
            ),
        ),
        ("CR", OrderedDict([("X", "Not Defined"), ("H", "High"), ("M", "Medium"), ("L", "Low")])),
        ("IR", OrderedDict([("X", "Not Defined"), ("H", "High"), ("M", "Medium"), ("L", "Low")])),
        ("AR", OrderedDict([("X", "Not Defined"), ("H", "High"), ("M", "Medium"), ("L", "Low")])),
        (
            "MAV",
            OrderedDict(
                [
                    ("X", "Not Defined"),
                    ("N", "Network"),
                    ("A", "Adjacent"),
                    ("L", "Local"),
                    ("P", "Physical"),
                ]
            ),
        ),
        ("MAC", OrderedDict([("X", "Not Defined"), ("L", "Low"), ("H", "High")])),
        ("MAT", OrderedDict([("X", "Not Defined"), ("N", "None"), ("P", "Present")])),
        ("MPR", OrderedDict([("X", "Not Defined"), ("N", "None"), ("L", "Low"), ("H", "High")])),
        (
            "MUI",
            OrderedDict([("X", "Not Defined"), ("N", "None"), ("P", "Passive"), ("A", "Active")]),
        ),
        ("MVC", OrderedDict([("X", "Not Defined"), ("H", "High"), ("L", "Low"), ("N", "None")])),
        ("MVI", OrderedDict([("X", "Not Defined"), ("H", "High"), ("L", "Low"), ("N", "None")])),
        ("MVA", OrderedDict([("X", "Not Defined"), ("H", "High"), ("L", "Low"), ("N", "None")])),
        (
            "MSC",
            OrderedDict([("X", "Not Defined"), ("H", "High"), ("L", "Low"), ("N", "Negligible")]),
        ),
        (
            "MSI",
            OrderedDict(
                [
                    ("X", "Not Defined"),
                    ("S", "Safety"),
                    ("H", "High"),
                    ("L", "Low"),
                    ("N", "Negligible"),
                ]
            ),
        ),
        (
            "MSA",
            OrderedDict(
                [
                    ("X", "Not Defined"),
                    ("S", "Safety"),
                    ("H", "High"),
                    ("L", "Low"),
                    ("N", "Negligible"),
                ]
            ),
        ),
        ("S", OrderedDict([("X", "Not Defined"), ("N", "Negligible"), ("P", "Present")])),
        ("AU", OrderedDict([("X", "Not Defined"), ("N", "No"), ("Y", "Yes")])),
        (
            "R",
            OrderedDict(
                [("X", "Not Defined"), ("A", "Automatic"), ("U", "User"), ("I", "Inrecoverable")]
            ),
        ),
        ("V", OrderedDict([("X", "Not Defined"), ("D", "Diffuse"), ("C", "Concentrated")])),
        ("RE", OrderedDict([("X", "Not Defined"), ("L", "Low"), ("M", "Moderate"), ("H", "High")])),
        (
            "U",
            OrderedDict(
                [
                    ("X", "Not Defined"),
                    ("Clear", "Clear"),
                    ("Green", "Green"),
                    ("Amber", "Amber"),
                    ("Red", "Red"),
                ]
            ),
        ),
    ]
)


MAX_COMPOSED = OrderedDict(
    [
        (
            # EQ1
            "eq1",
            OrderedDict(
                [
                    ("0", ["AV:N/PR:N/UI:N/"]),
                    ("1", ["AV:A/PR:N/UI:N/", "AV:N/PR:L/UI:N/", "AV:N/PR:N/UI:P/"]),
                    ("2", ["AV:P/PR:N/UI:N/", "AV:A/PR:L/UI:P/"]),
                ]
            ),
        ),
        (
            # EQ2
            "eq2",
            OrderedDict([("0", ["AC:L/AT:N/"]), ("1", ["AC:H/AT:N/", "AC:L/AT:P/"])]),
        ),
        (
            # EQ3+EQ6
            "eq3",
            OrderedDict(
                [
                    (
                        "0",
                        OrderedDict(
                            [
                                ("0", ["VC:H/VI:H/VA:H/CR:H/IR:H/AR:H/"]),
                                (
                                    "1",
                                    [
                                        "VC:H/VI:H/VA:L/CR:M/IR:M/AR:H/",
                                        "VC:H/VI:H/VA:H/CR:M/IR:M/AR:M/",
                                    ],
                                ),
                            ]
                        ),
                    ),
                    (
                        "1",
                        OrderedDict(
                            [
                                (
                                    "0",
                                    [
                                        "VC:L/VI:H/VA:H/CR:H/IR:H/AR:H/",
                                        "VC:H/VI:L/VA:H/CR:H/IR:H/AR:H/",
                                    ],
                                ),
                                (
                                    "1",
                                    [
                                        "VC:L/VI:H/VA:L/CR:H/IR:M/AR:H/",
                                        "VC:L/VI:H/VA:H/CR:H/IR:M/AR:M/",
                                        "VC:H/VI:L/VA:H/CR:M/IR:H/AR:M/",
                                        "VC:H/VI:L/VA:L/CR:M/IR:H/AR:H/",
                                        "VC:L/VI:L/VA:H/CR:H/IR:H/AR:M/",
                                    ],
                                ),
                            ]
                        ),
                    ),
                    ("2", OrderedDict([("1", ["VC:L/VI:L/VA:L/CR:H/IR:H/AR:H/"])])),
                ]
            ),
        ),
        (
            # EQ4
            "eq4",
            OrderedDict(
                [
                    ("0", ["SC:H/SI:S/SA:S/"]),
                    ("1", ["SC:H/SI:H/SA:H/"]),
                    ("2", ["SC:L/SI:L/SA:L/"]),
                ]
            ),
        ),
        (
            # EQ5
            "eq5",
            OrderedDict(
                [
                    ("0", ["E:A/"]),
                    ("1", ["E:P/"]),
                    ("2", ["E:U/"]),
                ]
            ),
        ),
    ]
)

MAX_SEVERITY = OrderedDict(
    [
        ("eq1", OrderedDict([(0, 1), (1, 4), (2, 5)])),
        ("eq2", OrderedDict([(0, 1), (1, 2)])),
        (
            "eq3eq6",
            OrderedDict(
                [
                    (0, OrderedDict([(0, 7), (1, 6)])),
                    (1, OrderedDict([(0, 8), (1, 8)])),
                    (2, OrderedDict([(1, 10)])),
                ]
            ),
        ),
        ("eq4", OrderedDict([(0, 6), (1, 5), (2, 4)])),
        ("eq5", OrderedDict([(0, 1), (1, 1), (2, 1)])),
    ]
)

CVSS_LOOKUP_GLOBAL = OrderedDict(
    [
        ("000000", 10),
        ("000001", 9.9),
        ("000010", 9.8),
        ("000011", 9.5),
        ("000020", 9.5),
        ("000021", 9.2),
        ("000100", 10),
        ("000101", 9.6),
        ("000110", 9.3),
        ("000111", 8.7),
        ("000120", 9.1),
        ("000121", 8.1),
        ("000200", 9.3),
        ("000201", 9),
        ("000210", 8.9),
        ("000211", 8),
        ("000220", 8.1),
        ("000221", 6.8),
        ("001000", 9.8),
        ("001001", 9.5),
        ("001010", 9.5),
        ("001011", 9.2),
        ("001020", 9),
        ("001021", 8.4),
        ("001100", 9.3),
        ("001101", 9.2),
        ("001110", 8.9),
        ("001111", 8.1),
        ("001120", 8.1),
        ("001121", 6.5),
        ("001200", 8.8),
        ("001201", 8),
        ("001210", 7.8),
        ("001211", 7),
        ("001220", 6.9),
        ("001221", 4.8),
        ("002001", 9.2),
        ("002011", 8.2),
        ("002021", 7.2),
        ("002101", 7.9),
        ("002111", 6.9),
        ("002121", 5),
        ("002201", 6.9),
        ("002211", 5.5),
        ("002221", 2.7),
        ("010000", 9.9),
        ("010001", 9.7),
        ("010010", 9.5),
        ("010011", 9.2),
        ("010020", 9.2),
        ("010021", 8.5),
        ("010100", 9.5),
        ("010101", 9.1),
        ("010110", 9),
        ("010111", 8.3),
        ("010120", 8.4),
        ("010121", 7.1),
        ("010200", 9.2),
        ("010201", 8.1),
        ("010210", 8.2),
        ("010211", 7.1),
        ("010220", 7.2),
        ("010221", 5.3),
        ("011000", 9.5),
        ("011001", 9.3),
        ("011010", 9.2),
        ("011011", 8.5),
        ("011020", 8.5),
        ("011021", 7.3),
        ("011100", 9.2),
        ("011101", 8.2),
        ("011110", 8),
        ("011111", 7.2),
        ("011120", 7),
        ("011121", 5.9),
        ("011200", 8.4),
        ("011201", 7),
        ("011210", 7.1),
        ("011211", 5.2),
        ("011220", 5),
        ("011221", 3),
        ("012001", 8.6),
        ("012011", 7.5),
        ("012021", 5.2),
        ("012101", 7.1),
        ("012111", 5.2),
        ("012121", 2.9),
        ("012201", 6.3),
        ("012211", 2.9),
        ("012221", 1.7),
        ("100000", 9.8),
        ("100001", 9.5),
        ("100010", 9.4),
        ("100011", 8.7),
        ("100020", 9.1),
        ("100021", 8.1),
        ("100100", 9.4),
        ("100101", 8.9),
        ("100110", 8.6),
        ("100111", 7.4),
        ("100120", 7.7),
        ("100121", 6.4),
        ("100200", 8.7),
        ("100201", 7.5),
        ("100210", 7.4),
        ("100211", 6.3),
        ("100220", 6.3),
        ("100221", 4.9),
        ("101000", 9.4),
        ("101001", 8.9),
        ("101010", 8.8),
        ("101011", 7.7),
        ("101020", 7.6),
        ("101021", 6.7),
        ("101100", 8.6),
        ("101101", 7.6),
        ("101110", 7.4),
        ("101111", 5.8),
        ("101120", 5.9),
        ("101121", 5),
        ("101200", 7.2),
        ("101201", 5.7),
        ("101210", 5.7),
        ("101211", 5.2),
        ("101220", 5.2),
        ("101221", 2.5),
        ("102001", 8.3),
        ("102011", 7),
        ("102021", 5.4),
        ("102101", 6.5),
        ("102111", 5.8),
        ("102121", 2.6),
        ("102201", 5.3),
        ("102211", 2.1),
        ("102221", 1.3),
        ("110000", 9.5),
        ("110001", 9),
        ("110010", 8.8),
        ("110011", 7.6),
        ("110020", 7.6),
        ("110021", 7),
        ("110100", 9),
        ("110101", 7.7),
        ("110110", 7.5),
        ("110111", 6.2),
        ("110120", 6.1),
        ("110121", 5.3),
        ("110200", 7.7),
        ("110201", 6.6),
        ("110210", 6.8),
        ("110211", 5.9),
        ("110220", 5.2),
        ("110221", 3),
        ("111000", 8.9),
        ("111001", 7.8),
        ("111010", 7.6),
        ("111011", 6.7),
        ("111020", 6.2),
        ("111021", 5.8),
        ("111100", 7.4),
        ("111101", 5.9),
        ("111110", 5.7),
        ("111111", 5.7),
        ("111120", 4.7),
        ("111121", 2.3),
        ("111200", 6.1),
        ("111201", 5.2),
        ("111210", 5.7),
        ("111211", 2.9),
        ("111220", 2.4),
        ("111221", 1.6),
        ("112001", 7.1),
        ("112011", 5.9),
        ("112021", 3),
        ("112101", 5.8),
        ("112111", 2.6),
        ("112121", 1.5),
        ("112201", 2.3),
        ("112211", 1.3),
        ("112221", 0.6),
        ("200000", 9.3),
        ("200001", 8.7),
        ("200010", 8.6),
        ("200011", 7.2),
        ("200020", 7.5),
        ("200021", 5.8),
        ("200100", 8.6),
        ("200101", 7.4),
        ("200110", 7.4),
        ("200111", 6.1),
        ("200120", 5.6),
        ("200121", 3.4),
        ("200200", 7),
        ("200201", 5.4),
        ("200210", 5.2),
        ("200211", 4),
        ("200220", 4),
        ("200221", 2.2),
        ("201000", 8.5),
        ("201001", 7.5),
        ("201010", 7.4),
        ("201011", 5.5),
        ("201020", 6.2),
        ("201021", 5.1),
        ("201100", 7.2),
        ("201101", 5.7),
        ("201110", 5.5),
        ("201111", 4.1),
        ("201120", 4.6),
        ("201121", 1.9),
        ("201200", 5.3),
        ("201201", 3.6),
        ("201210", 3.4),
        ("201211", 1.9),
        ("201220", 1.9),
        ("201221", 0.8),
        ("202001", 6.4),
        ("202011", 5.1),
        ("202021", 2),
        ("202101", 4.7),
        ("202111", 2.1),
        ("202121", 1.1),
        ("202201", 2.4),
        ("202211", 0.9),
        ("202221", 0.4),
        ("210000", 8.8),
        ("210001", 7.5),
        ("210010", 7.3),
        ("210011", 5.3),
        ("210020", 6),
        ("210021", 5),
        ("210100", 7.3),
        ("210101", 5.5),
        ("210110", 5.9),
        ("210111", 4),
        ("210120", 4.1),
        ("210121", 2),
        ("210200", 5.4),
        ("210201", 4.3),
        ("210210", 4.5),
        ("210211", 2.2),
        ("210220", 2),
        ("210221", 1.1),
        ("211000", 7.5),
        ("211001", 5.5),
        ("211010", 5.8),
        ("211011", 4.5),
        ("211020", 4),
        ("211021", 2.1),
        ("211100", 6.1),
        ("211101", 5.1),
        ("211110", 4.8),
        ("211111", 1.8),
        ("211120", 2),
        ("211121", 0.9),
        ("211200", 4.6),
        ("211201", 1.8),
        ("211210", 1.7),
        ("211211", 0.7),
        ("211220", 0.8),
        ("211221", 0.2),
        ("212001", 5.3),
        ("212011", 2.4),
        ("212021", 1.4),
        ("212101", 2.4),
        ("212111", 1.2),
        ("212121", 0.5),
        ("212201", 1),
        ("212211", 0.3),
        ("212221", 0.1),
    ]
)