def pandocket(soup):
	for table in soup.find_all("table", class_="site-menu"):
		table.decompose()
	soup.find("table", class_="page-menu").decompose()
	return soup
