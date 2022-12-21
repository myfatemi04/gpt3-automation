const fetch = require("node-fetch").default;
const jsdom = require("jsdom");
const readability = require("@mozilla/readability");

async function parseText(url) {
	const controller = new AbortController();
	let text;
	const id = setTimeout(() => controller.abort(), 15000);
	try {
		text = await (await fetch(url, {
			headers: {
				'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
			},
			signal: controller.signal
		})).text();
		clearTimeout(id);
	} catch (e) {
		return { "error": "timeout" }
	}
	const virtualConsole = new jsdom.VirtualConsole();
	const jdom = new jsdom.JSDOM(text, { virtualConsole });
	const document = jdom.window.document;
	const r = new readability.Readability(document);
	const result = r.parse();
	if (result) {
		return { "result": result.textContent.trim() };
	} else {
		return { "error": ".parse() failed" };
	}
}

module.exports = {
	parseText,
}
