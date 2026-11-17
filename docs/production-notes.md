# Seedream 5.5 API production notes

## Confirmed contract

- Endpoint: `POST /api/generate/submit`
- Model IDs: `seedream-5.5`, `seedream-5.5-layerize`
- Authentication: `Authorization: Bearer <POYO_API_KEY>`
- Status: `GET /api/generate/status/{task_id}`

## Input limits

| Field | Requirement | Constraint |
| --- | --- | --- |
| prompt (seedream-5.5) | required | 5–5,000 characters. |
| image_urls (seedream-5.5) | optional | 1–10 public JPEG, PNG, or WebP URLs, up to 10 MB each; array even for one image. |
| size | optional | 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9, or auto (editing). Default 1:1 / auto. |
| resolution (seedream-5.5) | optional | 1K, 1.5K, or 2K; default 2K. |
| background | optional | auto (default), transparent (needs png), or opaque. |
| output_format | optional | png (default) or jpeg. |
| image_urls (layerize) | required | Exactly 1 public JPEG or PNG, up to 10 MB, 512×512 to 6000×6000, aspect ratio 1:16 to 16:1. |
| prompt (layerize) | optional | Up to 2,000 characters. |
| resolution (layerize) | optional | 1K, 1.5K, 2K, or auto (default; billed as 2K). |
| max_images | optional | 2–100 including the base image; default 30. Balance must cover max_images at submission. |
| text_recognition | optional | Default false. |
| enable_safety_checker | optional | Default true. |

## Operational checklist

- Keep API keys in a server-side secret manager.
- Validate user input before calling the API.
- Persist `data.task_id` immediately after submission.
- Use five-second polling only for development; prefer `callback_url` in production.
- Make webhook processing idempotent and reconcile status before fulfilling an order.
- Copy output files to durable storage after the task finishes.
- Recheck the live model page before hard-coding prices.

## Failure handling

Treat non-2xx HTTP responses and non-success API `code` values as errors. Preserve the HTTP status, API code, and a redacted response body for debugging.

Schema: [PoYo API documentation](https://docs.poyo.ai/api-manual/image-series/seedream-5-5?utm_source=github&utm_medium=readme&utm_campaign=seedream-5.5-api)
