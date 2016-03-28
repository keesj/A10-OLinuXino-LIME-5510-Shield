#!/bin/sh
set -x 
set -e 
set -o
make clean

mkdir -p _build
git clone git@github.com:keesj/A10-OLinuXino-LIME-5510-Shield.git -b  gh-pages _build/html
(
cd _build/html
rm -rf *
)
make html
touch _build/html/.nojekyll

(
cd _build/html
git add -A .
)
echo 'now "git commit and git push"'
