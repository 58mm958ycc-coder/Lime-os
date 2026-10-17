import os
import sys

def write_to_log(message):
    print(message)
    with open("../loy_build.log", "a") as log:
        log.write(message + "\n")

def process_image_assets():
    """Locates the custom splash logo and transforms it to an uncompressed BMP framework."""
    assets_dir = "../assets"
    target_boot_dir = "../iso/boot"
    os.makedirs(target_boot_dir, exist_ok=True)

    logo_source = None
    # Scan for common input structures dropped by the user
    for filename in ["logo.png", "logo.jpg", "logo.jpeg"]:
        potential_path = os.path.join(assets_dir, filename)
        if os.path.exists(potential_path):
            logo_source = potential_path
            break

    if logo_source:
        write_to_log(f"[Loy Engine] Found branding asset at: {logo_source}")
        try:
            from PIL import Image
            img = Image.open(logo_source)
            
            # Downscale resolution matching the kernel's graphic frame buffer mode targets
            img_resized = img.resize((1024, 768))
            
            # Export as clean uncompressed 24-bit Windows Bitmap
            output_bmp_path = os.path.join(target_boot_dir, "logo.bmp")
            img_resized.save(output_bmp_path, format="BMP")
            write_to_log(f"[Loy Engine] Successfully converted graphic framework -> {output_bmp_path}")
        except Exception as e:
            write_to_log(f"[Loy Engine] Error transforming image asset: {str(e)}")
    else:
        write_to_log("[Loy Engine] Warning: No source file found inside assets/ folder layout. Staging fallback block color indexes.")

def heal_workspace():
    write_to_log("[Loy Engine] Starting workspace diagnostic sweep...")
    
    # 1. Generate linker.ld if dropped from src/
    if not os.path.exists("linker.ld"):
        with open("linker.ld", "w") as f:
            f.write("""ENTRY(_start)
SECTIONS
{
    . = 2M;
    .text BLOCK(4K) : ALIGN(4K) { *(.multiboot) *(.text) }
    .rodata BLOCK(4K) : ALIGN(4K) { *(.rodata) }
    .data BLOCK(4K) : ALIGN(4K) { *(.data) }
    .bss BLOCK(4K) : ALIGN(4K) { *(COMMON) *(.bss) }
}""")

    # 2. FIXED: Automatically generates the graphics-enabled grub.cfg if missing
    if not os.path.exists("../grub.cfg"):
        with open("../grub.cfg", "w") as f:
            f.write("""insmod vbe
insmod vga
insmod video_bochs
insmod video_cirrus

set gfxmode=1024x768x32
set gfxpayload=keep

menuentry "Lime OS (Unified Store System)" {
    multiboot /boot/limeos.bin
    boot
}""")

    # Standard distribution path preparations
    paths = [
        "../iso/limestore/google_play_subsystem/apks",
        "../iso/limestore/apple_store_subsystem/ipas",
        "../iso/limestore/microsoft_store_subsystem/exes",
        "../iso/limestore/chrome_browser_core/libs"
    ]
    for p in paths:
        os.makedirs(p, exist_ok=True)

if __name__ == "__main__":
    for i in range(2):
        heal_workspace()
    # Execute the graphical asset pipeline compilation
    process_image_assets()
