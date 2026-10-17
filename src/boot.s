.set ALIGN,    1<<0             
.set MEMINFO,  1<<1             
.set GRAPHICS, 1<<2             # Flag 2: Request an explicit graphics frame buffer layout
.set FLAGS,    ALIGN | MEMINFO | GRAPHICS  
.set MAGIC,    0x1BADB002       
.set CHECKSUM, -(MAGIC + FLAGS) 

.section .multiboot
.align 4
.long MAGIC
.long FLAGS
.long CHECKSUM
# Multiboot graphics field specifications layout requirements:
.long 0          # Mode type configuration (0 = linear graphics mode)
.long 1024       # Targeted Screen Width Sizing
.long 768        # Targeted Screen Height Sizing
.long 32         # Color depth per pixel element channel

.section .bss
.align 16
stack_bottom:
.skip 16384 
stack_top:

.section .text
.global _start
.type _start, @function
_start:
	mov $stack_top, %esp
	push %ebx         # Multiboot info structure pointer address is stored inside EBX register
	call kernel_main
	cli
1:	hlt
	jmp 1b
