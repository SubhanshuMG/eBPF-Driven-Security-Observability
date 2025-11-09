// lsm_sample.c  (conceptual)
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

SEC("lsm/socket_create")
int BPF_PROG(socket_create_lsm, int family, int type, int protocol)
{
    if (family == AF_INET) {
        return -1; // deny
    }
    return 0; // allow
}

char LICENSE[] SEC("license") = "GPL";
