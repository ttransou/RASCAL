# Frontend Guide

This folder contains the static frontend served by `backend/api.py`.

## Files

- `frontend/index.html`
	- Main app shell.
- `frontend/styles.css`
	- Shared UI styling.
- `frontend/app.js`
	- Main chat/wiki interaction logic.
- `frontend/graph_map.html`
	- Graph map page.
- `frontend/graph_map.js`
	- Graph map rendering and interactions.
- `frontend/feedback_review.html`
	- Curator/feedback review page.
- `frontend/faq.json`
	- FAQ content used by the UI.

## Served Routes (via backend)

- `GET /`
- `GET /index.html`
- `GET /styles.css`
- `GET /app.js`
- `GET /graph-map`
- `GET /graph_map.js`
- `GET /feedback-review`
- `GET /faq.json`

## Notes

- The frontend is intentionally no-build-step HTML/CSS/JS for portability.
- Graph and wiki data are fetched from API endpoints in `backend/api.py`.
