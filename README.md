# PanoScene4D

WebXR Gaussian Splat viewer for PanoScene4D.

The repository stores a static WebXR viewer plus a small default demo scene. The large original training assets are not committed.

## Directory

```text
.
├── webxr_viewer/             # GitHub Pages static site
│   ├── index.html
│   ├── index.js
│   ├── index.css
│   ├── static/               # viewer UI/runtime assets
│   └── scenes/               # default compressed demo scene
│       ├── case1_static_sog/
│       └── girl_ply_seq_sam3_rotx_y135_staticworld/
└── .github/workflows/pages.yml
```

## Local Preview

```bash
cd webxr_viewer
python3 -m http.server 3000
```

Open:

```text
http://127.0.0.1:3000
```

The default page loads:

```text
./scenes/case1_static_sog/scene.sog
./scenes/girl_ply_seq_sam3_rotx_y135_staticworld/sequence.json
```

## Open Another Scene

Static splat:

```text
http://127.0.0.1:3000/?load=https://example.com/scene.sog&filename=scene.sog
```

PLY sequence:

```text
http://127.0.0.1:3000/?sequence=https://example.com/sequence.json
```

Static plus dynamic:

```text
http://127.0.0.1:3000/?load=https://example.com/static.sog&filename=static.sog&sequence=https://example.com/sequence.json
```

The scene URLs must be HTTPS and must allow browser CORS requests.

## VR Performance

The viewer starts immersive VR with a reduced framebuffer scale by default:

```text
xrScale=0.7
```

Lower values improve Quest performance at the cost of sharpness:

```text
https://panoscene4d.github.io/PanoScene4D/?xrScale=0.6
```

Use `xrScale=1` for native headset resolution if performance allows.

## GitHub Pages

Push to `main`, then enable Pages with source `GitHub Actions` in repository settings.
