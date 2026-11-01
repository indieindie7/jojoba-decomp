// ListBlocks.java: print memory blocks with flags.
//@category JoJo
import ghidra.app.script.GhidraScript;
import ghidra.program.model.mem.*;
public class ListBlocks extends GhidraScript {
  public void run() throws Exception {
    for (MemoryBlock b : currentProgram.getMemory().getBlocks())
      println(b.getName() + " " + b.getStart() + "-" + b.getEnd() + " init=" + b.isInitialized() + " r=" + b.isRead() + " w=" + b.isWrite() + " x=" + b.isExecute() + " vol=" + b.isVolatile());
  }
}
