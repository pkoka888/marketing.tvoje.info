const fs = require('fs');  
let c = fs.readFileSync('./src/i18n/translations.ts', 'utf8');  
c = c.replace(/devops/g, 'strategy');  
fs.writeFileSync('./src/i18n/translations.ts', c);  
