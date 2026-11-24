# Virtual Drone Shot Expert

> Turn any video into a **GTA6-style** / **Tesla Reality View–inspired** virtual drone follow shot.

[中文 README](./README.md) · [Technical background](./docs/principles.md) · [Installation](./docs/installation.md) · [Prompt examples](./docs/prompt-examples.md) · [FAQ](./docs/faq.md)

| | |
| --- | --- |
| Version | `v1.0.0` |
| Type | WorkBuddy / CodeBuddy expert package (Agent) |
| Prompt language | Simplified Chinese (metadata is bilingual) |
| License | [MIT](./LICENSE) |

---

## What this is

This is an **expert package**, not a standalone inference program. It encodes the workflow *video → virtual aerial follow shot* — analyse the subject, design a virtual camera path, synthesise a new viewpoint, suggest refinements — as an Agent prompt that the host platform executes.

```
your video ──► scene / subject / motion analysis ──► drone camera path design ──► new-viewpoint video
               (understanding)                      (cinematography)            (host video model)
```

📦 **Included**: a Chinese Agent prompt, `plugin.json` metadata, an avatar, documentation, and a packaging script.
🚫 **Not included**: model weights, inference code, training code, or any third-party API calls. **Actual video generation is provided by the video model connected to WorkBuddy / CodeBuddy.**

> ⚠️ **Expectation setting**: synthesising a physically consistent novel view from a *single ordinary video* is still an open research problem. Output is a **stylised re-imagining**: subject, motion trend, palette and lighting are preserved as far as possible, while geometry, occlusion and background details are generatively completed — not an accurate 3D reconstruction, and not Tesla's multi-camera real-time system.

---

## Styles

| Style | Look | Good for |
| --- | --- | --- |
| **GTA6 cinematic** | Third-person high follow shot, open-world saturated lighting, wide motion | Streets, parkour, driving, crowds |
| **Reality View–inspired** | Virtual camera above and behind the subject, strong path legibility | Driving, cycling, skating |
| **FPV high speed** | Low altitude, fast traversal, heavy motion blur | Sports, racing, running pets |
| **Slow orbit** | Static subject, constant-speed orbit | Portraits, products |
| **Pull-up reveal** | Close follow shot rising smoothly to a top-down view | Travel, city, events |

---

## Quick start

1. Download `virtual-drone-expert.zip` from [Releases](../../releases), or run `python scripts/build-package.py` at the repo root.
2. In WorkBuddy, open **Experts → import local expert package** and select the zip.
3. Start a conversation with *Virtual Drone Shot Expert* and upload a video.
4. Describe the shot, e.g.:

   > Convert this into a GTA6-style aerial follow shot: camera 8 m behind and 4 m above the subject, slow acceleration, pull up to a top-down view over the last 2 seconds.

See [Installation](./docs/installation.md) and [Prompt examples](./docs/prompt-examples.md).

---

## Camera parameters

Natural language is enough, but being explicit about these dimensions noticeably improves consistency.

| Parameter | Meaning | Typical values |
| --- | --- | --- |
| Height | Camera altitude | 2–3 m (FPV) / 4–8 m (follow) / 15 m+ (top-down) |
| Distance | Horizontal gap to subject | 5–15 m |
| Azimuth | Position relative to subject | Directly behind / rear 45° / above-behind / retreating front |
| Speed | Follow and camera motion | Constant / slow acceleration / fast push / hard stop |
| Focal feel | Wide to tele compression | 16–24 mm / 50–85 mm |
| Duration | Output clip length | 4–8 s recommended (longer clips drift) |
| Style | One of the five presets above | Combinations welcome |

---

## Technical background (30-second version)

In November 2026, Tesla's FSD v15 shipped **Reality View**: instead of a game engine or stitched camera feeds, an on-device generative model paints a virtual overhead camera view from multi-camera vision features. Owners and press widely described it as "like GTA6". Reported figures include a ~1B-parameter generative branch, a shared Universal Vision Encoder (UVE), 8 frames at 36 fps per generation, ~220 ms latency, and roughly half a TRIP accelerator on AI4.

This expert **borrows the visual language and workflow as a creative pattern**; it does not reproduce the technology. The input changes from *live multi-camera streams* to *a single offline video*, so the result is an artistic reconstruction rather than a visualisation of a perception system.

Full context, conflicting reports, and links: [docs/principles.md](./docs/principles.md).

---

## Limitations and compliance

- **Not a technical reproduction.** No claim of using, containing, or reproducing Tesla models, code, or data.
- **Trademarks.** `GTA6` / `Grand Theft Auto`, `Tesla`, and `Reality View` belong to their respective owners and are used here only as **descriptive references to a visual style**. This project is not affiliated with, endorsed by, or licensed by them.
- **Source material.** Only upload videos you own or are authorised to use. Check portrait rights, copyright and platform rules before publishing outputs.
- **No factual use.** Generated frames are hallucinated where data is missing — **never** use them for accident reconstruction, evidence, measurement, or any geometry-critical purpose.
- **Host-dependent quality.** Subject consistency, max duration and resolution vary by platform. See [FAQ](./docs/faq.md).

---

## Contributing

Issues and PRs are welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE) © 2026 mycode8899
