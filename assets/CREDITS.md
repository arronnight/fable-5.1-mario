# Sprite credits

The game art in `assets/cut/` is cut out of fan sprite-sheet rips. The
original pixels are Nintendo's; the rips below did the extraction work.
**Fan-made, non-commercial, educational use only** — same terms as the repo.

| File | Sheet | Ripped by | Via |
|---|---|---|---|
| `mario-5.png` | Super Mario Land 2: Six Golden Coins — Mario (Small / Mario / Fire / Bunny, space & dark variants, misc, custom) | **Mister Man** | [Mario Universe SML2 sheets](https://www.mariouniverse.com/sprites-gb-sml2/) ([tSR asset 54604](https://www.spriters-resource.com/game_boy_gbc/sml2/asset/54604/), "Only For TSR — Please don't steal") |
| `mario-6.png` | Super Mario Land 2 — Mario set, white background | **BADASSDILL** ("PLEASE GIVE CREDIT") | [Mario Universe SML2 sheets](https://www.mariouniverse.com/sprites-gb-sml2/) |
| `mario-7.png` | Super Mario Land 2 — Mario set, orange background | **Mister Man** | [Mario Universe SML2 sheets](https://www.mariouniverse.com/sprites-gb-sml2/) |
| `sml2-enemies.png` | Super Mario Land 2 — Enemies ("Give credit if used") | **A.J. Nitro** | [Mario Universe SML2 sheets](https://www.mariouniverse.com/sprites-gb-sml2/) |
| `smw-goombas.png` | Super Mario World — Goomba (Yellow / Blue / Red / Green "Goombob" / Goombetty) | **NES Boy** (NESBoy215@aol.com) | [Mario Universe SMW sheets](https://www.mariouniverse.com/sprites-snes-smw/) |
| `smw-koopas.png` | Super Mario World — Koopas (Green / Red / Blue / Yellow / Black / Gold / Turquoise / Silver) | **ARMA** (7/27/2005–7/3/2005) | [Mario Universe SMW sheets](https://www.mariouniverse.com/sprites-snes-smw/) |

These sheets stand in for the three reference sheets: the Mister Man SML2
Mario compilation, the Tonberry2k SMW enemies compilation (whose Goomba and
Koopa sections are the NES Boy / ARMA rips used here), and the BADASSDILL
SML2 set.

Cut frames (`assets/cut/*.png`, see `assets/manifest.json`) were produced
with `tools/cut_sprites.py` — flood-fill background removal + bounding-box
extraction + transparent trim. Re-run anytime:

```sh
python3 tools/cut_sprites.py cut assets/manifest.json assets
```
