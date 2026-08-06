/**
 * scripts/lib/svg-optimizer.js
 *
 * Wraps SVGO. Preserves named <g id="layer-*"> groups (see prompts/README.md
 * "layered" spec field) so animation hooks defined in the Design System's
 * motion guidelines (§23) survive optimization instead of being merged/flattened away.
 */

const { optimize } = require('svgo');

const SVGO_CONFIG = {
  multipass: true,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          // Never strip IDs — layered illustrations rely on stable
          // layer-* group IDs for CSS/JS animation targeting.
          cleanupIds: false,
          removeViewBox: false,
        },
      },
    },
    'removeDimensions', // rely on viewBox for responsive scaling instead of fixed width/height
  ],
};

function optimizeSvg(svgString) {
  const result = optimize(svgString, SVGO_CONFIG);
  return result.data;
}

module.exports = { optimizeSvg };
