# Civilization-game

This project is a simple turn-based strategy prototype. The game relies on external AI services for the automatic players. To run the game with these services you must provide API keys through environment variables:

- `OPENAI_API_KEY` or `OPENAI_KEY_V2` – used for ChatGPT.
- `GOOGLE_API_KEY` – used for Google Gemini.
- `ANTHROPIC_API_KEY` – optional, reserved for future Claude support.

You can export these variables before running the game or fill them in a file
named `api_keys.py` (see `api_keys.py` in the repository for a template):

```bash
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_API_KEY="your-google-key"
# optional
export ANTHROPIC_API_KEY="your-anthropic-key"
```

If you do not set environment variables, the game will attempt to load keys
from `api_keys.py`.

Then launch the game with `python3 main.py`.
