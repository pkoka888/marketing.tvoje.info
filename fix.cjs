const fs = require('fs'); 
let c = fs.readFileSync('src/i18n/translations.ts', 'utf8');  
c = c.replace(/all: string;  devops: string;/, 'all: string;\n      strategy: string;');  
