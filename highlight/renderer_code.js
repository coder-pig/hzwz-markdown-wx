const hljs = require('./highlight.pack');
hljs.configure()
const highlightedCode = hljs.highlightAuto('private static byte[] loadIndexes(Context context) {\n' +
    '        byte[] indexes = null;\n' +
    '\n' +
    '        InputStream is = null;\n' +
    '        try {\n' +
    '            is = context.getAssets().open(ASSET);\n' +
    '\n' +
    '            indexes = new byte[(END - START + 1) * 2];\n' +
    '\n' +
    '            is.read(indexes);\n' +
    '        } catch (Throwable tr) {\n' +
    '            PartnerLogger.d(tr.getMessage());\n' +
    '\n' +
    '            indexes = null;\n' +
    '        } finally {\n' +
    '            if (is != null) {\n' +
    '                try {\n' +
    '                    is.close();\n' +
    '                } catch (IOException e) {\n' +
    '                    PartnerLogger.d(e.getMessage());\n' +
    '                }\n' +
    '            }\n' +
    '        }\n' +
    '\n' +
    '        return indexes;\n' +
    '    }').value;
console.log(highlightedCode);