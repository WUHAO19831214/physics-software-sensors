import {
  NumberOCRSensor,
  RecordedNumberRecognizer,
  Vector3Assembler,
  YANAN_CLASSROOM_TO_SCENE,
  componentFromNumberOcrEvent,
  createVector3RenderModel,
} from '../../packages/typescript/dist/src/index.js';

const axes = ['x', 'y', 'z'];
const inputs = document.querySelector('#inputs');
for (const [axis, value] of [['x', 0], ['y', 1.2], ['z', -0.8]]) {
  const label = document.createElement('label');
  label.innerHTML = `<strong>${axis}</strong><input id="${axis}" type="number" step="0.01" value="${value}"><select id="${axis}-source"><option>observed</option><option>derived</option><option>constrained</option><option>default</option><option>missing</option></select>`;
  inputs.append(label);
}
document.querySelector('#x-source').value = 'constrained';

const assembler = new Vector3Assembler({ maxComponentSkewMs: 150 });
const canvas = document.querySelector('#scene');
const context = canvas.getContext('2d');

function manualComponent(axis, timestampMs) {
  const source = document.querySelector(`#${axis}-source`).value;
  if (source === 'missing') return { source };
  return { value: Number(document.querySelector(`#${axis}`).value), source, timestampMs };
}

function show(result, mode) {
  document.querySelector('#mode').textContent = mode;
  document.querySelector('#status').textContent = result.status;
  document.querySelector('#flags').textContent = result.flags.join(', ');
  if (!result.measurement) {
    for (const id of ['magnitude', 'azimuth', 'elevation']) document.querySelector(`#${id}`).textContent = 'incomplete';
    document.querySelector('#details').textContent = JSON.stringify({ missing: result.missingComponents }, null, 2);
    context.clearRect(0, 0, canvas.width, canvas.height);
    return;
  }
  const measurement = result.measurement;
  document.querySelector('#magnitude').textContent = measurement.magnitude.toFixed(4);
  document.querySelector('#azimuth').textContent = measurement.direction ? `${measurement.direction.azimuthDeg.toFixed(2)}°` : 'undefined';
  document.querySelector('#elevation').textContent = measurement.direction ? `${measurement.direction.elevationDeg.toFixed(2)}°` : 'undefined';
  document.querySelector('#details').textContent = JSON.stringify(measurement.componentDetails, null, 2);
  draw(createVector3RenderModel(measurement, YANAN_CLASSROOM_TO_SCENE));
}

function draw(model) {
  context.clearRect(0, 0, canvas.width, canvas.height);
  const origin = { x: canvas.width / 2, y: canvas.height / 2 };
  const max = Math.max(1, ...model.arrows.map((arrow) => Math.hypot(arrow.to.x, arrow.to.y, arrow.to.z)));
  const scale = 220 / max;
  const project = ({ x, y, z }) => ({ x: origin.x + (x - z * 0.55) * scale, y: origin.y - (y - z * 0.28) * scale });
  context.setLineDash([8, 8]); context.strokeStyle = '#54677d'; context.lineWidth = 2;
  for (const axis of model.axes) {
    const to = project({ x: axis.direction.x * max, y: axis.direction.y * max, z: axis.direction.z * max });
    context.beginPath(); context.moveTo(origin.x, origin.y); context.lineTo(to.x, to.y); context.stroke();
    context.fillStyle = '#8ea5bd'; context.font = '15px system-ui'; context.fillText(axis.label, to.x + 5, to.y + 5);
  }
  context.setLineDash([]);
  const colors = { 'x-component': '#ff6b6b', 'y-component': '#4ecdc4', 'z-component': '#ffd166', resultant: '#ffffff' };
  for (const arrow of model.arrows) {
    const from = project(arrow.from); const to = project(arrow.to);
    context.strokeStyle = colors[arrow.id]; context.fillStyle = colors[arrow.id]; context.lineWidth = arrow.id === 'resultant' ? 6 : 3;
    context.beginPath(); context.moveTo(from.x, from.y); context.lineTo(to.x, to.y); context.stroke();
    const angle = Math.atan2(to.y - from.y, to.x - from.x);
    context.beginPath(); context.moveTo(to.x, to.y); context.lineTo(to.x - 14 * Math.cos(angle - .45), to.y - 14 * Math.sin(angle - .45)); context.lineTo(to.x - 14 * Math.cos(angle + .45), to.y - 14 * Math.sin(angle + .45)); context.closePath(); context.fill();
    context.font = '16px system-ui'; context.fillText(`${arrow.label} (${arrow.source ?? 'sum'})`, to.x + 8, to.y - 8);
  }
}

document.querySelector('#manual').addEventListener('click', () => {
  show(assembler.compose({
    quantity: 'generic', unit: '1', coordinateSystem: 'manual-classroom-xyz',
    components: Object.fromEntries(axes.map((axis, index) => [axis, manualComponent(axis, 1000 + index * 20)])),
  }), 'Manual input');
});

function frame() {
  return {
    frameId: 'recorded-yanan-frame', runId: 'demo-replay', sequence: 0,
    observedAt: '2026-06-04T12:54:03.000Z', monotonicNs: 1_000_000, sourceTimestamp: 1000,
    sourceSensorId: 'screen.capture', media: { kind: 'screen-frame', width: 1920, height: 1080, mediaType: 'image/png', colorSpace: 'RGBA' },
    artifactUri: 'fixture://yanan/recorded-frame.png',
  };
}

async function replayOcr(roiId, rawText, confidence) {
  const recognizer = new RecordedNumberRecognizer([{ frameId: frame().frameId, roiId, result: { method: 'recorded', rawText, confidence, durationMs: 40 } }]);
  const sensor = new NumberOCRSensor(recognizer, `demo-${roiId}`);
  sensor.configure({ roiId, roi: { x: 0, y: 0, width: .5, height: .5 }, name: roiId, symbol: roiId, unit: 'N' });
  await sensor.start({ runId: 'demo-replay' });
  return sensor.processFrame(frame());
}

document.querySelector('#replay').addEventListener('click', async () => {
  const [fy, fz] = await Promise.all([replayOcr('Fy', '-2.33', .94), replayOcr('Fz', '0.50', .91)]);
  const components = {
    x: { value: 0, source: 'constrained', quality: { flags: ['yanan-apparatus-plane-constraint'] } },
    y: componentFromNumberOcrEvent(fy), z: componentFromNumberOcrEvent(fz),
  };
  for (const axis of axes) {
    if (components[axis].value !== undefined) document.querySelector(`#${axis}`).value = components[axis].value;
    document.querySelector(`#${axis}-source`).value = components[axis].source;
  }
  show(assembler.compose({ quantity: 'force', unit: 'N', coordinateSystem: 'yanan-classroom-x-y-z', components }), 'Recorded OCR: Fy/Fz observed; Fx constrained to zero');
});

document.querySelector('#manual').click();
