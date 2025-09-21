# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: FastAPI app (`main.py`), routers (`backend/routers`), data models (`backend/models`), schemas (`backend/schemas`), and config (`backend/core/database.py`). Serves static media from `../media` at `/media`.
- `frontend/`: Static site (`index.html`, `css/style.css`, `js/app.js`). Uses `live-server` for local dev.
- `scripts/`: Utility downloaders (Instagram/Douyin) and renamers. Not required to run the app.

## Build, Test, and Development Commands
- Backend:
  - `cd backend && pip install -r requirements.txt`
  - Dev server: `uvicorn main:app --reload --port 8001` (or `python main.py`)
- Frontend:
  - `cd frontend && npm install`
  - Start: `npm run dev` (serves on `http://localhost:3000`, calls API on `http://localhost:8001`)
- Scripts (optional): `python scripts/douyin_user_downloader.py --help`

## Coding Style & Naming Conventions
- Python: PEP 8, 4‑space indent, `snake_case` for functions/variables, type hints where feasible. Keep endpoints slim; place logic in routers/models.
- JS/CSS/HTML: 2‑space indent, single quotes, `const/let` over `var`. Keep DOM IDs/classes descriptive.
- Tools: Prefer Black and Ruff for `backend/` and `scripts/`; Prettier for `frontend/` (if installed).

## Testing Guidelines
- Framework: pytest + httpx. Place tests in `backend/tests/` named `test_*.py` (e.g., `backend/tests/test_gallery.py`).
- Install: `pip install pytest httpx`
- Run: `pytest -q`
- Aim to cover routers (gallery, timeline, messages) and configuration edge cases.

## Commit & Pull Request Guidelines
- Commits in history are short and imperative (EN/ZH). Prefer Conventional Commits going forward: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`.
- Pull Requests include:
  - Clear summary and rationale; linked issues.
  - Screenshots/GIFs for `frontend/` changes.
  - Local run steps and any `.env`/DB notes.

## Security & Configuration Tips
- Backend reads `.env` (in `backend/`) via pydantic‑settings. Example:
  ```
  DATABASE_URL=sqlite:///./zhaolusi.db
  ADMIN_API_KEY=change-me
  MEDIA_ROOT=../media
  MEDIA_URL=/media/
  ```
- If backend host/port changes, update `frontend/js/app.js` `API_BASE_URL` and `MEDIA_BASE_URL`.
