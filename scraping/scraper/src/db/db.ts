// db.ts
import { createPool } from 'mysql2/promise';

export const pool = createPool({
  host: 'localhost',
  user: 'root',
  password: '1234',
  database: 'yourDatabaseName',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

export async function saveArticle(article: {
    site_id: string;
    title: string;
    url: string;
    date: string;
    content: string;
  }) {
    const sql = `
      INSERT INTO articles (site_id, title, url, date, content)
      VALUES (?, ?, ?, ?, ?)
      ON DUPLICATE KEY UPDATE
      title = VALUES(title),
      content = VALUES(content),
      date = VALUES(date);
    `;
    const { site_id, title, url, date, content } = article;
    await pool.execute(sql, [site_id, title, url, date, content]);
  }
  