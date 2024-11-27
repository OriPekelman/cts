#!/bin/bash

CORPORA=(abraham acts-pilate AP besa-letters bohairic-habakkuk bohairic-life-isaac bohairic.1corinthians bohairic.mark bohairic.nt bohairic.ot book-bartholomew coptic-treebank doc-papyri dormition-john helias johannes-canons john-constantinople lament-mary life-aphou life-cyrus life-eustathius-theopiste life-john-kalybites life-longinus-lucius life-onnophrius life-paul-tamma life-phib life-pisentius magical-papyri martyrdom-victor mercurius mysteries-john pachomius-instructions pistis-sophia proclus-homilies pseudo-athanasius-discourses pseudo-basil pseudo-celestinus pseudo-chrysostom pseudo-ephrem pseudo-flavianus pseudo-theophilus pseudo-timothy sahidic.ot sahidic.ruth sahidica.1corinthians sahidica.mark sahidica.nt shenoute-a22 shenoute-considering shenoute-crushed shenoute-dirt shenoute-eagerness shenoute-errs shenoute-fox shenoute-house shenoute-listen shenoute-night shenoute-place shenoute-prince shenoute-seeks shenoute-those shenoute-thundered shenoute-true shenoute-uncertain-xr shenoute-unknown5_1 shenoute-witness theodosius-alexandria)
for CORPUS in "${CORPORA[@]}"; do
    python manage.py addcorpus  --source=local --local-repo-path=../../corpora  "$CORPUS"
done
