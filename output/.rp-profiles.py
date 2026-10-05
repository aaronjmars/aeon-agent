import re

def clean_bio(bio):
    if not bio:
        return None
    b = re.sub(r'[\r\n]+', ' ', bio).strip()
    b = re.sub(r'\s+', ' ', b)
    if len(b) > 140:
        b = b[:140].rstrip() + "…"
    return b

def fmt_followers(f):
    if f is None or f < 10:
        return None
    if f < 1000:
        return str(f)
    return "{:.1f}k".format(f/1000).replace(".0k", "k")

profiles = [
    ("djh4ck3r", "A4r0n$t0n3", None, None, None, "https://ubiquitous-alpaca-247db6.netlify.app", None, 0, 3),
    ("normancomics", "normancomics.eth", "Cartoonist of the comic-strip, NORMAN(R) / Author - iatrogenic / Founder/Lead Engineer @BibleFi / Anti-Pop-Culture Style Consultant / Esoteric Cipherpunk", "East-Coast US", "BibleFi", "https://app.icebreaker.xyz/profiles/fTu9Z9w4XNzzURf8lfaS6", "KEKBONDS", 131, 62),
    ("Domimueller85", "Dominik", "Ich bin Koch und Dichter, einer der besseren Richter, wer nicht wagt der nicht gewinnt, nun blaest eine spezieller wind den ich selbst noch finden muss!", "de", None, "", "Dominik_mu5237", 0, 387),
    ("Blockchains", "Blockchain Lab", "The Worlds First Blockchain Lab; Venture Studio with deep expertise in Digital Assets, Tokenization and Stablecoins", "London", "Blockchain Lab", "BlockchainLab.com", "BlockchainLab", 125, 588),
    ("nkipa", "Paul Dawidowicz", "Consultant, Data Scientist, Engineer and Entrepreneur", "Chile", "NKIPA, LLC.", "", None, 6, 223),
    ("Towa-1", "Emmanuel Kofi Ntow Gyamfi", None, None, None, "", None, 0, 23),
    ("adeyholar", None, None, None, None, "", None, 5, 12721),
    ("Colinchiu007", "ColinChiu", None, None, None, "", None, 2, 43),
    ("alifndaru", "alif ndaru kusuma", "hello my name alif", "Jakarta", None, "", None, 12, 36),
    ("emkaters", None, None, None, None, "", None, 0, 0),
    ("khairi-u28", "Khairi Ubaidah", "Web Developer and Web Designer", "Jakarta, Indonesia", "Japan Dream Tour Co., Ltd.", "khairiu.site", "khairiu28", 15, 28),
    ("alekseizadubnenko-art", None, None, None, None, "", None, 4, 9),
    ("jarjut", "Ahmad Fajrul Falah", None, "Surabaya, Indonesia", None, "https://jarjut.dev/", None, 16, 42),
    ("n1106836-collab", None, "I am passionate about technology, particularly the .NET framework. As a Backend Developer and student at the esteemed National Taipei University of Business, I", None, None, "", None, 0, 99),
    ("robertoatila", "Roberto Atila", "Full-Stack Developer | Java, Spring Boot, PHP, JavaScript | TCC: SaaS multi-tenant com JWT e Docker | Buscando 1o estagio - 18 anos", "Ourinhos-SP", "ETEC Jacinto Ferreira de Sa", "", None, 32, 15),
    ("termaulmaul", "Maulana Rafi", None, "Jakarta", "Mandiri Sekuritas", "", None, 15, 95),
    ("AndresPuglia98", "Jose Andres Puglia", None, None, "@thisisqubika", "", None, 0, 6),
    ("Bentley7988", None, None, None, None, "", None, 0, 1),
    ("Cacrowley01", None, None, None, None, "", None, 10, 2),
    ("Ninoweer", None, None, None, None, "", None, 4, 1),
    ("alexiss31", None, None, None, None, "", None, 0, 6),
    ("bravoxcapitan", None, None, None, None, "", None, 0, 0),
    ("eterru", None, None, None, None, "", None, 0, 0),
]

for login, name, bio, loc, company, blog, twitter, followers, repos in profiles:
    b = clean_bio(bio)
    fol = fmt_followers(followers)
    notable = (followers or 0) >= 100 or (repos or 0) >= 20
    print(login, "| notable=", notable, "| followers_disp=", fol, "| bio=", b)
