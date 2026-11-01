// ResolvePools.java <ramlo hex> <ramhi hex> [dry]: SH-2 literal pools -> RAM globals.
// Adds an uninitialized RW block "ram" over [lo,hi) when unmapped, sets ROM blocks read-only (constant pools then
// resolve in the decompiler), and types every pool slot read by code whose 32-bit value lies in [lo,hi) as a pointer.
//@category JoJo
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.data.PointerDataType;
import java.util.*;
public class ResolvePools extends GhidraScript {
  public void run() throws Exception {
    String[] a = getScriptArgs();
    long lo = Long.parseLong(a[0], 16), hi = Long.parseLong(a[1], 16);
    boolean dry = a.length > 2 && a[2].equals("dry");
    Memory mem = currentProgram.getMemory();
    if (!mem.contains(toAddr(lo)) && !dry) {
      MemoryBlock b = mem.createUninitializedBlock("ram", toAddr(lo), hi - lo, false);
      b.setRead(true); b.setWrite(true);
    }
    for (MemoryBlock b : mem.getBlocks())
      if (b.isInitialized() && !dry) { println("ro " + b.getName() + " w=" + b.isWrite() + " x=" + b.isExecute()); b.setWrite(false); }
    Set<Address> slots = new TreeSet<>();
    InstructionIterator it = currentProgram.getListing().getInstructions(true);
    while (it.hasNext()) {
      Instruction in = it.next();
      for (Reference r : in.getReferencesFrom()) {
        if (!r.getReferenceType().isRead()) continue;
        Address s = r.getToAddress();
        if (s.getOffset() % 4 != 0 || !mem.contains(s)) continue;
        try { long v = mem.getInt(s) & 0xffffffffL; if (v >= lo && v < hi) slots.add(s); } catch (Exception e) {}
      }
    }
    int typed = 0, bad = 0; Set<Long> targets = new HashSet<>();
    for (Address s : slots) {
      targets.add(mem.getInt(s) & 0xffffffffL);
      if (dry) continue;
      try {
        Data d = getDataAt(s);
        if (d != null && d.isPointer()) { typed++; continue; }
        clearListing(s, s.add(3)); createData(s, new PointerDataType()); typed++;
      } catch (Exception e) { bad++; }
    }
    println("pools: slots " + slots.size() + ", typed " + typed + ", failed " + bad + ", distinct RAM targets " + targets.size() + (dry ? " (dry)" : ""));
  }
}
