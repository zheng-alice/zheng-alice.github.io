#!/usr/bin/env bash
# Generate svg favicon from standalone latex document
for jobname in favicon favicon-inactive; do
	latex -jobname $jobname favicon.tex
	svg="site/icons/$jobname.svg"
	dvisvgm --no-fonts $jobname.dvi -o $svg
	for ext in aux dvi log; do
		rm $jobname.$ext
	done
	inkscape --actions "page-fit-to-selection" --export-plain-svg --export-overwrite $svg
	xmlstarlet ed -L -u '/_:svg/@width' -v '16px' -u '/_:svg/@height' -v '16px' $svg
done
