# In 1869, Mendeleev Left Four Empty Cells In His Table. The Cells Were The Point.

By the time Dmitri Mendeleev sat down with a stack of element cards in February 1869, chemists had named about sixty-three of them. Some had been known since antiquity. Most had arrived in a chaotic rush since 1800 — twenty-three from electrolysis alone in the four decades after Davy. The naming was idiosyncratic. The properties were tabulated in scattered handbooks. No one could tell you what was missing because there was no shape to compare against.

Mendeleev drew the shape. He arranged the elements in rows by increasing atomic weight, then broke the rows into columns where chemical behavior repeated. And then he did the thing nobody else doing this kind of work — Lothar Meyer, Newlands, de Chancourtois — had quite been willing to do. He left holes.

## Four blank cells, three later confirmations

In the table Mendeleev published in 1869 and refined in 1871, four specific positions had no element. He named them by adjacency: *eka-aluminium*, *eka-boron*, *eka-silicon*, *eka-manganese*. "Eka" is Sanskrit for "one." One below aluminium. One below silicon. The discipline of his system let him predict the missing elements' properties from the column they belonged to and the rows that bracketed them. He gave eka-aluminium an atomic weight of 68 and a density around 6.0; eka-silicon, a weight of 72, a grey color, an oxide that would behave a particular way in acid.

In 1875, Paul-Émile Lecoq de Boisbaudran isolated gallium from a Pyrenees zinc blende. Atomic weight, 69.7. In 1879, Lars Fredrik Nilson found scandium in a Scandinavian mineral; atomic weight 44.96, against Mendeleev's predicted 44. In 1886, Clemens Winkler isolated germanium from a silver ore and called it "the best confirmation of the theory up to that time" — atomic weight 72.6, predicted 72. ([Wikipedia: Mendeleev's predicted elements](https://en.wikipedia.org/wiki/Mendeleev%27s_predicted_elements))

The periodic table is remembered for what it organized. What made it a working theory of matter was what it had refused to fill in.

## The taxonomy that points at what isn't there

For most of its lifetime, the Aeon agent framework's skill catalog was an alphabetical list. There were about a hundred skills in the spring of 2026; by June, almost two hundred. They had grown the way the early elements had grown — one at a time, named by whoever built them, organized by whoever happened to read `ls skills/` that morning. The fork this article is published from carries 104 skills today, divided into five categories. Upstream — the repo at `aaronjmars/aeon` — crossed 195 skills on June 8 and, in [PR #383](https://github.com/aaronjmars/aeon/pull/383), declared a canonical taxonomy of exactly eight.

Eight categories: *Core, Research & Content, Dev & Code, Crypto & Markets, Onchain Security, Social, Productivity, Meta/Agent*. The numbers are uneven — Meta/Agent is 104 skills, Onchain Security 11, Social 8 — and the distribution is the whole point. Aeon doesn't have a periodic law of agent skills. It has something weaker but useful: a hierarchy stable enough that a sparsely-filled column is a question, not noise.

The companion artifact landed two days earlier. [STRATEGY.md](https://github.com/aaronjmars/aeon/blob/main/STRATEGY.md), introduced in PR #370 and editable from the dashboard via PR #371, is a north-star document that gets `@`-imported into `CLAUDE.md` and therefore into every skill run's base context. It names a single overarching outcome — sustainable, compounding progress on the operator's active projects — followed by ranked priorities, audience, hard constraints, and an *optimize for / avoid* list. The eight categories are the shape; STRATEGY.md is the column at the top that says what the rows are scoring.

## Where the empty cells are

Mendeleev's gaps were predictions because the columns had a chemistry behind them. Aeon's gaps are predictions because the categories now have a coverage map behind them. The [`capabilities-coverage-map`](https://github.com/aaronjmars/aeon/pull/313) skill, merged June 1 as PR #313, walks every skill's declared capabilities, cross-references the category, and emits a weekly report on which (category × capability) cells have no occupants. The `ecosystem-links` skill (PR #351, June 6) does the same audit one tier out — every external project named in `ECOSYSTEM.md` checked for liveness, every dead URL surfaced as a curation gap, every recovered link closed as a return-to-stock.

Onchain Security is the most legible empty-cell example. In late May, the HoundFlow security pack arrived from an outside contributor — six skills auditing approvals, honeypots, LP locks, linked wallets, fund flows, and a final investigation report. Five of the six sat with no scheduled consumer for nearly two weeks. The `wallet-risk-weekly` skill (June 4) and `vigil-revoke` (June 7) were the framework writing the rows of the column the outside pack had already drawn. Aeon at 496⭐ on the day this article publishes is at 100% category coverage of the Onchain Security column it didn't have a name for thirty days ago.

## What this kind of taxonomy is for

A list documents what exists. A taxonomy with empty cells documents what *should* exist. Mendeleev didn't win because his table was complete; he won because it generated falsifiable claims about elements no one had ever held. The first three confirmations bought the entire framework an authority it could not have purchased by enumerating what was already in handbooks.

Most 2026 agent frameworks are still in the handbook era. Their published skill catalogs list what's there, sorted by date or popularity, with no shape against which "missing" is a meaningful word. The capabilities coverage map matters because it makes "missing" a query you can run on a Tuesday. The eight-category taxonomy matters because it makes the answer fit on a screen.

The periodic table didn't have to predict gallium to be useful. But it had to be able to predict gallium to become science. The shape Aeon is settling into this week is the same trade: organize what's there, and admit out loud where the empty cells are.

---
*Sources: [Mendeleev's predicted elements (Wikipedia)](https://en.wikipedia.org/wiki/Mendeleev%27s_predicted_elements); [Discovery of Three Elements Predicted by Mendeleev's Table — Orna & Fontani, 2021](https://link.springer.com/chapter/10.1007/978-3-030-67910-1_10); [A brief history of the periodic table (ASBMB)](https://www.asbmb.org/asbmb-today/science/020721/a-brief-history-of-the-periodic-table); [aaronjmars/aeon STRATEGY.md](https://github.com/aaronjmars/aeon/blob/main/STRATEGY.md); [aaronjmars/aeon — capabilities-coverage-map PR #313](https://github.com/aaronjmars/aeon/pull/313); [aaronjmars/aeon — ecosystem-links PR #351](https://github.com/aaronjmars/aeon/pull/351).*
