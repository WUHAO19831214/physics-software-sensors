import { pathToFileURL } from 'node:url';
import path from 'node:path';
import { syntheticRuler } from '../packages/fringelab/dist/tests/fixtures/scenes.js';

/** Same deterministic inputs can exercise fixed source .ts or built package .js. */
export async function runGolden(directory, extension = '.js') {
  const load = name => import(pathToFileURL(path.join(directory, name + extension)).href);
  const [signal, optics, simulator, ruler, roi, spatial, calculator, detection, analysis] = await Promise.all(['signal','physics','simulator','ruler','roi','spatial','calculator','ruler-detection','analysis'].map(load));
  const simulation = simulator.simulateDiffraction({ kind: 'double-slit', width: 320, height: 100, mmPerPixel: .08, slitWidthMm: .04, slitSeparationMm: .25, screenDistanceM: 1.5, wavelengthNm: 650, seed: 9173, noiseStd: .008, gamma: 1.2, saturationLevel: .9 });
  const region = { centerX: 160, centerY: 50, width: 290, height: 24, angleDeg: 7 };
  const profile = signal.extractStripProfile(simulation.frame, { roi: region, channel: 'auto' });
  const smooth = signal.gaussianSmooth(profile.profile, 1.8);
  const manual = { start: { x: 20, y: 40 }, end: { x: 120, y: 40 }, knownLengthMm: 10 };
  const anchors = [{ x: 0, y: 0, mm: 0 }, { x: 100, y: 0, mm: 10 }, { x: 220, y: 0, mm: 20 }];
  const observations = [-2,-1,0,1,2].map(order => ({ order, screenPositionM: order * .0039 }));
  const rulerResults = [
    { body: [235,235,230], ink: [18,18,18] },
    { body: [25,30,35], ink: [230,235,235] },
    { body: [220,190,50], ink: [20,20,20], angleDeg: 12 },
    { body: [235,235,230], ink: [18,18,18], perspective: 2.5, missing: new Set([7,8,23]) },
  ].map(options => { const result = detection.detectPhysicalRuler(syntheticRuler(options), { sourceType: 'image' }); if (result) delete result.createdAt; return result; });
  const result = {
    calculator: ['(12+8)/5','2^3^2','-2^2','2^-2','1e-3*10^9'].map(calculator.calculateExpression),
    roi: roi.resizeRoiFromCorner(region, 'se', { x: 300, y: 90 }, { minWidth: 20, minHeight: 10, maxWidth: 320, maxHeight: 100 }),
    ruler: { scale: ruler.calculateMmPerPixel(manual), ticks: ruler.generateRulerTicks(manual), detection: rulerResults },
    spatial: anchors.map(p => spatial.mapScreenPointMm({ x: p.x + 15, y: 30 }, anchors)),
    simulation: { truth: simulation.truthProfile, encoded: simulation.encodedProfile },
    profile,
    features: { smooth, peaks: signal.detectPeaks(smooth, { minProminence: 2, minDistance: 12 }), troughs: signal.detectTroughs(smooth, { minProminence: 2, minDistance: 12 }), period: signal.estimatePeriodAutocorrelation(smooth), fwhm: signal.calculateFwhm(smooth, 145) },
    optics: optics.fitDoubleSlitOrders({ observations, screenDistanceM: 1.5, slitSeparationM: .00025, centerPositionM: 0 }),
    analysis: analysis.analyseFrame(simulation.frame, { experiment: 'double', channel: 'auto', orientation: 'vertical', roi: region, mmPerPixel: .08, screenDistanceM: 1.5, slitWidthMm: .04, slitSeparationMm: .25, apertureUncertaintyMm: .002, distanceUncertaintyM: .005, calibrationUncertaintyPct: 1, referenceWavelengthNm: 650, smoothingSigma: 1.8, background: null, measurementReady: true }),
  };
  return JSON.parse(JSON.stringify(result, (_key, value) => ArrayBuffer.isView(value) ? Array.from(value) : value));
}
if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  console.log(JSON.stringify(await runGolden(process.argv[2], process.argv[3] ?? '.js'), null, 2));
}
