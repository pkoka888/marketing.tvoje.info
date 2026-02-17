const fs = require('fs'); const c = fs.readFileSync('src/i18n/translations.ts', 'utf8'); console.log(c.includes('devops') ? 'HAS DEVOPS' : 'NO DEVOPS');  
