#define SCREEN_WIDTH  1024
#define SCREEN_HEIGHT 768

// Multiboot Information Structure schema mapping
struct multiboot_info {
    unsigned int flags;
    unsigned int mem_lower;
    unsigned int mem_upper;
    unsigned int boot_device;
    unsigned int cmdline;
    unsigned int mods_count;
    unsigned int mods_addr;
    unsigned int syms[4];
    unsigned int mmap_length;
    unsigned int mmap_addr;
    unsigned int drives_length;
    unsigned int drives_addr;
    unsigned int config_table;
    unsigned int boot_loader_name;
    unsigned int apm_table;
    unsigned int vbe_control_info;
    unsigned int vbe_mode_info;
    unsigned short vbe_mode;
    unsigned short vbe_interface_seg;
    unsigned short vbe_interface_off;
    unsigned short vbe_interface_len;
    
    // Dynamic Frame Buffer Fields
    unsigned int   framebuffer_addr_high;
    unsigned int   framebuffer_addr_low; // This contains the true physical video hardware address!
    unsigned int   framebuffer_pitch;
    unsigned int   framebuffer_width;
    unsigned int   framebuffer_height;
    unsigned char  framebuffer_bpp;
    unsigned char  framebuffer_type;
};

struct __attribute__((packed)) BMPHeader {
    unsigned short signature;     
    unsigned int   file_size;
    unsigned short reserved1, reserved2;
    unsigned int   data_offset;   
};

// Global system pointer targeting dynamic physical memory layers
unsigned int* target_video_framebuffer = 0;

void draw_pixel(int x, int y, unsigned int color) {
    if (target_video_framebuffer != 0) {
        target_video_framebuffer[y * SCREEN_WIDTH + x] = color;
    }
}

extern "C" void kernel_main(struct multiboot_info* mbi) {
    // Dynamically retrieve the real video memory channel map assigned by UTM virtual hardware
    if ((mbi->flags & (1 << 12)) && mbi->framebuffer_addr_low != 0) {
        target_video_framebuffer = (unsigned int*)(unsigned long)mbi->framebuffer_addr_low;
    } else {
        target_video_framebuffer = (unsigned int*)0xFD000000; // Safe default backup register path
    }

    // Paint background to verify graphic execution channel is active
    for (int i = 0; i < (SCREEN_WIDTH * SCREEN_HEIGHT); i++) {
        target_video_framebuffer[i] = 0xA3E899; // Fills screen with custom Lime OS brand theme color instantly
    }

    // Read and parse image graphic from storage address layout
    unsigned char* logo_asset_address = (unsigned char*)0x01000000; 
    BMPHeader* header = (BMPHeader*)logo_asset_address;

    if (header->signature == 0x4D42) {
        unsigned char* pixels = logo_asset_address + header->data_offset;
        for (int y = SCREEN_HEIGHT - 1; y >= 0; y--) {
            for (int x = 0; x < SCREEN_WIDTH; x++) {
                unsigned char b = *pixels++;
                unsigned char g = *pixels++;
                unsigned char r = *pixels++;
                draw_pixel(x, y, (r << 16) | (g << 8) | b);
            }
        }
    }
}
