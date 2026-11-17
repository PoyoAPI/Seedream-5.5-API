# Seedream 5.5 API: cURL quickstart

```bash
export POYO_API_KEY="your-api-key"
export POYO_BASE_URL="https://api.poyo.ai"
```

## Text-to-image

```bash
curl -X POST "$POYO_BASE_URL/api/generate/submit" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "seedream-5.5",
  "input": {
    "prompt": "A ceramic pour-over coffee set on a walnut counter, soft morning window light, steam rising from the cup, minimalist product photography",
    "size": "16:9",
    "resolution": "2K"
  }
}'
```

## Transparent PNG

```bash
curl -X POST "$POYO_BASE_URL/api/generate/submit" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d @payloads/seedream-5.5-transparent-png.json
```

`background: transparent` needs `output_format: png`.

## Edit with a reference image

```bash
curl -X POST "$POYO_BASE_URL/api/generate/submit" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d @payloads/seedream-5.5-edit.json
```

Passing `image_urls` selects editing. `size` defaults to `auto`, which follows the reference images. Each reference image adds 1.6 credits.

## Layer decomposition

```bash
curl -X POST "$POYO_BASE_URL/api/generate/submit" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d @payloads/seedream-5.5-layerize.json
```

Returns one file per image, base image first, each with a `layer` object. Add `"text_recognition": true` for OCR on text layers.

## Check status

Save `data.task_id` from the submit response, then poll:

```bash
curl "$POYO_BASE_URL/api/generate/status/<task_id>" \
  -H "Authorization: Bearer $POYO_API_KEY"
```

For production, add a public HTTPS `callback_url` to the top-level request and make the receiver idempotent.

See the [full README](../README.md) and [production notes](../docs/production-notes.md).
