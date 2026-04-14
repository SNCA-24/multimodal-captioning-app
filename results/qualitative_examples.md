# Qualitative Examples

Status:
- This repo does not yet include benchmark metrics or a large evaluation set.
- The examples below are the current checked-in output artifacts available from the tested API paths.
- They are useful for showing response shape and supported behavior, but they should eventually be complemented with real UI screenshots and real model outputs.

## 1. Image caption example
- Source: mocked backend API test path
- Endpoint: `POST /api/generate-image-caption`
- Example response:

```json
{
  "caption": "caption:fr"
}
```

## 2. Video caption example
- Source: mocked backend API test path
- Endpoint: `POST /api/generate-video-caption`
- Example response:

```json
{
  "captions": [
    {
      "frame": 0,
      "caption": "video-caption:es"
    }
  ]
}
```

## 3. Translated caption examples
- Translation request path is supported through the `language` form field.
- Current checked-in examples from mocked tests:
  - image request with `language=fr` -> `caption:fr`
  - video request with `language=es` -> `video-caption:es`

## 4. Known failure cases
- Dense scenes or ambiguous actions may produce weak captions.
- Video understanding is limited by simple frame sampling rather than full temporal reasoning.
- Translation output may drift from the source caption wording.
- First-run real inference may be slow because models may need to be downloaded and loaded locally.
