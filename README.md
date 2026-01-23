# Personal website

In large part inspired by [David Gosset](http://www.davidgosset.com)'s website.
Responsive layout partially based on the [Academic Pages](https://academicpages.github.io) theme.

Generated using the [BibtexParser](https://bibtexparser.readthedocs.io) and [Jinja](https://jinja.palletsprojects.com) packages.

Palladio URW font by (URW)++ Design & Development.
Fonts subset using [subfont](https://github.com/Munter/subfont) and [fontTools](https://fonttools.readthedocs.io).
Rights for the icons of Google Scholar, arXiv, and ORCID go to their respective owners.

## Scripts

The following scripts process content that changes frequently.
Their artifacts are not committed, they are instead run by GitHub Actions.
* `parse.py` fills in html templates, then
* `fonts.py` extracts used characters and subsets fonts.

Outputs of the following scripts do not change frequently and are directly committed.
* `favicon.sh` generates the favicon,
* `images.sh` downscales images for responsiveness.
