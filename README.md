# Seedream 5.5 API: cURL, Python, and Node.js Examples

[![Seedream 5.5 on PoYo](https://img.shields.io/badge/Try%20on%20PoYo-seedream--5.5-84cc16)](https://poyo.ai/models/seedream-5-5?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api) [![API docs](https://img.shields.io/badge/API-docs-22d3ee)](https://docs.poyo.ai/api-manual/image-series/seedream-5-5?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api) [![Check](https://github.com/PoyoAPI/Seedream-5.5-API/actions/workflows/check.yml/badge.svg)](https://github.com/PoyoAPI/Seedream-5.5-API/actions/workflows/check.yml)

Runnable examples for ByteDance Seed **Seedream 5.5** through PoYo's async image API: text-to-image, editing with up to 10 reference images, native transparent PNGs, and layer decomposition into a base image plus up to 99 transparent layers.

**Answer:** To use the Seedream 5.5 API, send a server-side request to `POST https://api.poyo.ai/api/generate/submit` with model `seedream-5.5` (or `seedream-5.5-layerize` for layers) and a PoYo API key, then poll `GET https://api.poyo.ai/api/generate/status/{task_id}`. The examples in this repository run with Python 3.9+, Node.js 22+, or cURL.

Last verified against the live PoYo schema and pricing on **November 17, 2026**.

## Seedream 5.5 at a glance

- **Model IDs:** `seedream-5.5` (generate and edit), `seedream-5.5-layerize` (layer decomposition)
- **Released:** November 9, 2026 by ByteDance Seed
- **Editing:** the same model ID; add 1–10 reference images in `image_urls`
- **Output:** one image per request, 8 aspect ratios at 1K, 1.5K, or 2K (default 2K, up to 3136×1344 at 21:9), PNG or JPEG
- **Transparency:** `background: "transparent"` returns an RGBA PNG
- **Layers:** a base image plus up to 99 transparent PNG layers, with optional OCR for text layers
- **Price:** from 4 credits ($0.02) per image at 1K or 1.5K and 7 credits ($0.035) at 2K, plus 1.6 credits ($0.008) per reference image

## Quickstart

1. Create a key in the [PoYo dashboard](https://poyo.ai/dashboard/api-key?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api).
2. Copy `.env.example` to `.env` and replace the placeholder.
3. Run one of the examples. Each submits the task and polls until `finished` or `failed`.

```dotenv
POYO_API_KEY=YOUR_POYO_API_KEY_HERE
POYO_BASE_URL=https://api.poyo.ai
```

### Python

```bash
python python/generate.py
python python/generate.py payloads/seedream-5.5-transparent-png.json
```

[`python/generate.py`](python/generate.py) uses only the Python standard library.

### Node.js

```bash
node node/index.mjs
node node/index.mjs payloads/seedream-5.5-layerize.json
```

### cURL

```bash
curl -X POST "https://api.poyo.ai/api/generate/submit" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d @payloads/seedream-5.5-text-to-image.json
```

Status polling and the other modes are in [curl/generate.md](curl/generate.md).

## Example requests

Every file in [`payloads/`](payloads) is a complete request body with public input media, so it runs as-is.

| File | Mode | Settings | Credits |
| --- | --- | --- | --- |
| [`seedream-5.5-text-to-image.json`](payloads/seedream-5.5-text-to-image.json) | Text-to-image | 16:9, 2K (2816×1584) | 7 ($0.035) |
| [`seedream-5.5-transparent-png.json`](payloads/seedream-5.5-transparent-png.json) | Transparent sticker | 1:1, 1K, RGBA PNG | 4 ($0.02) |
| [`seedream-5.5-edit.json`](payloads/seedream-5.5-edit.json) | Edit, 1 reference image | 2K, `size` auto | 8.6 ($0.043) |
| [`seedream-5.5-layerize.json`](payloads/seedream-5.5-layerize.json) | Layer decomposition | 1K, `max_images: 10` | 4 per returned image + 1.6; at most 41.6 ($0.208) |

## Input modes

| Model ID | Mode | Selected when |
| --- | --- | --- |
| `seedream-5.5` | Image editing | `image_urls` has 1–10 URLs |
| `seedream-5.5` | Text-to-image | `image_urls` is omitted |
| `seedream-5.5-layerize` | Layer decomposition | Always; `image_urls` holds exactly one image |

Refer to reference images in the prompt by order (image 1, image 2, and so on), and say what changes and what stays the same. For multi-turn editing, pass the previous result back as the next reference image; regions you leave out of the prompt stay the same.

## Request fields

### `seedream-5.5`

| Field | Requirement | Meaning |
| --- | --- | --- |
| prompt | required | 5–5,000 characters. |
| image_urls | optional | 1–10 public JPEG, PNG, or WebP URLs, up to 10 MB each. Selects editing. Always an array. |
| size | optional | `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`, or `auto` (editing). Default `1:1` for text-to-image, `auto` for editing. |
| resolution | optional | `1K`, `1.5K`, or `2K`. Default `2K`. |
| background | optional | `auto` (default), `transparent` (needs `png`), or `opaque`. |
| output_format | optional | `png` (default) or `jpeg`. |
| enable_safety_checker | optional | Default `true`. |

### `seedream-5.5-layerize`

| Field | Requirement | Meaning |
| --- | --- | --- |
| image_urls | required | Exactly one public JPEG or PNG, up to 10 MB, 512×512 to 6000×6000 pixels, aspect ratio between 1:16 and 16:1. |
| prompt | optional | How to split the image, up to 2,000 characters. Without it, the model puts each main element on its own layer. |
| resolution | optional | `1K`, `1.5K`, `2K`, or `auto` (default). `auto` is billed as 2K. |
| max_images | optional | 2–100 output images including the base image. Default 30. |
| text_recognition | optional | Return OCR for regular text layers in `layer.text_recognition`. Default `false`. |
| output_format | optional | Base image format, `png` (default) or `jpeg`. Layers are always transparent PNG. |
| enable_safety_checker | optional | Default `true`. |

## Pricing

Billing is per image. 1 credit = $0.005.

| Model | 1K / 1.5K | 2K | Add-on |
| --- | --- | --- | --- |
| `seedream-5.5` | 4 credits ($0.02) | 7 credits ($0.035) | 1.6 credits ($0.008) per image in `image_urls` |
| `seedream-5.5-layerize` | 4 credits ($0.02) per returned image | 7 credits ($0.035) per returned image (`auto` bills as 2K) | 1.6 credits ($0.008) for the input image |

Layer decomposition charges for the images actually returned, base image included. Your balance must cover `max_images` images when you submit. Credits are charged only when the task succeeds. Confirm current prices on the [model page](https://poyo.ai/models/seedream-5-5?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api).

## Writing Seedream 5.5 prompts

- **Say what stays:** for edits, list what must not change (subject, camera angle, lighting) as well as the change.
- **Transparent assets:** describe an isolated subject "on a transparent background" and set `background` to `transparent` with `output_format` `png`.
- **Iterate opaque, finish transparent:** keep intermediate edit rounds at `auto` or `opaque` and switch to `transparent` for the final cut-out.
- **Guide the layers:** name the elements that should get their own layer, and turn on `text_recognition` when the image has editable copy.

## Async production flow

```text
submit -> persist data.task_id -> poll during development -> receive callback_url webhook in production
```

Treat `finished` and `failed` as terminal states. Each finished layer task lists one file per image, base image first; every file carries a `layer` object with `z_index`, a name, a description, and a `bounding_box`. Copy outputs to your own storage after the task finishes.

## FAQ

**How much does the Seedream 5.5 API cost?** 4 credits ($0.02) at 1K or 1.5K and 7 credits ($0.035) at 2K, plus 1.6 credits per reference image, so a 2K edit with one reference costs 8.6 credits.

**How many layers can Seedream 5.5 return?** Up to 99 layers plus the base image (`max_images` up to 100). The model returns as many as the image needs.

**Do I need a separate model ID for editing?** No. Add `image_urls` to a `seedream-5.5` request.

**Can it make transparent PNGs from a text prompt?** Yes. Set `background` to `transparent` and `output_format` to `png`, with or without reference images.

**How long does a request take?** In PoYo tests in November 2026, a `seedream-5.5` image took about 24 seconds on average; layer decomposition returning 3 to 13 images took about 18 to 47 seconds. Times vary with load and settings.

## Repository map

- [`payloads/`](payloads) — complete request bodies for each mode
- [`python/generate.py`](python/generate.py) — standard-library Python example
- [`node/index.mjs`](node/index.mjs) — dependency-free Node.js example
- [`curl/generate.md`](curl/generate.md) — copy-paste cURL requests
- [`docs/production-notes.md`](docs/production-notes.md) — limits and rollout checklist

## Related repositories

- [Seedream-5.0-Pro-API](https://github.com/PoyoAPI/Seedream-5.0-Pro-API) — Seedream 5.0 Pro for dense layouts and multilingual text
- [MiniMax-H3-Image-API](https://github.com/PoyoAPI/MiniMax-H3-Image-API) — 1K–4K images with up to 16 references
- [awesome-poyo-api](https://github.com/PoyoAPI/awesome-poyo-api) — every PoYo model repository in one list
- [poyo-devtools](https://github.com/PoyoAPI/poyo-devtools) — PoYo CLI, MCP bridge, and Agent Skill

## Links

- [Seedream 5.5 API on PoYo](https://poyo.ai/models/seedream-5-5?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api)
- [Seedream 5.5 API reference](https://docs.poyo.ai/api-manual/image-series/seedream-5-5?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api)
- [Seedream 5.5 layer decomposition reference](https://docs.poyo.ai/api-manual/image-series/seedream-5-5-layerize?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api)
- [PoYo model catalog](https://poyo.ai/models?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api)

## License

MIT
