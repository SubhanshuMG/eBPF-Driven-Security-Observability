eBPF-LSM sample: demonstrates attaching to LSM hooks for file open or socket create.

Requirements:
- Kernel with CONFIG_LSM and CONFIG_EBPF_LSM enabled
- libbpf (for loading BPF object)
- Good understanding of kernel programming & safety

Do NOT run on production without testing.
