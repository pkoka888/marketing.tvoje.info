const fs = require('fs');
let c = fs.readFileSync('./src/i18n/translations.ts', 'utf8');
c = c.replace(/ai/g, 'campaigns');
c = c.replace(/web/g, 'content');
c = c.replace(/infrastructure/g, 'analytics');
fs.writeFileSync('./src/i18n/translations.ts', c);
