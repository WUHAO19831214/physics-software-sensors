import { BrowserScreenBackend, ScreenCaptureSource } from '../../packages/typescript/dist/src/capture/screen.js';

const start = document.querySelector('#start');
const stop = document.querySelector('#stop');
const status = document.querySelector('#status');
const canvas = document.querySelector('#preview');
let source = null;

start.addEventListener('click', async () => {
  source = new ScreenCaptureSource(new BrowserScreenBackend());
  source.configure({ requestedIntervalMs: 500 });
  try {
    await source.start({ runId: `manual-browser-${Date.now()}` });
    start.disabled = true;
    stop.disabled = false;
    for await (const frame of source.read()) {
      canvas.width = frame.pixels.width;
      canvas.height = frame.pixels.height;
      canvas.getContext('2d').putImageData(new ImageData(frame.pixels.data, frame.pixels.width, frame.pixels.height), 0, 0);
      status.textContent = JSON.stringify({ frameId: frame.frameId, media: frame.media, capture: frame.payload.capture, health: source.health() }, null, 2);
    }
  } catch (error) {
    status.textContent = `${error.code ?? 'SCREEN_CAPTURE_ERROR'}: ${error.message}`;
  }
});

stop.addEventListener('click', async () => {
  await source?.stop();
  start.disabled = false;
  stop.disabled = true;
});
