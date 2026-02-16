const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const imagesDir = 'public/images/theme';

const conversions = [
  // Logos PNG -> WebP
  { from: 'logo_titan.png', to: 'logo_titan.webp', w: 512 },
  { from: 'logo_nova.png', to: 'logo_nova.webp', w: 512 },
  { from: 'logo_target.png', to: 'logo_target.webp', w: 512 },
  { from: 'logo_spark.png', to: 'logo_spark.webp', w: 512 },
  { from: 'logo_lux.png', to: 'logo_lux.webp', w: 512 },
  // Hero JPG -> WebP
  { from: 'hero_titan.jpg', to: 'hero_titan.webp', w: 1920 },
  { from: 'hero_nova.jpg', to: 'hero_nova.webp', w: 1920 },
  { from: 'hero_target.jpg', to: 'hero_target.webp', w: 1920 },
  { from: 'hero_spark.jpg', to: 'hero_spark.webp', w: 1920 },
  { from: 'hero_lux.jpg', to: 'hero_lux.webp', w: 1920 },
  // Photos JPG -> WebP
  { from: 'photo_titan.jpg', to: 'photo_titan.webp', w: 800 },
  { from: 'photo_nova.jpg', to: 'photo_nova.webp', w: 800 },
  { from: 'photo_target.jpg', to: 'photo_target.webp', w: 800 },
  { from: 'photo_spark.jpg', to: 'photo_spark.webp', w: 800 },
  { from: 'photo_lux.jpg', to: 'photo_lux.webp', w: 800 },
];

async function convertImages() {
  console.log('🎨 Converting images to WebP...\n');

  for (const conv of conversions) {
    const inputPath = path.join(imagesDir, conv.from);
    const outputPath = path.join(imagesDir, conv.to);

    try {
      await sharp(inputPath)
        .resize(conv.w, null, { withoutEnlargement: true })
        .webp({ quality: 80 })
        .toFile(outputPath);

      const oldSize = fs.statSync(inputPath).size;
      const newSize = fs.statSync(outputPath).size;
      const savings = (((oldSize - newSize) / oldSize) * 100).toFixed(1);

      console.log(`✅ ${conv.from} → ${conv.to}`);
      console.log(
        `   ${(oldSize / 1024).toFixed(0)}KB → ${(newSize / 1024).toFixed(0)}KB (${savings}% smaller)`
      );
    } catch (err) {
      console.log(`❌ Error with ${conv.from}: ${err.message}`);
    }
  }

  console.log('\n✨ WebP conversion complete!');
}

convertImages();
