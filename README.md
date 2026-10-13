# 🍄 SUPER FABLE WORLD — Yoshi's Island 2

### *One-shotted by **Claude Fable 5.1** — not 5. The point-one is the whole point.*

> **Super Mario World: Yoshi's Island 2, remade in ONE single HTML file. Zero dependencies. Zero assets. Zero build step.**
> Every sprite, every tile, every note of the soundtrack — synthesized from raw code, by a model, in one session.

<p align="center">
  <a href="https://inonono66.github.io/fable-5.1-mario/"><b>▶️ PLAY IT RIGHT NOW</b></a>
</p>

<p align="center">
  <img src="docs/gameplay.gif" width="480" alt="Autopilot gameplay">
</p>

<p align="center">
  <img src="docs/title.png" width="380" alt="Title screen">
  <img src="docs/gameplay.png" width="380" alt="Gameplay">
</p>

<p align="center">
  🎬 <a href="docs/full-run.mp4">Full no-death flagpole run (mp4, 🔊 sound on)</a> — played start-to-finish by a scripted autopilot, 22,500 pts, 3 lives intact.
  <br>The chiptune you hear is 100% WebAudio oscillators — there is no audio file anywhere in this repo.
</p>

<p align="center">
  <img alt="single file" src="https://img.shields.io/badge/files-1-e94f37?style=flat-square">
  <img alt="dependencies" src="https://img.shields.io/badge/dependencies-0-43aa8b?style=flat-square">
  <img alt="assets" src="https://img.shields.io/badge/external_assets-0-577590?style=flat-square">
  <img alt="loc" src="https://img.shields.io/badge/LOC-~1600-f9c74f?style=flat-square">
  <img alt="vanilla" src="https://img.shields.io/badge/vanilla_JS-100%25-f8961e?style=flat-square">
  <img alt="model" src="https://img.shields.io/badge/model-Claude_Fable_5.1-b5179e?style=flat-square">
</p>

---

## What is this?

Yoshi's Island 2 from Super Mario World — the meadow start, mesa hops,
turn-block bridge, staircase hill, midway gate, pipe flats and step hills
to the goal — packed into a single `index.html` you can open by
double-clicking. No `npm install`. No sprite sheets. No `.mp3` files. Just open it.
The level map and SMW sprite sheets were studied as visual reference; every
pixel you see is still hand-encoded ASCII bitmaps rendered to canvas.

**One-shotted by `claude-fable-5-1` — that's Fable 5.1, mind the minor version.**
The whole game was produced by the model in a single coding session — no human wrote
a line of it. If Fable 5 was the fairy tale, 5.1 is the one that ships playable games
in one take.

## Features

- 🗺️ **Yoshi's Island 2 layout** — message blocks, turn-block bridge over the first pit, staircase mesa, midway checkpoint gate, pipe flats, coin trails, 5 dragon coins (1UP), hidden 1-UP, flagpole & castle finish
- 🏃 **True SMW physics** — P-meter sprint, speed-indexed jumps, cape takeoff/glide/dive, spin jumps, walljump, skid smoke, −1 trick, corner boosts, shell carrying, swimming
- 🍄 **Full power-up chain** — Small → Big → Cape (feather) or Fire (flower), Starman invincibility, 1-UP mushrooms
- 👾 **Enemies** — Goombas, green + red Koopas (red never walks off ledges), 2-hit purple Rexes, Bullet Bills, stompable + kickable + carryable shells
- 🎵 **Chiptune synth engine** — the overworld theme and all SFX (coin, stomp, fireball, flagpole fanfare, hurry-up speedup at 100s) generated live with the WebAudio API. Not a single audio file
- 🎨 **Hand-encoded pixel art** — every sprite is a string-encoded bitmap rendered to canvas: SMW grass-topped ground, turn/message blocks, dragon coins, Rex, red shells, cape drape
- 📱 **Touch controls** — virtual D-pad + A/B/SPIN buttons appear automatically on mobile
- ⏸️ Pause, mute, lives, score, coin counter, 400-second timer — the whole HUD

## Controls

| Action | Keys |
|---|---|
| Move | `←` `→` / `A` `D` |
| Jump | `X` / `Space` / `↑` |
| Run / Fireball | `Z` / `Shift` |
| Crouch | `↓` |
| Start / Pause | `Enter` |
| Mute | `M` |

On touch devices, on-screen buttons show up on their own.

## Run it

```sh
git clone https://github.com/INONONO66/fable-5.1-mario.git
open fable-5.1-mario/index.html   # that's it. that's the build system.
```

Or just play the hosted version: **https://inonono66.github.io/fable-5.1-mario/**

## How it fits in one file

| Subsystem | How |
|---|---|
| Rendering | 256×240 `<canvas>`, integer-scaled, `image-rendering: pixelated` |
| Sprites | ASCII bitmap strings → offscreen canvases at boot, palette-swap for variants |
| Audio | Tiny sequencer over `OscillatorNode`s — square/triangle waves, note tables in MIDI numbers |
| Level | Tile map built procedurally with helpers (`pipe(x,h)`, `stairs(...)`, `q(x,y,'mush')`) |
| Physics | Fixed-timestep loop, tile-based AABB collision, NES-flavored accel/friction constants |
| Spawns | Camera-trigger thresholds + patrol bounds per enemy (idea from jipham510, see References) |
| Collision | Swept last-position guards so fast bodies can't tunnel (idea from jipham510 `Tile_Collision`) |
| Background | Clouds on a 0.5× parallax layer (idea from CharlesStover's `mario.js` controller) |
| SMW enemies | Bullet Bill (gravity-free flyer, stomp grounds it, bursts on landing), Dragon + purple Rex (2-hit dinos: half-flatten + speeds up, then flat), red Koopas (fast, never walk off ledges) — behaviors after jipham510's `Bullet.js`/`Dragon.js`, sprites hand-encoded from the SMW sheets to match |
| YI2 systems | Turn blocks (unbreakable bridges), message blocks with text, midway checkpoint gate with tape-drop, floating coins + 5 dragon coins (1UP), grass-topped mesa cliffs |
| Build mode | `Shift+Click` places a 2-wide pipe at the cursor (height follows click row) — after CharlesStover's `ADD_TUBE` click handler; only builds on empty tiles |
| Level data | Ground stretches + spawn list + pickup trails + midway live in one `LEVEL_DATA` table — after jipham510's JSON range level parser |
| True physics | Walk 1.25 / run 2.25 / sprint 3.0 px/f caps, P-meter (−1/+2, full at 112), speed-indexed jump table (−5.0…−6.06), held/released gravity 0.19/0.375, terminal 4.0, stomp bounce −3.0/−5.5 — exact values from the [galaxyhaxz/smw-src](https://github.com/galaxyhaxz/smw-src) disassembly (`player.s` tables `DATA_00D535`/`00D5EB`/`00D2BD`/`00D7A5`/`00D7AF`, `BoostMarioSpeed`) |
| SMW movement | 16-bit-style accel (0.094 walk / 0.125 run, 0.7× air control), skid smoke + turning pose, −1 trick kick, wall slide/catch + walljump + airborne bonk (±2.0 rebound, −2.0 pop-up), corner-boost nudge, landing dust |
| Spin jump | `C`/`V` — higher jump-table entry, poofs foes with a −0.5 hop instead of stomping (true `$F8` bounce) |
| Cape | Feather item → Cape Mario; P-speed jump arms takeoff meter 80, ascend phase, then glide (hold jump = 1.0 float cap), dive (`↓` banks speed + swoop lift), cape drape sprite + HUD takeoff gauge |
| Water | Full swim physics in-engine (strokes, surface leap −5.0, 1.5 swim cap; fire dies in water) — Yoshi's Island 2 itself has no pools, so its pits are real pits; water tiles remain for custom builds |
| Carry | Hold run to grab idle shells, run-button to throw (3.25), carried shells kill on touch |

## References

Mechanics ideas ported (not code — the implementation above stays original,
single-file, zero-dependency) from these open-source Mario engines:

- **[CharlesStover/super-mario-world-js](https://github.com/CharlesStover/super-mario-world-js)** (JS, MIT-style college project) — redux-style reducer + `Sprite` model with split `collisionX`/`collisionY` handlers, bouncing-fireball model (`verticalVelocity` reset on ground contact), parallax background scrolling at `mario.x / 2`, timer-based enemy spawns. Its Python twin **[CharlesStover/super-mario-world-py](https://github.com/CharlesStover/super-mario-world-py)** documents the same controller/reducer/view architecture.
- **[jipham510/Super-Mario-World](https://github.com/jipham510/Super-Mario-World)** (vanilla JS + canvas) — OOP `GameObject` + composable behaviors (`AutoMove` patrol limits, `SpawnEnemies` camera triggers, `Stomp` bounce), `Tile_Collision` swept resolution using last-position guards (`getLastRight`/`getLastBottom`), lethal-shell kills-other-enemies logic with kicker i-frames, and JSON range-based level parsing. Our `trigger`/`x1`/`x2` spawn fields, swept guards in `moveX`/`moveY`, shell `noHurt` + kicker `invuln` window, and moving-shell lethality follow these designs.

## 🤖 Agent Trajectory

This game was generated end-to-end by **Claude Fable 5.1** (`claude-fable-5-1`). The
full agent session trajectory — every prompt, tool call, and edit, completely
unedited — is published on Hugging Face:

> 📦 **[INONONO/fable-5.1-mario-trajectory](https://huggingface.co/datasets/INONONO/fable-5.1-mario-trajectory)**
> — raw Claude Code session log (`trajectory.jsonl`, 95 model turns / 51 user events / ~1.1 MB).
> No human wrote a line of the game; the whole prompt→tool-call→edit loop is in there.

## License

Fan-made, non-commercial educational remake. Super Mario Bros. is a trademark of
Nintendo. All original code in this repo is MIT.
