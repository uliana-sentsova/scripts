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

beddu = '<e lm="LEMMA"><i>ROOT</i><par n="bedd/u__adj"/></e>'
eticu = '<e lm="LEMMA"><i>ROOT</i><par n="ètic/u__adj"/></e>'
facista = '<e lm="LEMMA"><i>ROOT</i><par n="fascist/a__adj"/></e>'
duci = '<e lm="LEMMA"><i>ROOT</i><par n="duci__adj"/></e>'

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


noun_pars = {"zioni": zioni, "iu": saccheggiu, "ia": oriccia, "ca": ripubbrica, "cu": parcu, "sioni": visioni,
                  "ìa": filusufia, "ati": citati, "uti": giuvintuti, "tà": libirta, "ismu": sucialismu}
adj_pars = {"cu": eticu, "a": facista, "i": duci}

verb_pars = {"iari": pigghiari, "iri": battiri, "cari": mancari}

not_defined = []
entries = []

separator = " "
with open("word_list.txt", 'r', encoding='utf-8') as f:
    for line in f:
        word, PoS = line.strip().split(separator)

        checked = False

        if PoS == "n":
            for suffix in noun_pars:
                if word.endswith(suffix):
                    entries.append(build_paradigm(word, noun_pars[suffix]))
                    checked = True

            if checked:
                continue

            if word.endswith("i"):
                not_defined.append((word, PoS))
            elif word.endswith("u"):
                entries.append(build_paradigm(word, annu))
            elif word.endswith("a"):
                entries.append(build_paradigm(word, casa))
            else:
                not_defined.append((word, PoS))

        elif PoS == "adj":
            for suffix in adj_pars:
                if word.endswith(suffix):
                    entries.append(build_paradigm(word, adj_pars[suffix]))
                    checked = True

            if checked:
                continue

            if word.endswith("u"):
                entries.append(build_paradigm(word, beddu))
            else:
                not_defined.append((word, PoS))

        elif PoS == "adv":
            entries.append(build_paradigm(word, oggi))

        elif PoS == "v":
            for suffix in verb_pars:
                if word.endswith(suffix):
                    pars = build_verb(word, verb_pars[suffix])
                    for par in pars:
                        entries.append(par)
                    checked = True

            if checked:
                continue

            if word.endswith("ari"):
                pars = build_verb(word, parrari)
                for par in pars:
                    entries.append(par)
        else:
            not_defined.append(word)


print("========================================")
for entry in entries:
    print(entry)
print()
print("========================================")
print("Undefined words: ")

for undef in not_defined:
    print(undef)