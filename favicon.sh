#!/usr/bin/env bash
for jobname in favicon favicon-inactive; do
	latex -jobname $jobname favicon.tex
	dvisvgm --no-fonts $jobname.dvi -o site/icons/$jobname.svg
	for ext in aux dvi log; do
		rm $jobname.$ext
	done
done
