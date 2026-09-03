# LEEKed IN 1.0

Clean rebuild of the GramLeek game prototype.

## Stack

- Phaser 4.2.1
- TypeScript 7.0.2
- Vite 8.2.2
- Telegram Mini App bridge (minimal shell for now)

## First vertical slice

This build intentionally uses generated placeholder textures. It proves the architecture and combat loop before the art pass:

- Menu -> game -> result scene flow
- WASD / arrow movement
- Pointer aim
- Continuous auto-fire
- One BOT enemy type
- Arcade Physics walls and collisions
- Hit feedback, camera shake and simple death shards
- Score + kills in a dedicated run state
- Telegram haptic bridge when running inside a Mini App

## Local development

```bash
npm install
npm run dev
```

Production check:

```bash
npm run build
```

## Build order

1. Stabilize this player/BOT combat slice.
2. Add touch movement + touch aim designed for Telegram WebView.
3. Port remaining enemy behaviours and the three-act run.
4. Add canonical HD pixel-art assets and Tiled maps.
5. Add audio and juice pass.
6. Wire Telegram start parameters / challenge links.
7. Port Supabase leaderboard.
8. Only after the game is stable: design and test token-burn mechanics.

Current public GramLeek prototype remains separate and untouched.
