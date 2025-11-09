FROM public.ecr.aws/amazonlinux/amazonlinux:2 as builder

RUN yum -y install python3 python3-devel gcc make bzip2 bzip2-devel libbpf-devel elfutils-libelf-devel git && yum clean all
RUN python3 -m pip install --upgrade pip

FROM amazonlinux:2
COPY --from=builder /usr /usr
RUN yum -y install python3 && yum clean all
COPY bcc_agent.py /opt/bcc_agent.py
RUN python3 -m pip install bcc
CMD ["python3", "/opt/bcc_agent.py"]
