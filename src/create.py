import os
import sys

def write_to_log(message):
    print(message)
    with open("../loy_build.log", "a") as log:
        log.write(message + "\n")

def heal_workspace():
    write_to_log("[Loy Engine] Running unified ecosystem directory build...")
    
    # Generate linker.ld if missing
    linker_path = "linker.ld"
    if not os.path.exists(linker_path):
        write_to_log("[Loy Engine] Creating linker.ld script...")
        linker_content = """ENTRY(_start)
SECTIONS
{
    . = 2M;
    .text BLOCK(4K) : ALIGN(4K) { *(.multiboot) *(.text) }
    .rodata BLOCK(4K) : ALIGN(4K) { *(.rodata) }
    .data BLOCK(4K) : ALIGN(4K) { *(.data) }
    .bss BLOCK(4K) : ALIGN(4K) { *(COMMON) *(.bss) }
}"""
        with open(linker_path, "w") as f:
            f.write(linker_content)

    # Generate grub.cfg if missing
    grub_path = "../grub.cfg"
    if not os.path.exists(grub_path):
        write_to_log("[Loy Engine] Creating grub.cfg configuration...")
        grub_content = """menuentry "Lime OS (Unified Store System)" {
    multiboot /boot/limeos.bin
    boot
}"""
        with open(grub_path, "w") as f:
            f.write(grub_content)

    # Create distinct filesystem directories for real app emulation containers
    paths = [
        "../iso/limestore/google_play_subsystem/apks",
        "../iso/limestore/apple_store_subsystem/ipas",
        "../iso/limestore/microsoft_store_subsystem/exes",
        "../iso/limestore/chrome_browser_core/libs"
    ]
    for p in paths:
        os.makedirs(p, exist_ok=True)

    write_to_log("[Loy Engine] Subsystem infrastructure paths initialized.")

if __name__ == "__main__":
    for i in range(3):
        heal_workspace()
