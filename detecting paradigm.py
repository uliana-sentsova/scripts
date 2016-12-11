casa = '<e lm="LEMMA"><i>ROOT</i><par n="cas/a__n"/></e>'
annu = '<e lm="LEMMA"><i>ROOT</i><par n="ann/u__n"/></e>'
parcu = '<e lm="LEMMA"><i>ROOT</i><par n="parc/u__n"/></e>'
zioni = '<e lm="LEMMA"><i>ROOT</i><par n="pupulaz/zioni__n"/></e>'
patri = '<e lm="LEMMA"><i>ROOT</i><par n="patri__n"/></e>'
matri = '<e lm="LEMMA"><i>ROOT</i><par n="matri__n"/></e>'
saccheggiu = '<e lm="LEMMA"><i>ROOT</i><par n="sacchegg/iu__n"/></e>'
filusufia = '<e lm="LEMMA"><i>ROOT</i><par n="filusuf/ìa__n"/></e>'
oriccia = '<e lm="LEMMA"><i>ROOT</i><par n="oricch/ia__n"/></e>'
ripubbrica = '<e lm="LEMMA"><i>ROOT</i><par n="ripùbbric/a__n"/></e>'
citati = '<e lm="LEMMA"><i>ROOT</i><par n="cit/ati__n"/></e>  '
visioni = '<e lm="LEMMA"><i>ROOT</i><par n="vi/sioni__n"/></e>'
libirta = '<e lm="LEMMA"><i>ROOT</i><par n="libirtà__n"/></e>'
giuvintuti = '<e lm="LEMMA"><i>ROOT</i><par n="giuvint/uti__n"/></e>'
sucialismu = '<e lm="LEMMA"><i>ROOT</i><par n="sucialism/u__n"/></e>'
pianeta = '<e lm="LEMMA"><i>ROOT</i><par n="pianet/a__n"/></e>'
chitarrista = '<e lm="LEMMA"><i>ROOT</i><par n="chitarrist/a__n"/></e>'
visitaturi = '<e lm="LEMMA"><i>ROOT</i><par n="visitatur/i__n"/></e>'
nimicu = '<e lm="LEMMA"><i>ROOT</i><par n="nimic/u__n"/></e>'
studenti = '<e lm="LEMMA"><i>ROOT</i><par n="studenti__n"/></e>'
manu = '<e lm="LEMMA"><i>ROOT</i><par n="man/u__n"/></e>'
citadinu = '<e lm="LEMMA"><i>ROOT</i><par n="citadin/u__n"/></e>'


beddu = '<e lm="LEMMA"><i>ROOT</i><par n="bedd/u__adj"/></e>'
eticu = '<e lm="LEMMA"><i>ROOT</i><par n="ètic/u__adj"/></e>'
facista = '<e lm="LEMMA"><i>ROOT</i><par n="fascist/a__adj"/></e>'
duci = '<e lm="LEMMA"><i>ROOT</i><par n="duci__adj"/></e>'
lariu = '<e lm="LEMMA"><i>ROOT</i><par n="lar/iu__adj"/></e>'

oggi = '<e lm="LEMMA"><i>ROOT</i><par n="oggi__adv"/></e>'


parrari = ['<e lm="LEMMA"><i>ROOT</i><par n="parr/ari__vblex"/></e>',
           '<e lm="LEMMA"><p><l>ACCENTED</l><r>ROOT</r></p><par n="pàrr/anu__vblex"/></e>']
mancari = ['<e lm="LEMMA"><i>ROOT</i><par n="manc/ari__vblex"/></e>',
           '<e lm="LEMMA"><p><l>ACCENTED</l><r>ROOT</r></p><par n="pàrr/anu__vblex"/></e>']
battiri = ['<e lm="LEMMA"><i>ROOT</i><par n="batt/iri__vblex"/></e>',
               '<e lm="ROOT"><p><l>ACCENTED</l><r>ROOT</r></p><par n="bàtt/inu__vblex"/></e>']
pigghiari = ['<e lm="LEMMA"><i>ROOT</i><par n="piggh/iari__vblex"/></e>',
             '<e lm="LEMMA"><p><l>ACCENTED</l><r>ROOT</r></p><par n="pìggh/ianu__vblex"/></e>']


def split_word(word, paradigm):
    try:
        suffix = paradigm.split("__")[0].split("n=\"")[1].split("/")[1]
    except IndexError:
        suffix = ""
    root = word
    if suffix:
        root = word[:-len(suffix)]
    return root, suffix


def build_paradigm(word, paradigm):
    root, suffix = split_word(word, paradigm)
    entry = paradigm.replace("ROOT", root).replace("LEMMA", word)
    return entry


def accented(verb):
    vocals = "aioue"
    accent = {"a": "à", "i": "ì", "u": "ù", "e": "è", "o": "ò"}
    ind = -1
    for i in range(0, len(verb)):
        if verb[i] in vocals:
            ind = i
            break
    if ind != -1:
        verb = verb[:ind] + accent[verb[ind]] + verb[ind + 1:]
    return verb



def build_verb(verb, paradigm):
    root, suffix = split_word(verb, paradigm[0])

    main_entry = paradigm[0].replace("ROOT", root).replace("LEMMA", verb)
    form_entry = paradigm[1].replace("ROOT", root).replace("LEMMA", verb)
    accented_root = accented(root)
    form_entry = form_entry.replace("ACCENTED", accented_root)

    return main_entry, form_entry

def is_accented(word):
    for symbol in "àòìùè":
        if symbol in word:
            return True
    return False

pars = {"zioni": zioni,  "ia": oriccia, "ca": ripubbrica,  "sioni": visioni, "ati": citati,
        "uti":giuvintuti, "tà": libirta, "ìa": filusufia,  "ismu": sucialismu, "uri": visitaturi}

noun_pars = {"f": {"zioni": zioni,  "ia": oriccia, "ca": ripubbrica,  "sioni": visioni,
                    "ati": citati, "uti": giuvintuti, "tà": libirta, "ìa": filusufia,
                    "a": casa, "i": matri, "u": manu},
             "m": {"iu": saccheggiu, "cu": parcu, "ismu": sucialismu, "u": annu, "a": pianeta, "i": patri},
             "m/f": {"cu": nimicu, "uri": visitaturi, "i": studenti, "a": chitarrista, "u": citadinu}}

adj_pars = {"cu": eticu, "a": facista, "i": duci, "u": beddu, "iu": lariu}

verb_pars = {"iari": pigghiari, "iri": battiri, "cari": mancari, "ari": parrari}

not_defined = []
entries = []

# You should change the separator string ----->
separator = " "

with open("word_list.txt", 'r', encoding='utf-8') as f:
    for line in f:
        checked = False
        try:
            word, PoS = line.strip().split(separator)
        except ValueError:

            word = line.strip()

            if word.endswith("ari") or word.endswith("iri"):
                for suffix in sorted(verb_pars, key=len, reverse=True):
                    pars = build_verb(word, verb_pars[suffix])
                    for par in pars:
                        entries.append(par)
                    break

            else:
                for suffix in sorted(pars, key=len, reverse=True):
                    if word.endswith(suffix):
                        entries.append(build_paradigm(word, pars[suffix]))
                        break
            continue

        if PoS in ["f", "m", 'm/f']:
            for suffix in sorted(noun_pars[PoS], key=len, reverse=True):
                if word.endswith(suffix):
                    entries.append(build_paradigm(word, noun_pars[PoS][suffix]))
                    checked = True
                    break

            if not checked:
                not_defined.append((word, PoS))
            #
            # if word.endswith("i") and 'm' in PoS:
            #     entries.append(build_paradigm(word, patri))
            # elif word.endswith("i") and 'f' in PoS:
            #     entries.append(build_paradigm(word, matri))
            # elif word.endswith("i") and "m/f" in PoS:
            #     entries.append(build_paradigm(word, visitaturi))
            # elif word.endswith("u") and "m" in PoS:
            #     entries.append(build_paradigm(word, annu))
            # elif word.endswith("cu") and "m/f" in PoS:
            #     entries.append(build_paradigm(word, nimicu))
            # elif word.endswith("a") and "f" in PoS:
            #     entries.append(build_paradigm(word, casa))
            # elif word.endswith("a") and "m" in PoS:
            #     entries.append(build_paradigm(word, pianeta))
            # elif word.endswith("a") and "m/f" in PoS:
            #     entries.append(build_paradigm(word, chitarrista))
            #
            # else:
            #     not_defined.append((word, PoS))

        elif PoS == "adj":
            for suffix in sorted(adj_pars, key=lambda x:len(x), reverse=True):
                if word.endswith(suffix):
                    entries.append(build_paradigm(word, adj_pars[suffix]))
                    checked = True
                    break

            if not checked:
                not_defined.append((word, PoS))
            else:
                continue

        elif PoS == "adv":
            entries.append(build_paradigm(word, oggi))

        elif PoS == "v":
            if is_accented(word[:-3]):
                not_defined.append((word, PoS))
                continue
            word = word.replace("ìri", "iri")

            for suffix in sorted(verb_pars, key=lambda x:len(x), reverse=True):
                if word.endswith(suffix):
                    pars = build_verb(word, verb_pars[suffix])
                    for par in pars:
                        entries.append(par)
                    checked = True
                    break

            if checked:
                continue
            else:
                not_defined.append((word, PoS))
        else:
            not_defined.append((word, PoS))


print("========================================")
for entry in entries:
    print(entry)
print()
print("========================================")
print("Undefined words: ")

for undef in not_defined:
    print(undef)