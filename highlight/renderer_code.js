const dirPath = __dirname
const hljs = require(dirPath + '/highlight.pack.js');
const fs = require('fs');
const readline = require('readline')
const language = process.argv.splice(2)[0]
var fReadName = dirPath + '/transform/before.html'
var fWriteName = dirPath + '/transform/after.html'
var fRead = fs.createReadStream(fReadName)
var fWrite = fs.createWriteStream(fWriteName)
var objReadline = readline.createInterface({
    input: fRead,
    terminal: true
});
var data = ''
objReadline.on('line', (line) => {
    data += line + "\n"
});
objReadline.on('close', () => {
    var highlightedCode = ''
    if (language == null) {
        highlightedCode = hljs.highlightAuto(data).value;
    } else {
        highlightedCode = hljs.highlight(languageName = language, code = data).value;
    }
    fWrite.write(highlightedCode)
})