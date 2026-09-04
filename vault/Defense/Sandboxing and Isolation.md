---
tags: [defense, sandboxing-and-isolation]
group: Defense
---

# Sandboxing and Isolation

*Runtime containment, sandboxing, and isolation for AI agents and code execution.*

**Related:** [[Coding Tools]]

## Sandbox Tools

- [Secure, kernel-enforced sandbox CLI a](https://github.com/always-further/nono)
- [OpenSandbox is a general-purpose sand](https://github.com/alibaba/OpenSandbox)
- [Python read-only sandbox for LLM agents an](https://github.com/corv89/shannot)
- [A minimal, secure Python interpreter writt](https://github.com/pydantic/monty)
- [Postgres Sandbox](https://postgres.new/)
- [Claude "File creation" is actually a sandboxed code execution environment and has](https://x.com/tjade273/status/1965525541739704574)
- [acl-proxy - Rust ACL-aware HTTP/HTTPS proxy with URL policy engine](https://github.com/kcosr/acl-proxy)
- [Agent Safehouse - macOS kernel-level sandboxing for LLM coding agents](https://agent-safehouse.dev)
- [Box by ASCII - cheap persistent Linux VM sandboxes for AI agents](https://box.ascii.dev)
- [Bromure - disposable Linux VM sandboxes on macOS for AI coding agents and browsing](https://github.com/rderaison/bromure)
- [clawker - self-hosted AI coding agent sandbox in Docker with egress firewall](https://github.com/schmitthub/clawker)
- [cloudflare/computer - virtual filesystem and sandboxed execution environment for agents](https://github.com/cloudflare/computer)
- [Coder - self-hosted, governed environments for running AI coding agents at scale](https://coder.com)
- [Cordium - open-source identity-based sandbox platform for developers and AI agents](https://github.com/octelium/cordium)
- [CubeSandbox - secure lightweight sandbox for AI agents](https://github.com/TencentCloud/CubeSandbox)
- [Dan Guido on running Claude Code in YOLO mode safely with the Trail of Bits devcontainer](https://x.com/dguido/status/2017302474952945922)
- [Daytona - Secure Infrastructure for Running AI-Generated Code](https://daytona.io)
- [Docker Sandboxes - Run Claude Code and Coding Agents Unsupervised but Safely](https://docker.com/blog/docker-sandboxes-run-claude-code-and-other-coding-agents-unsupervised-but-safely)
- [dyana - sandbox for loading, running and profiling ML models, pickles and other files](https://github.com/dreadnode/dyana)
- [exe.dev - disposable sandbox VMs for AI agents](https://exe.dev)
- [fend - sandboxed micro-VM runtime for npm install and dev scripts](https://github.com/Lisovate/fend)
- [hazmat - OS-level containment for AI coding agents](https://github.com/dredozubov/hazmat)
- [httpjail - HTTP and HTTPS request filter and network isolation for processes](https://github.com/coder/httpjail)
- [iron-proxy v0.23.0 - egress firewall for untrusted workloads](https://github.com/ironsh/iron-proxy/releases/tag/v0.23.0)
- [jailer - eBPF-based mandatory access control process jailing for Linux](https://github.com/gen0sec/jailer)
- [John McBride introduces stereOS, a hardened NixOS-based operating system for sandboxing AI agents](https://x.com/johncodes/status/2027079574513664071)
- [Landlock - unprivileged sandboxing for Linux](https://landlock.io)
- [Lume - macOS VM sandbox for AI agents](https://cua.ai/docs/lume/guide/getting-started/introduction)
- [mezz - self-contained wifi sandbox for inspecting IoT devices](https://github.com/ABGEO/mezz)
- [MXC - Microsoft eXecution Container for sandboxing untrusted model output and tools](https://github.com/microsoft/mxc)
- [netfence - eBPF network egress allowlisting daemon for VMs and containers](https://github.com/danthegoodman1/netfence)
- [sandbox-probe - agentic sandbox enumeration and escape testing for AI coding agents](https://github.com/controlplaneio/sandbox-probe)
- [sandcat - Docker dev container sandbox for AI agents with mitmproxy network rules and secret injection](https://github.com/softwaremill/sandcat)
- [shuru - local-first microVM sandbox for AI agents](https://shuru.run)
- [SlicerVM - real Linux microVMs for AI sandboxes](https://slicervm.com)
- [traffico - eBPF traffic shaping with network intent guardrails for agent workloads](https://github.com/leodido/traffico)
- [vmux - stateful sandboxes for agents](https://vmux.sdan.io)
- [yolobox - sandboxed AI coding agents in a container](https://yolobox.dev)

## Containerization

- [Docker Desktop 4.40 Release - Docker](https://www.docker.com/blog/docker-desktop-4-40/)
- [Docker Labs: GenAI No. 19](https://www.linkedin.com/pulse/docker-labs-genai-19-docker-5v8oe)
- [Containerize your agents!](https://discord.gg/tFksvzbHde)
- [Docker Sandboxes: Run Agents in YOLO Mode, Safely](https://www.docker.com/blog/docker-sandboxes-run-agents-in-yolo-mode-safely/)
- [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/)
- [Chainguard Images - minimal hardened container images](https://images.chainguard.dev)
- [Chainguard OS Whitepaper](https://get.chainguard.dev/hubfs/Collateral/Reports_and_Whitepapers/ChainguardOSWhitepaper.pdf)
- [Containerize your agents! - Dagger](https://youtube.com/watch?v=XWO_3My2eVU)
- [Copacetic - directly patch container image vulnerabilities](https://project-copacetic.github.io/copacetic/website)
- [Copy Fail in Kubernetes: RuntimeDefault Did Not Block AF_ALG - CVE-2026-31431](https://juliet.sh/blog/we-tested-copy-fail-in-kubernetes-pss-restricted-runtime-default-af-alg)
- [Docker-OSX - run macOS in Docker for security research](https://github.com/sickcodes/Docker-OSX)
- [Greg Castle on converting GKE system containers to non-root - KubeCon EU talk summary](https://x.com/mrgcastle/status/1659650484242894849)
- [Kasm Workspaces - container streaming and remote browser isolation](https://kasmweb.com)
- [Kubernetes security: Safeguarding your container kingdom - Red Canary](https://redcanary.com/blog/kubernetes-security)
- [macOS Containers Initiative - native container support and isolation on macOS](https://macoscontainers.org)
- [Minimus - free hardened container images with near-zero CVEs](https://minimus.io)
- [oci-seccomp-bpf-hook - OCI hook to trace syscalls and generate seccomp profiles](https://github.com/containers/oci-seccomp-bpf-hook)
- [Orchard - native macOS UI for Apple Containers with sandboxed agents](https://orchard.andon.dev)
- [seccomp-profiler - eBPF tool that generates per-container seccomp profiles](https://github.com/rimvydascivilis/seccomp-profiler)
- [Securing the Container World with Policies: acjs and ctrdac](https://bughunters.google.com/blog/6669874749636608/securing-the-container-world-with-policies-acjs-and-ctrdac)
- [tank-os - Fedora bootc image for running OpenClaw as a rootless Podman workload](https://github.com/LobsterTrap/tank-os)

## Guides and Discussion

- https://www.luiscardoso.dev/blog/sandboxes-for-ai
- [YOLO in the Sandbox – Voratiq](https://voratiq.com/blog/yolo-in-the-sandbox/)
- [KiloClaw Security White Paper](https://244051090.fs1.hubspotusercontent-na2.net/hubfs/244051090/KiloClaw%20Security%20White%20Paper.pdf)
- [A field guide to sandboxes for AI](https://luiscardoso.dev/blog/sandboxes-for-ai)
- [Agent Safety is a Box - Marc Brooker](https://brooker.co.za/blog/2026/01/12/agent-box.html)
- [Daniel Von Fange on secure crypto dev needing 4 isolated computers - no npm, VS Code or agents](https://x.com/danielvf/status/2059302685539471738)
- [Escaping Google Cloud Application Integration Sandbox: Straight into Borg](https://nopnop.pro/2026/08/26/escaping-google-cloud-application-integration-sandbox)
- [In sandboxes we shouldn't trust - limits of sandboxing AI agents](https://embroidery.io/blog/in-sandboxes-we-shouldnt-trust)
- [Jennifer Marsman on sandboxing OpenClaw with Microsoft Execution Containers](https://x.com/i/status/2061867078072549795)
- [Philipp Schmid on sandbox network allowlists and egress-proxy credential injection](https://x.com/_philschmid/status/2056836579122147749)
- [Simon Willison on httpjail - HTTP sandboxing for coding agents](https://simonwillison.net/2025/Sep/19/httpjail)
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/2026/08/26/vms-wont-contain-cyber-capable-agents)
- [Your Container Is Not a Sandbox - The State of MicroVM Isolation in 2026](https://emirb.github.io/blog/microvm-2026)

---
*72 resources*
