function link(href, text) {
	document.write('<a href=\"');
	document.write(href);
	document.write('\">');
	document.write(text);
	document.write('</a>');
}

function createLink(href, text) {
	a = document.createElement("a");
	a.href = href;
	a.appendChild(document.createTextNode(text));
	return a;
}