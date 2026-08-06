/**
 * scripts/lib/image-generator.js
 *
 * Provider-agnostic adapter for AI image generation.
 *
 * Design decision: rather than hard-coding one vendor's SDK, this module
 * exposes a single generateImage() function that POSTs a normalized request
 * to whichever endpoint is configured via environment variables. This keeps
 * the asset pipeline swappable across providers (and testable/mockable)
 * without touching any calling script.
 *
 * Configure via .env (see .env.example):
 *   IMAGE_API_URL      - full endpoint URL for the provider's image generation API
 *   IMAGE_API_KEY       - bearer token / API key
 *   IMAGE_API_PROVIDER  - free-text label, used only for logging/debugging
 *
 * If these are not configured, generateImage() throws a clear, actionable
 * error rather than failing silently or producing a placeholder file —
 * silently shipping a missing/blank asset would violate the "no missing
 * assets" requirement more than a loud, explicit failure would.
 */

const fs = require('fs');
const path = require('path');
const { loadStyleConstraints } = require('./shared-style');

async function generateImage({ prompt, format = 'svg', width, height, layered = false }) {
  const apiUrl = process.env.IMAGE_API_URL;
  const apiKey = process.env.IMAGE_API_KEY;
  const provider = process.env.IMAGE_API_PROVIDER || 'unconfigured';

  if (!apiUrl || !apiKey) {
    throw new Error(
      '[image-generator] IMAGE_API_URL and IMAGE_API_KEY must be set in .env before ' +
      'assets can be generated. This is an execution dependency, not a missing design ' +
      'decision — every prompt, filename, and destination path is already fully specified ' +
      'in /prompts. See prompts/README.md for details.'
    );
  }

  const { palette, styleConstraints, layeredInstruction } = loadStyleConstraints();

  const fullPrompt = [
    prompt,
    styleConstraints,
    `Color palette (strict): ${palette.join(', ')}.`,
    layered ? layeredInstruction : null,
  ]
    .filter(Boolean)
    .join(' ');

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      prompt: fullPrompt,
      format,
      width,
      height,
    }),
  });

  if (!response.ok) {
    const body = await response.text().catch(() => '');
    throw new Error(
      `[image-generator] Provider "${provider}" request failed: ${response.status} ${response.statusText}. ${body}`
    );
  }

  // Expected response contract: { data: <base64 or raw SVG string>, contentType: string }
  // Adjust this parsing block to match your chosen provider's actual response shape —
  // this is the one piece that is necessarily provider-specific.
  const result = await response.json();
  return {
    data: result.data,
    contentType: result.contentType || (format === 'svg' ? 'image/svg+xml' : 'image/png'),
  };
}

function writeGeneratedAsset(outputPath, data, contentType) {
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  if (contentType === 'image/svg+xml') {
    fs.writeFileSync(outputPath, data, 'utf-8');
  } else {
    fs.writeFileSync(outputPath, Buffer.from(data, 'base64'));
  }
}

module.exports = { generateImage, writeGeneratedAsset };
