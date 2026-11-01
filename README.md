# JoJo's Bizarre Adventure: Heritage for the Future (CPS3 arcade, jojoba) reverse-engineering notes and symbols

Hand-named function map, naming inputs and tools for the Capcom CPS3 arcade fighter **JoJo's Bizarre Adventure:
Heritage for the Future** (1999, set `jojoba`, SH-2). Round 1 = one naming pass over every function of the program
(SIMM1 + SIMM2 flash, decrypted, loaded at 0x06000000):

| Program | Functions | Hand-named | Still `provisional` |
|---|---|---|---|
| JOJOBA.BIN (simm1 + simm2 at 0x06000000) | 2,662 | 2,662 | 20 (after round 3) |

0 placeholder (`FUN_`) names left. Round 2 (11-01): all 1,727 provisional names re-read with callers/callees context by Sonnet agents (13 parts, prompt + verdicts in `ghidra/review/`): 992 confirmed, 551 renamed, 184 still unsure. Round 3 (11-01): those 184 re-read with current callee names + callers (`tools/provctx3.py`, verdicts `ghidra/review/r3_JJ_*_rv.txt`): 4 confirmed, 160 renamed (mostly generic `plyr_UpdateMisc_N` placeholders), 20 still `provisional`.

Subsystems named (prefixes): player and character logic (`plyr_`, `chr_`), stands (`stand_`), hits and collision
(`hit_`), objects and effects (`obj_`, `fx_`, `efx*_`), sprites and graphics (`spr_`, `gfx_`, `anim_`), HUD / UI
(`hud_`, `ui_`, `txt_`), rounds and game flow (`round_`, `game_`, `scene_`, `demo_`), sound (`snd_`), input
(`input_`), tasks and system (`task_`, `sys_`), debug and test menus (`dbg_`, `test_`).

Prior art: the PS1 port has a static recomp ([MenuuTUX/jojo-hftf-native](https://github.com/MenuuTUX/jojo-hftf-native))
whose `docs/ANIMATION_FORMAT.md` describes the move bytecode; this repo covers the arcade build, which had no
public decomp.

Same method as [robotica-decomp](https://github.com/indieindie7/robotica-decomp): SIMMs decrypted with the public
MAME CPS3 algorithm (`tools/cps3dec.py`), functions by SH-2 prologue scan, a decompile dump cut into slices, each
slice named from its code (prompt in `ghidra/naming/`), names applied as USER_DEFINED labels; next, every provisional
name is re-read with its callers (`tools/ckprovctx.py`, verdicts applied with `tools/srprovapply.py`).
Non-commercial, done for study (fighting-game stand / combo design reference).

**No game data is included**: no ROMs, no BIOS, no decrypted images, no decompiled C, no game text, no Ghidra
database. You need your own dump of the board to use any of this.

## What is here

| Path | Content |
|---|---|
| `NOTES.md` | ROM layout, decryption, Ghidra setup, RAM map, rounds, what comes next |
| `ghidra/hand_JOJOBA.txt` | hand names: `0x<addr> func <name> hand <comment>` (apply with ApplyNames.java from the Scorcher / AMOK repos, hand mode) |
| `ghidra/funcinfo_JOJOBA.tsv` | per-function export: `F` address name source size, `C` callees (string rows removed) |
| `ghidra/naming/prompt_JOJO.txt` | the round-1 naming prompt |
| `ghidra/review/` | round-2 review prompt + verdict lines (`JJ 0x<addr> <old> CONFIRM/RENAME/UNSURE <new> <reason>`) |
| `ghidra/scripts/` | `FindSh2FunctionsMem.java` (SH-2 prologue scan), `CreateAt.java`, `CsDumpAll.java` (decompile dump with headers) |
| `tools/` | `cps3dec.py` (SIMM de-interleave + CPS3 decrypt), `splitdump.py` (cut the dump into slices), `ckprovctx.py`, `srprovapply.py`, `pubfuncinfo.py` |

## Licence

Notes, names and tools: MIT (see `LICENSE`). JoJo's Bizarre Adventure belongs to its rights holders (Capcom,
Araki / Shueisha); nothing from the game is distributed here.
