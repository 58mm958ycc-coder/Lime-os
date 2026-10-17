import os
import sys

def write_to_log(message):
    print(message)
    with open("../loy_build.log", "a") as log:
        log.write(message + "\n")

def heal_workspace():
    write_to_log("[Loy Engine] Starting self-healing workspace scan...")
    
    # 1. Automatically generate linker.ld if missing
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

    # 2. Automatically generate grub.cfg if missing in root
    grub_path = "../grub.cfg"
    if not os.path.exists(grub_path):
        write_to_log("[Loy Engine] Missing grub.cfg! Generating boot config dynamically...")
        grub_content = """menuentry "Lime OS (Unified Store System)" {
    multiboot /boot/limeos.bin
    boot
}"""
        with open(grub_path, "w") as f:
            f.write(grub_content)

    # 3. Patch missing hashtag compiler error in parser.c
    parser_path = "parser.c"
    if os.path.exists(parser_path):
        with open(parser_path, "r") as f:
            content = f.read()
        if "include <stddef.h>" in content and not "#include <stddef.h>" in content:
            write_to_log("[Loy Engine] Patching missing '#' symbol in parser.c preprocessor include...")
            content = content.replace("include <stddef.h>", "#include <stddef.h>")
            with open(parser_path, "w") as f:
                f.write(content)

    write_to_log("[Loy Engine] All files verified. Workspace ready for large-payload ISO compilation.")

if __name__ == "__main__":
    # Standard compilation environment preparation loop iteration
    loop_count = 0
    while loop_count < 3:
        heal_workspace()
        loop_count += 1
