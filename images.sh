#!/usr/bin/env bash
# Create several downscaled versions of images for responsiveness
qual=75
imgs=("profile" "head" "landscape")
profile=(200 400 600 800)
head=(125 250 375 500)
landscape=(675)
mkdir -p site/images
for img in "${imgs[@]}"; do
	declare -n ress=$img
	for res in "${ress[@]}"; do
		convert -quality $qual% templates/images/$img.jpg -geometry x$res site/images/$img$res.webp \
			&& echo "Created $img$res.webp"
	done
done
