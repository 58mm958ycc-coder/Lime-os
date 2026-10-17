import os
import sys

def write_to_log(message):
    print(message)
    with open("../loy_build.log", "a") as log:
        log.write(message + "\n")

def heal_workspace():
    write_to_log("[Loy Engine] Starting self-healing workspace scan...")
    
    # 1. Automatically generate linker.ld if missing in src/
    linker_path = "linker.ld"
    if not os.path.exists(linker_path):
        write_to_log("[Loy Engine] Missing linker.ld! Generating layout dynamically...")
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

    # 2. Automatically generate grub.cfg if missing in project root
    grub_path = "../grub.cfg"
    if not os.path.exists(grub_path):
        write_to_log("[Loy Engine] Missing grub.cfg! Generating boot config dynamically...")
        grub_content = """menuentry "Lime OS (Unified Store System)" {
    multiboot /boot/limeos.bin
    boot
}"""
        with open(grub_path, "w") as f:
            f.write(grub_content)

    # 3. Dynamic setup for Lime Store file allocation paths
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
    # Runs workspace normalization loops
    for i in range(2):
        heal_workspace()
