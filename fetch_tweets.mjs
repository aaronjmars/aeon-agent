import { env } from 'process';

const apiKey = env.XAI_API_KEY || '';
const url = 'https://api.x.ai/v1/responses';

const payload = {
  model: 'grok-4',
  input: [{
    role: 'user',
    content: 'Search X/Twitter for recent tweets (last 7 days, March 29 to April 5 2026) about the AEON crypto token on Base chain (contract 0xbf8e8f0e8866a7052f948c16508644347c57aba3 or cashtag AEON). Only return tweets about this specific cryptocurrency, not unrelated uses of the word aeon. Prioritize interesting, insightful, or highly-engaged posts. For each tweet include: handle, full text, date, likes, retweets, and direct URL. Return as a numbered list of up to 10 tweets.'
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
