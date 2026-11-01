# JoJo HFTF (CPS3, jojoba) decomp notes

## ROM
- Set `jojoba` (Euro, no-CD BIOS). SIMM1 (4 x 2 MB) = program at 0x06000000, SIMM2 (4 x 2 MB) at 0x06800000 = more code + character data; SIMM3-5 = graphics.
- Each SIMM bank = 4 chips byte-interleaved into big-endian dwords.
- Encryption: MAME `cps3_mask` (rotxor), per-game keys for jojoba 0x23323ee3 / 0x03021972; dword ^= mask(address). `tools/cps3dec.py` does both steps. Check: first dwords of SIMM1 = reset PC 0x06001668, SP 0x02080000.

## Ghidra
- JOJOBA.BIN = decrypted SIMM1 + SIMM2 (16 MB), SuperH:BE:32:SH-2 at 0x06000000.
- `FindSh2FunctionsMem.java` + `CreateAt.java`: 2,662 functions (code 0x06000000..~0x061Cxxxx; a few at 0x0624xxxx may be data).
- `CsDumpAll.java` dump -> `tools/splitdump.py dump.c naming/JOJO 10` -> 10 slices named with `ghidra/naming/prompt_JOJO.txt`.

## RAM (from public MAME training-mode scripts)
- Objects 0x420 apart: P1 ~0x02034800, P2 +0x420, P1 stand +0x840, P2 stand +0xC60. obj+0x1CD = health (players) / stand gauge (stands).
- Super meter 0x02034863 / 0x02034887. HUD mirrors 0x0205BB28.. (hp, combo count, stand hp, meter).

## Rounds
- Round 1 (2026-11-01): all 2,662 named, 1,727 provisional.
- Next: provisional review with callers (ckprovctx.py -> verdicts -> srprovapply.py), then data tables (move bytecode / frame records, compare with the PS1 format doc).
