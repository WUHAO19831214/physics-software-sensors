# Web Vector Compose 3D demo

This deliberately small browser app proves that `vector.compose-3d` works outside the Yan'an teacher UI. It has two deterministic modes:

- **Manual**: edit x/y/z and their source semantics.
- **Recorded OCR**: replays the current Yan'an shape, with Fx constrained to zero and Fy/Fz produced by two `NumberOCRSensor` instances.

Build the TypeScript package, then serve the repository root:

```bash
cd packages/typescript
npm run build
cd ../..
python3 -m http.server 8000
```

Open `http://localhost:8000/examples/web-vector-compose-3d/`. The app imports the built OCR and Vector3 library modules directly; it does not contain a second vector implementation and does not require a browser bundler. The canvas is a minimal renderer-neutral projection, not the original Three.js classroom interface.
