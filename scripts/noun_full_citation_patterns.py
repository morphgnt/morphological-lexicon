#!/usr/bin/env python3

from collections import defaultdict
import re
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")

ACUTE = u"\u0301"
GRAVE = u"\u0300"
CIRCUMFLEX = u"\u0342"


def strip_accents(w):
    return "".join(
        unicodedata.normalize("NFC", "".join(
            component
            for component in unicodedata.normalize("NFD", ch)
            if component not in [ACUTE, GRAVE, CIRCUMFLEX]
        )) for ch in w
    )

SKIP = [

    ## missing full citation

    "αἴτιον",
    "ἀκμήν",
    "ἁλληλουϊά",
    "ἀμήτωρ",
    "ἀπάτωρ",
    "ἀπελεύθερος",
    "ἅρπαξ",
    "αὐτόχειρ",
    "βοηθός",
    "Γαλιλαῖος",
    "Γερασηνός",
    "δέκα",
    "δεκαοκτώ",
    "δεκαπέντε",
    "δεκατέσσαρες",
    "δώδεκα",
    "ἑβδομήκοντα",
    "ἑβδομηκοντάκις",
    "Ἑβραΐς",
    "ἔγγυος",
    "ἔγκυος",
    "εἴκοσι(ν)",
    "ἑκατόν",
    "ἕνδεκα",
    "ἐνενήκοντα",
    "ἐννέα",
    "ἕξ",
    "ἑξήκοντα",
    "ἑπτά",
    "ἔρημος",
    "εφφαθα",
    "ἱερόν",
    "ἱερόσυλος",
    "ἱλαστήριον",
    "κουμ",
    "λεμά",
    "λεπτόν",
    "μίσθιος",
    "μισθωτός",
    "μοιχαλίς",
    "νῆστις",
    "ὀγδοήκοντα",
    "ὀκτώ",
    "πανοῦργος",
    "παραλυτικός",
    "παράσημος",
    "πένης",
    "πέντε",
    "πεντήκοντα",
    "πετεινόν",
    "πλανήτης",
    "πλατεῖα",
    "πρόγονος",
    "σαβαχθάνι",
    "στεῖρα",
    "σύζυγος",
    "συνεργός",
    "τεσσεράκοντα",
    "Τραχωνῖτις",
    "τριάκοντα",
    "χήρα",
    "ὡσαννά",

    ## missing mounce-morphcat

    "ἅλα",
    "ἀλάβαστρος",
    "Ἄψινθος",
    "βάτος",
    "δεσμόν",
    "δύσις",
    "ἦχος",
    "θέρμη",
    "Ἰουνία",
    "Ἰωβήλ",
    "Μαθθαῖος",
    "Μαθθίας",
    "μητρολῴας",
    "νουμηνία",
    "νύμφη",
    "Σαλείμ",
    "σκῦλα",
    "στάδιος",
    "τριετία",
    "χείμαρρος",
    "ψίξ",

    ## problematic without changes to lexemes.yaml

    "δοῦλος",
    "θρίξ",
    "Ἱεροσόλυμα",
    "Ἰσκαριώτης",
    "μέλαν",
    "Μωϋσῆς",
    "Σολομών",
    "ζῆλος",
    "τιμιότης",
    "Ταρσός",
    "Βαριησοῦς",
    "λεγιών",
    "Βαριωνᾶ",
]

DODSON_OVERRIDES = {
    "ἀφθορία":       "N:F",
    "δοκιμασία":     "N:F",
    "εἰδέα":         "N:F",
    "οἰκετεία":      "N:F",
    "ὀλιγοπιστία":   "N:F",
    "πραϋπαθία":     "N:F",
    "Εὕα":           "N:F",
    "κοπρία":        "N:F",
    "Μαρία":         "N:F",

    "βελόνη":        "N:F",
    "διαπαρατριβή":  "N:F",
    "ἐμπαιγμονή":    "N:F",
    "καταδίκη":      "N:F",
    "ὁμίχλη":        "N:F",

    "κορβανᾶς":      "N:M",

    "Ζηλωτής":       "N:M",
    "προσαίτης":     "N:M",
    "στασιαστής":    "N:M",

    "ἄμωμον":        "N:N",  # but Heb 9.14
    "ἀνάγαιον":      "N:N",
    "κλινάριον":     "N:N",
    "κόπριον":       "N:N",
    "σιτίον":        "N:N",
    "φάρμακον":      "N:N",
    "ὠτάριον":       "N:N",
    "δυσεντέριον":   "N:N",
    "Σόδομα":        "N:N",
    "στάδιον":       "N:N",

    "ἀνθρωποκτόνος": "N:M",
    "Ἑβραῖος":       "N:M",
    "ἑκατόνταρχος":  "N:M",
    "ἐλεγμός":       "N:M",
    "Καναναῖος":     "N:M",
    "Κορίνθιος":     "N:M",
    "κυλισμός":      "N:M",
    "λοίδορος":      "N:M",
    "νοσσός":        "N:M",
    "οἰκιακός":      "N:M",
    "οἰκοδόμος":     "N:M",
    "Πύρρος":        "N:M",
    "συναιχμάλωτος": "N:M",
    "Τίτιος":        "N:M",
    "σῖτος":         "N:M",

    "ἄψινθος":       "N:F",

    "δισμυριάς":     "N:F",
    "στιβάς":        "N:F",
    "συγγενίς":      "N:F",
    "διόρθωμα":      "N:N",
    "τρῆμα":         "N:N",
    "ὑπόλειμμα":     "N:N",
    "ἄγγος":         "N:N",
    "δέος":          "N:N",
    "ἐκζήτησις":     "N:F",
    "ἔλεος":         "N:N",
    "ἐπίστασις":     "N:F",
    "λῆμψις":        "N:F",
    "μετάλημψις":    "N:F",
    "πρόσκλισις":    "N:F",
    "σκότος":        "N:N",
    "εὐρακύλων":     "N:M",
    "Σαρών":         "N:M",
    "κατήγωρ":       "N:M",
    "προπάτωρ":      "N:M",
}

MOUNCE_OVERRIDES = {
    "Ἀθῆναι":       "n-1c",

    "ζυγός":        "n-2a",
    "ἄψινθος":      "n-2b",
    "Πέργαμος":     "n-2b",

    "θάμβος":       "n-3d(2b)",
    "στάχυς":       "n-3e(1)",
}


MATCHES_1 = [

    # 1.1/F feminine with genitive ending in ας (1st)

    (r"^(\w+)[ειϊρ]α, ας, ἡ$",      r"^n-1a$",         r"^N:F$"),
    (r"^(\w+)[^ειϊρ]α, ας, ἡ$",     r"^n-1a$",         r"^N:F$"),
    (r"^(\w+)α, ας, ἡ$",            r"^n-1h$",         r"^N:F$"),  # μνᾶ n-1a

    # 1.2/F feminine with genitive ending in ης (1st)

    (r"^(\w+)η, ης, ἡ$",            r"^n-1b$",         r"^N:F$"),
    (r"^(\w+)α, ης, ἡ$",            r"^n-1c$",         r"^N:F$"),
    (r"^(\w+)η, ης, ἡ$",            r"^n-1h$",         r"^N:F$"),  # γῆ/συκῆ 1b

    # 2/M masculine with genitive ending in ου (1st or 2nd)

    (r"^(\w+)[ειϊῳ]ας, ου, ὁ$",     r"^n-1d$",         r"^N:M$"),
    (r"^(\w+)ης, ου, ὁ$",           r"^n-1f$",         r"^N:M$"),
    (r"^(\w+)ης, ου, ὁ$",           r"^n-1h$",         r"^N:M$"),  # Ἑρμῆς n-1f
    (r"^(\w+)ος, ου, ὁ$",           r"^n-2a$",         r"^N:M$"),

    # 2/F feminine with genitive ending in ου (2nd)

    (r"^(\w+)ος, ου, ἡ$",           r"^n-2b$",         r"^N:F$"),

    # 2/N neuter with genitive ending in ου (2nd)

    (r"^(\w+)ον, ου, το$",          r"^n-2c$",         r"^N:N$"),

    # 3/M masculine ending in α (1st)

    (r"^(\w+)ας, α, ὁ$",            r"^n-1e$",         r"^N:M$"),

    # 4/M masculine ending in ω (2nd)

    (r"^(\w+)ως, ω, ὁ$",            r"^n-2e$",         r"^N:M$"),

    # 5.1/M masculine ending in ος (3rd)

    (r"^(\w+)([οω])ψ, \2πος, ὁ$",   r"^n-3a\(1\)$",    r"^N:M$"),
    (r"^(\w+)([αι])ψ, \2βος, ὁ$",   r"^n-3a\(2\)$",    r"^N:M$"),
    (r"^(\w+)([αυηι])ξ, \2κος, ὁ$", r"^n-3b\(1\)$",    r"^N:M$"),
    (r"^(\w+)(υγ)ξ, \2γος, ὁ$",     r"^n-3b\(2\)$",    r"^N:M$"),
    (r"^(\w+)(υ)ξ, \2χος, ὁ$",      r"^n-3b\(3\)$",    r"^N:M$"),
    (r"^(\w+)([ηω])ς, \2τος, ὁ$",   r"^n-3c\(1\)$",    r"^N:M$"),
    (r"^(\w+)ους, οδος, ὁ$",        r"^n-3c\(2\)$",    r"^N:M$"),
    (r"^(\w+)ας, αντος, ὁ$",        r"^n-3c\(5a\)$",   r"^N:M$"),
    (r"^(\w+)ης, εντος, ὁ$",        r"^n-3c\(5a\)$",   r"^N:M$"),
    (r"^(\w+)ους, οντος, ὁ$",       r"^n-3c\(5a\)$",   r"^N:M$"),
    (r"^(\w+)ων, οντος, ὁ$",        r"^n-3c\(5b\)$",   r"^N:M$"),
    (r"^(\w+)ων, ωντος, ὁ$",        r"^n-3c\(5b\)$",   r"^N:M$"),
    (r"^(\w+)υς, υος, ὁ$",          r"^n-3e\(1\)$",    r"^N:M$"),
    (r"^(\w+)ους, οος, ὁ$",         r"^n-3e\(4\)$",    r"^N:M$"),  # βοῦς
    (r"^(\w+)([αηω])ν, \2νος, ὁ$",  r"^n-3f\(1a\)$",   r"^N:M$"),
    (r"^(\w+)ων, ονος, ὁ$",         r"^n-3f\(1b\)$",   r"^N:M$"),
    (r"^(\w+)ην, ενος, ὁ$",         r"^n-3f\(1b\)$",   r"^N:M$"),
    (r"^(\w+)([ηω])ν, \1νος, ὁ$",   r"^n-3f\(1c\)$",   r"^N:M$"),
    (r"^(\w+)(υ)ων, \2νος, ὁ$",     r"^n-3f\(1c\)$",   r"^N:M$"),
    (r"^(\w+)([αη])ρ, \2ρος, ὁ$",   r"^n-3f\(2a\)$",   r"^N:M$"),
    (r"^(\w+)(υ)ς, \2ρος, ὁ$",      r"^n-3f\(2a\)$",   r"^N:M$"),
    (r"^(\w+)ωρ, ορος, ὁ$",         r"^n-3f\(2b\)$",   r"^N:M$"),
    (r"^(\w+)ηρ, ερος, ὁ$",         r"^n-3f\(2b\)$",   r"^N:M$"),
    (r"^(\w+)(α)τηρ, \2τρος, ὁ$",   r"^n-3f\(2c\)$",   r"^N:M$"),
    (r"^(\w+)ηρ, \1δρος, ὁ$",       r"^n-3f\(2c\)$",   r"^N:M$"),

    # 5.1/F feminine ending in ος (3rd)

    (r"^(\w+)([α])ψ, \2πος, ἡ$",    r"^n-3a\(1\)$",    r"^N:F$"),
    (r"^(\w+)([αι]ρ?)ξ, \2κος, ἡ$", r"^n-3b\(1\)$",    r"^N:F$"),
    (r"^(\w+)(η)ξ, εκος, ἡ$",       r"^n-3b\(1\)$",    r"^N:F$"),  # ἀλώπηξ
    (r"^(\w+)η, αικος, ἡ$",         r"^n-3b\(1\)$",    r"^N:F$"),  # γυνή
    (r"^(\w+)([αιου]γ?)ξ, \2γος, ἡ$", r"^n-3b\(2\)$",  r"^N:F$"),
    (r"^(\w+)([ιη])ς, \2τος, ἡ$",   r"^n-3c\(1\)$",    r"^N:F$"),
    (r"^(\w+)(υ)ξ, \2κτος, ἡ$",     r"^n-3c\(1\)$",    r"^N:F$"),  # νύξ
    (r"^(\w+)([αιϊυ]|ει)ς, \2δος, ἡ$", r"^n-3c\(2\)$", r"^N:F$"),
    (r"^(\w+)υς, υος, ἡ$",          r"^n-3e\(1\)$",    r"^N:F$"),
    (r"^ὑς, ὑος, ἡ$",               r"^n-3e\(1\)$",    r"^N:F$"),
    (r"^(\w+)([ιω])ν, \2νος, ἡ$",   r"^n-3f\(1a\)$",   r"^N:F$"),
    (r"^(\w+)(ι)ς, \2νος, ἡ$",      r"^n-3f\(1a\)$",   r"^N:F$"),  # Σαλαμίς
    (r"^(\w+)ην, ενος, ἡ$",         r"^n-3f\(1b\)$",   r"^N:F$"),
    (r"^(\w+)ων, ονος, ἡ$",         r"^n-3f\(1b\)$",   r"^N:F$"),
    (r"^(\w+)(ει)ρ, \2ρος, ἡ$",     r"^n-3f\(2a\)$",   r"^N:F$"),  # χείρ
    (r"^(\w+)([αη]σ?)τηρ, \2τρος, ἡ$", r"^n-3f\(2c\)$", r"^N:F$"),

    # 5.1/N neuter ending in ος (3rd)

    (r"^(\w+)μα, ατος, το$",        r"^n-3c\(4\)$",    r"^N:N$"),
    (r"^(\w+)(α)ς, \2τος, το$",     r"^n-3c\(6a\)$",   r"^N:N$"),
    (r"^(\w+)[αω]ρ, ατος, το$",     r"^n-3c\(6b\)$",   r"^N:N$"),
    (r"^(\w+)υ, ατος, το$",         r"^n-3c\(6d\)$",   r"^N:N$"),
    (r"^οὐς, ὠτος, το$",            r"^n-3c\(6c\)$",   r"^N:N$"),
    (r"^(\w+)(ι), \2τος, το$",      r"^n-3c\(6d\)$",   r"^N:N$"),
    (r"^(\w+)(ω)ς, \2τος, το$",     r"^n-3c\(6c\)$",   r"^N:N$"),
    (r"^(\w+)α, ακτος, το$",        r"^n-3c\(6d\)$",   r"^N:N$"),
    (r"^(\w+)(υ)ρ, \2ρος, το$",     r"^n-3f\(2a\)$",   r"^N:N$"),  # πῦρ

    # 5.2/M masculine ending in εως (3rd)

    (r"^(\w+)υς, εως, ὁ$",          r"^n-3e\(1\)$",    r"^N:M$"),
    (r"^(\w+)ευς, εως, ὁ$",         r"^n-3e\(3\)$",    r"^N:M$"),
    (r"^(\w+)ις, εως, ὁ$",          r"^n-3e\(5b\)$",   r"^N:M$"),

    # 5.2/F feminine ending in εως (3rd)

    (r"^(\w+)ις, εως, ἡ$",          r"^n-3e\(2b\)$",   r"^N:F$"),
    (r"^(\w+)ις, εως, ἡ$",          r"^n-3e\(5a\)$",   r"^N:F$"),
    (r"^(\w+)ις, εως, ἡ$",          r"^n-3e\(5b\)$",   r"^N:F$"),

    # 5.2/N neuter ending in εως (3rd)

    (r"^(\w+)ι, εως, το$",          r"^n-3e\(5b\)$",   r"^N:N$"),

    # 5.3/M masculine ending in ους (3rd)

    (r"^(\w+)ης, ους, ὁ$",          r"^n-3d\(2a\)$",   r"^N:M$"),

    # 5.3/F feminine ending in ους (3rd)

    (r"^(\w+)ως, ους, ἡ$",          r"^n-3d\(3\)$",    r"^N:F$"),

    # 5.3/N neuter ending in ους (3rd)

    (r"^(\w+)ος, ους, το$",         r"^n-3b\(2b\)$",   r"^N:N$"),
    (r"^(\w+)ος, ους, το$",         r"^n-3d\(2b\)$",   r"^N:N$"),

    # 6/M masculine ending in ων (any in theory; 2nd in NT)

    (r"^(\w+)οι, ων, οἱ$",          r"^n-2a$",         r"^N:M$"),  # pl.

    # 6/F feminine ending in ων (any in theory; 1st or 3rd in NT)

    (r"^(\w+)[ειϊρ]αι, ων, αἱ$",    r"^n-1a$",         r"^N:F$"),  # pl.
    (r"^(\w+)αι, ων, αἱ$",          r"^n-1b$",         r"^N:F$"),  # pl.
    (r"^(\w+)αι, ων, αἱ$",          r"^n-1c$",         r"^N:F$"),  # pl.
    (r"^(\w+)εις, εων, αἱ$",        r"^n-3e\(5b\)$",   r"^N:F$"),  # pl.

    # 6/N neuter ending in ων (any in theory; 2nd in NT)

    (r"^(\w+)α, ων, τα$",           r"^n-2c$",         r"^N:N$"),  # pl.
]

MATCHES_2 = [
    (r"ας, ἡ$",    r"^n-1",    r"^N:F$",  "1.1/F"),
    (r"ης, ἡ$",    r"^n-1",    r"^N:F$",  "1.2/F"),

    (r"ου, ὁ$",    r"^n-[12]", r"^N:M$",  "2/M"),
    (r"ου, ἡ$",    r"^n-2",    r"^N:F$",  "2/F"),
    (r"ου, το$",   r"^n-2",    r"^N:N$",  "2/N"),

    (r"α, ὁ$",     r"^n-1",    r"^N:M$",  "3/M"),

    (r"ω, ὁ$",     r"^n-2",    r"^N:M$",  "4/M"),

    (r"ος, ὁ$",    r"^n-3",    r"^N:M$",  "5.1/M"),
    (r"ος, ἡ$",    r"^n-3",    r"^N:F$",  "5.1/F"),
    (r"ος, το$",   r"^n-3",    r"^N:N$",  "5.1/N"),
    (r"εως, ὁ$",   r"^n-3",    r"^N:M$",  "5.2/M"),
    (r"εως, ἡ$",   r"^n-3",    r"^N:F$",  "5.2/F"),
    (r"εως, το$",  r"^n-3",    r"^N:N$",  "5.2/N"),
    (r"ους, ὁ$",   r"^n-3",    r"^N:M$",  "5.3/M"),
    (r"ους, ἡ$",   r"^n-3",    r"^N:F$",  "5.3/F"),
    (r"ους, το$",  r"^n-3",    r"^N:N$",  "5.3/N"),

    (r"ων, οἱ$",   r"^n-2",    r"^N:M$",  "6/M"),
    (r"ων, αἱ$",   r"^n-[13]", r"^N:F$",  "6/F"),
    (r"ων, τα$",   r"^n-2",    r"^N:N$",  "6/N"),
]

MATCHES_3 = [
    (r"ας, ἡ$",    r"^n-1",    r"^N:F$",  "1.1/F"),
    (r"ης, ἡ$",    r"^n-1",    r"^N:F$",  "1.2/F"),
    (r"ου, ὁ$",    r"^n-[12]", r"^N:M$",  "2/M"),
    (r"ου, ἡ$",    r"^n-2",    r"^N:F$",  "2/F"),
    (r"ου, το$",   r"^n-2",    r"^N:N$",  "2/N"),
    (r"α, ὁ$",     r"^n-1",    r"^N:M$",  "3/M"),
    (r"ω, ὁ$",     r"^n-2",    r"^N:M$",  "4/M"),
    (r"εως, ὁ$",   r"^n-3",    r"^N:M$",  "5.2/M"),
    (r"εως, ἡ$",   r"^n-3",    r"^N:F$",  "5.2/F"),
    (r"εως, το$",  r"^n-3",    r"^N:N$",  "5.2/N"),
    (r"ους, ὁ$",   r"^n-3",    r"^N:M$",  "5.3/M"),
    (r"ους, ἡ$",   r"^n-3",    r"^N:F$",  "5.3/F"),
    (r"ους, το$",  r"^n-3",    r"^N:N$",  "5.3/N"),
    (r"ων, οἱ$",   r"^n-2",    r"^N:M$",  "6/M"),
    (r"ων, αἱ$",   r"^n-[13]", r"^N:F$",  "6/F"),
    (r"ων, τα$",   r"^n-2",    r"^N:N$",  "6/N"),

    (r"πος, (ὁ|ἡ|το)$",     r"^n-3a\(1\)$",           r"^N:[MFN]$",  "5.1.1"),
    (r"βος, (ὁ|ἡ|το)$",     r"^n-3a\(2\)$",           r"^N:[MFN]$",  "5.1.2"),

    (r"κος, (ὁ|ἡ|το)$",     r"^n-3b\(1\)$",           r"^N:[MFN]$",  "5.1.3"),
    (r"γος, (ὁ|ἡ|το)$",     r"^n-3b\(2\)$",           r"^N:[MFN]$",  "5.1.4"),
    (r"χος, (ὁ|ἡ|το)$",     r"^n-3b\(3\)$",           r"^N:[MFN]$",  "5.1.5"),

    (r"τος, (ὁ|ἡ|το)$",     r"^n-3c\((1|4|5.|6.)\)$", r"^N:[MFN]$",  "5.1.6"),
    (r"δος, (ὁ|ἡ|το)$",     r"^n-3c\(2\)$",           r"^N:[MFN]$",  "5.1.7"),

    (r"νος, (ὁ|ἡ|το)$",     r"^n-3f\(1.\)$",          r"^N:[MFN]$",  "5.1.8"),
    (r"ρος, (ὁ|ἡ|το)$",     r"^n-3f\(2.\)$",          r"^N:[MFN]$",  "5.1.9"),

    (r"[ουὑ]ος, (ὁ|ἡ|το)$", r"^n-3e\((1|4)\)$",       r"^N:[MFN]$",  "5.1.10"),
]


success_count = 0
fail_count = 0
first_fail = None

sub_rules = defaultdict(set)
match_2_counts = defaultdict(int)
match_3_counts = defaultdict(int)

for lexeme, metadata in sorted_items(lexemes):
    pos = metadata.get("pos")
    full_citation = metadata.get("full-citation-form")
    dodson_pos = DODSON_OVERRIDES.get(lexeme, metadata.get("dodson-pos", ""))
    mounce_morphcat = MOUNCE_OVERRIDES.get(
        lexeme, metadata.get("mounce-morphcat", ""))

    if (
        pos == "N" or
        (dodson_pos and dodson_pos.startswith("N")) or
        (
            isinstance(mounce_morphcat, str) and
            mounce_morphcat.startswith("n")
        ) or (
            isinstance(mounce_morphcat, list) and
            any(x.startswith("n") for x in mounce_morphcat)
        )
    ):

        if lexeme in SKIP:
            continue

        if not re.match(r"(\w+), (\w+), (\w+)$", full_citation):
            continue

        if isinstance(mounce_morphcat, list):
            mounce_morphcat = ";".join(mounce_morphcat)

        success_1 = False
        success_2 = False
        success_3 = False

        for i, (end, cat, dodson) in enumerate(MATCHES_1):
            if (
                full_citation and mounce_morphcat and
                re.search(end, strip_accents(full_citation)) and
                re.search(cat, mounce_morphcat) and
                re.search(dodson, dodson_pos)
            ):
                success_1 = True
                ii = i
                break

        for (end, cat, dodson, key) in MATCHES_2:
            if (
                full_citation and mounce_morphcat and
                re.search(end, strip_accents(full_citation)) and
                re.search(cat, mounce_morphcat) and
                re.search(dodson, dodson_pos)
            ):
                success_2 = True
                key_2 = key
                break

        for (end, cat, dodson, key) in MATCHES_3:
            if (
                full_citation and mounce_morphcat and
                re.search(end, strip_accents(full_citation)) and
                re.search(cat, mounce_morphcat) and
                re.search(dodson, dodson_pos)
            ):
                success_3 = True
                key_3 = key
                break

        if success_1 and success_2 and success_3:
            success_count += 1
            sub_rules[key_2].add(ii)
            match_2_counts[key_2] += 1
            match_3_counts[key_3] += 1
        else:
            fail_count += 1
            # print(lexeme, ":", full_citation)
            if not first_fail:
                first_fail = '(r"^{}$", r"^{}$", r"^{}$"),  # {} '.format(
                    strip_accents(full_citation),
                    mounce_morphcat, dodson_pos, lexeme)

print(success_count, fail_count)
print(first_fail)

# for j, i_set in sorted(sub_rules.items()):
#     print(j, sorted(list(i_set)))

# for cat, count in sorted(match_2_counts.items()):
#     print(cat, count)

# for cat, count in sorted(match_3_counts.items()):
#     print(cat, count)
