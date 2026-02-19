import type { APIRoute } from 'astro';

// Disable prerendering for server-side API
export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
  let name = '';
  let email = '';
  let message = '';
  let language = 'en';

  const contentType = request.headers.get('content-type') || '';

  if (contentType.includes('application/json')) {
    // Handle JSON body
    const body = await request.json();
    name = body.name?.toString() || '';
    email = body.email?.toString() || '';
    message = body.message?.toString() || '';
    language = body._language?.toString() || 'en';
  } else {
    // Handle form data
    const formData = await request.formData();
    name = formData.get('name')?.toString() || '';
    email = formData.get('email')?.toString() || '';
    message = formData.get('message')?.toString() || '';
    language = formData.get('_language')?.toString() || 'en';
  }

  // Validate
  if (!name || !email || !email.includes('@')) {
    return new Response(
      JSON.stringify({
        success: false,
        error: 'Name and valid email are required',
      }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const dbPath =
    import.meta.env.DATABASE_PATH || '/var/www/projects/marketing.tvoje.info/data/contacts.db';

  try {
    const Database = await import('better-sqlite3');
    const db = new Database.default(dbPath);

    db.exec(`
      CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT,
        language TEXT DEFAULT 'en',
        status TEXT DEFAULT 'new',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        source_url TEXT
      )
    `);

    const stmt = db.prepare(`
      INSERT INTO contacts (name, email, message, language, source_url)
      VALUES (?, ?, ?, ?, ?)
    `);

    const result = stmt.run(name, email, message, language, request.url);
    const contactId = result.lastInsertRowid;
    db.close();

    return new Response(
      JSON.stringify({
        success: true,
        id: contactId,
        message: "Thank you! We'll be in touch soon.",
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Contact API error:', error);

    return new Response(
      JSON.stringify({
        success: false,
        error: 'Something went wrong. Please try again.',
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};

export const GET: APIRoute = () => {
  return new Response(JSON.stringify({ status: 'ok', endpoint: 'contact-form-api' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};
