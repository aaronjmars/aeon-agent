import { env } from 'process';
import fs from 'fs';

const apiKey = env.XAI_API_KEY || '';
const url = 'https://api.x.ai/v1/responses';

const payload = {
  model: 'grok-4',
  input: [{
    role: 'user',
    content: 'Search for recent tweets about the $AEON crypto token on Base chain (contract address 0xbf8e8f0e8866a7052f948c16508644347c57aba3). Only return tweets about this specific cryptocurrency — not any other meaning of aeon. Date range: 2026-03-30 to 2026-04-06. Return 10 tweets — prioritize the most interesting, insightful, or highly-engaged posts. For each tweet include: @handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list.'
  }],
  tools: [{ type: 'x_search' }]
};

const resp = await fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + apiKey
  },
  body: JSON.stringify(payload)
});

const result = await resp.json();

// Save full JSON
fs.writeFileSync('xai_result.json', JSON.stringify(result, null, 2));

const textParts = [];
for (const item of (result.output || [])) {
  if (item.type === 'message') {
    for (const content of (item.content || [])) {
      if (content.type === 'output_text') {
        textParts.push(content.text);
      }
    }
  }
}

if (textParts.length > 0) {
  console.log(textParts.join('\n'));
} else {
  console.log(JSON.stringify(result, null, 2));
}
