from bcc import BPF
import os
import time

bpf_text = r"""
#include <net/sock.h>
#include <bcc/proto.h>

int trace_connect(struct pt_regs *ctx, struct sock *sk) {
    u16 dport = sk->__sk_common.skc_dport;
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    if (dport == bpf_htons(4444)) {
        bpf_trace_printk("ALERT: PID %d attempted connect to port 4444\n", pid);
    }
    return 0;
}
"""

b = BPF(text=bpf_text)
b.attach_kprobe(event="tcp_connect", fn_name="trace_connect")

print("BCC Agent: monitoring tcp_connect...")

while True:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        try:
            pid_val = int(msg.split()[2])
            cgroup_path = f"/proc/{pid_val}/cgroup"
            pod_info = "unknown"
            if os.path.exists(cgroup_path):
                with open(cgroup_path, 'r') as f:
                    cg = f.read()
                    pod_info = cg.splitlines()[-1].strip()
            print(time.strftime("%Y-%m-%d %H:%M:%S"), msg.strip(), "| cgroup:", pod_info)
        except Exception:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), msg.strip())
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print("Error reading trace:", e)
        time.sleep(1)
