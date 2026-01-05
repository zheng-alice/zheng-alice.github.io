document.addEventListener('visibilitychange', () => {
	document.querySelector("link[rel='icon']")?.setAttribute('href', 'icons/' + (document.hidden ? 'favicon-inactive.svg' : 'favicon.svg'));
});
