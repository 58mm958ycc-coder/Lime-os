include <stddef.h>

// Identify Executable Subsystem Types
typedef enum {
    FORMAT_UNKNOWN,
    FORMAT_EXE_PE,
    FORMAT_APK_ELF,
    FORMAT_IPA_MACHO
} binary_type_t;

// Scans binary headers (Magic Numbers)
binary_type_t detect_binary_format(const unsigned char* buffer, size_t size) {
    if (size < 4) return FORMAT_UNKNOWN;

    // Windows Executable Magic Header: 'MZ'
    if (buffer[0] == 'M' && buffer[1] == 'Z') {
        return FORMAT_EXE_PE;
    }
    
    // Android ZIP framework (APK starts as standard ZIP 'PK')
    if (buffer[0] == 'P' && buffer[1] == 'K' && buffer[2] == 0x03 && buffer[3] == 0x04) {
        return FORMAT_APK_ELF;
    }

    // Apple Mach-O Binary (IPA container contains Mach-O executable)
    // Magic: 0xFEEDFACE (32-bit) or 0xFEEDFACF (64-bit)
    if ((buffer[0] == 0xFE && buffer[1] == 0xED && buffer[2] == 0xFA && buffer[3] == 0xCE) ||
        (buffer[0] == 0xFE && buffer[1] == 0xED && buffer[2] == 0xFA && buffer[3] == 0xCF)) {
        return FORMAT_IPA_MACHO;
    }

    return FORMAT_UNKNOWN;
}
