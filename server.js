import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;
const HOST = '0.0.0.0';

// API health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Serve static assets and pages from workspace root
app.use(express.static(__dirname, {
  extensions: ['html', 'htm'],
  index: 'index.html',
  dotfiles: 'ignore'
}));

// Catch-all fallback to index.html for SPA/root routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, HOST, () => {
  console.log(`Portfolio server running on http://${HOST}:${PORT}`);
});
