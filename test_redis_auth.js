import Redis from 'ioredis';

const passwords = [
  process.env.REDIS_PASSWORD,
  'marketing',
  'marketing.tvoje.info',
  'marketing-tvoje-info',
  'marketing_tvoje_info',
  'marketingpass',
  'marketing_pass',
  'marketing-pass',
  'marketing123',
  'admin',
  'root',
  'password',
  '123456',
  'redis',
  'redis123',
  'tvoje.info',
  'tvoje-info',
  'tvoje_info',
].filter(Boolean);

async function checkPassword(password) {
  console.log(`Testing password: ${password}`);
  const redis = new Redis({
    port: 6379,
    host: 'localhost',
    password: password,
    showFriendlyErrorStack: true,
    lazyConnect: true,
    maxRetriesPerRequest: 0,
    connectTimeout: 2000,
  });

  try {
    await redis.connect();
    console.log(`✅ SUCCESS! Password is: ${password}`);
    await redis.quit();
    process.exit(0);
  } catch (err) {
    if (redis.status === 'ready') await redis.quit();
    else redis.disconnect();

    if (err.message.includes('NOAUTH') || err.message.includes('WRONGPASS')) {
      console.log(`❌ Failed: ${password}`);
    } else {
      console.error(`⚠️ Error: ${err.message}`);
    }
  }
}

async function run() {
  for (const p of passwords) {
    await checkPassword(p);
  }
  console.log('❌ All passwords failed.');
  process.exit(1);
}

run();
