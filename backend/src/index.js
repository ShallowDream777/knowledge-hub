import { createApp } from './app.js';

const PORT = process.env.PORT || 1906;
const { app } = createApp();

app.listen(PORT, () => {
  console.log(`knowledge-hub server listening on http://localhost:${PORT}`);
});
