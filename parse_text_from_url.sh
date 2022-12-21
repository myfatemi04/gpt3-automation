node -e "const {parseText} = require('./parse_text_from_url.js'); parseText('$1').then(content => { console.log(content.result); });"
