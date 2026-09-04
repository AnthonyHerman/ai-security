---
tags: [defense, secrets-management]
group: Defense
---

# Secrets Management

*Tools and techniques for protecting secrets from AI coding agents and LLM context exposure.*

**Related:** [[Agent Identity]] | [[Secure Coding]]

## Tools

- [enject - Hide .env secrets from AI coding tools](https://github.com/GreatScott/enject) -- encrypted local store with symbolic references; plaintext secrets never exist on disk
- [Agent Vault - Keep secrets hidden from AI agents](https://github.com/botiverse/agent-vault)
- [aivault - Stop leaking API keys to AI agents](https://aivault.moldable.sh/)
- [WardGate - Give AI agents API access without giving them secrets](https://github.com/wardgate/wardgate)
- [GAP - Give AI agents secure access to your APIs](https://github.com/mikekelly/gap)
- [DepthFirst - Secrets Shouldn't Be Guesswork](https://depthfirst.com/post/depthfirst-com-post-product-release-secrets-shouldnt-be-guesswork)
- [agent-sweep - find and redact secrets in AI coding agent histories](https://github.com/Ishannaik/agent-sweep)
- [API Radar - live feed of leaked LLM API keys found on GitHub](https://apiradar.live/explore)
- [Automic Vault - secrets manager that authorizes exact operations for AI agents](https://automicvault.com)
- [Betterleaks: The Gitleaks Successor Built for Faster Secrets Scanning](https://aikido.dev/blog/betterleaks-gitleaks-successor)
- [Dave Blumenfeld introduces keypo vault - Mac Secure Enclave secrets manager for agents](https://x.com/dblumenfeld/status/2031757313481335103)
- [dumpscan - extract secrets from kernel and Windows minidump memory](https://github.com/daddycocoaman/dumpscan)
- [ghtkn - CLI for short-lived GitHub App user access tokens](https://github.com/suzuki-shunsuke/ghtkn)
- [git-alerts - monitor GitHub org users' public repos for secrets and sensitive files](https://github.com/boringtools/git-alerts)
- [git-hound - Scans GitHub for leaked secrets using GitHub dorks](https://github.com/tillson/git-hound)
- [github-actions-log-checker - scan GitHub Actions logs for exposed secrets](https://github.com/latiotech/github-actions-log-checker)
- [github-secrets - find secrets in dangling and force-pushed GitHub commits](https://github.com/neodyme-labs/github-secrets)
- [GitleaksVerifier - CLI tool to verify secrets flagged by Gitleaks](https://github.com/aydinnyunus/GitleaksVerifier)
- [HasMySecretLeaked - GitGuardian search across exposed secrets on public GitHub](https://gitguardian.com/hasmysecretleaked)
- [Infisical - secrets, certificates and identity platform for developers and agents](https://infisical.com)
- [Introducing HAR Sanitizer: secure HAR sharing](https://blog.cloudflare.com/introducing-har-sanitizer-secure-har-sharing)
- [Introducing Kingfisher: Real-Time Secret Detection And Validation](https://mongodb.com/company/blog/product-release-announcements/introducing-kingfisher-real-time-secret-detection-validation)
- [jit - just-in-time secrets behind Touch ID for your dev machine](https://github.com/jitpass/jit?=x)
- [KeyDrop - reducing API key abuse](https://keydrop.io)
- [Kingfisher - secret scanner with live validation and blast-radius mapping](https://github.com/mongodb/kingfisher)
- [kubernetes-reflector - replicate secrets, configmaps and certificates across namespaces](https://github.com/emberstack/kubernetes-reflector)
- [LeakLens - web-aware secrets scanner for JS apps, source maps and Git history](https://github.com/dinosn/leaklens)
- [LogShield - CLI that redacts secrets from logs before sharing](https://github.com/afria85/LogShield)
- [LUKSbox - encrypted container vaults with FIDO2, TPM 2.0 and post-quantum keyslots](https://github.com/PentHertz/LUKSbox)
- [Madeline Lawrence on Betterleaks - new open source secrets scanner from the Gitleaks author](https://x.com/madelinelawren/status/2032182422469779710)
- [mantra - hunt down API key leaks in JS files and pages](https://github.com/MrEmpy/mantra)
- [Nosey Parker - finds secrets and sensitive information in text and Git history](https://github.com/praetorian-inc/noseyparker)
- [OpenBao - open-source secrets, certificates and key management](https://github.com/openbao/openbao/tree/development)
- [pivit - manage x509 certificates on PIV smart cards for git signing](https://github.com/cashapp/pivit)
- [postleaks - search for sensitive data in Postman public library](https://github.com/cosad3s/postleaks)
- [retriever - secure client-side secret sharing in the browser using web crypto](https://github.com/Corgea/retriever)
- [Retriever - serverless secret sharing in the browser with Web Crypto, by Corgea](https://retriever.corgea.io)
- [secret-bridge - Monitors GitHub for leaked secrets](https://github.com/duo-labs/secret-bridge)
- [secrets-patterns-db - open-source regex database for detecting secrets and API keys](https://github.com/mazen160/secrets-patterns-db)
- [sift - credential and sensitive-data exposure triage for file shares](https://github.com/HotStartLabs/sift)
- [Straylight-AI - AI agent credential proxy for zero-knowledge secret management](https://aj-geddes.github.io/straylight-ai)
- [Sulla - scan SMB shares for secrets with NoseyParker](https://github.com/praetorian-inc/Sulla)
- [truffleshow - client-side web viewer for TruffleHog JSON output](https://github.com/alioguzhan/truffleshow)
- [webtrufflehog - browser extension scanning web traffic for exposed secrets](https://github.com/c3l3si4n/webtrufflehog)

## Platform Features

- [Amp Code - Secret Redaction](https://ampcode.com/news/secret-redaction)
- [Amp Security Reference - Secret Redaction](https://ampcode.com/security#secret-redaction)
- [Secret Redaction in GitHub Copilot (Issue #11517)](https://github.com/microsoft/vscode-copilot-release/issues/11517)
- [Advanced Data Protection now available in HCP Vault](https://hashicorp.com/blog/advanced-data-protection-adp-now-available-in-hcp-vault)
- [Doppler Bug Bounty Program on HackerOne](https://hackerone.com/doppler?type=team)
- [GitGuardian - Monitor Public GitHub for leaked secrets](https://gitguardian.com/monitor-public-github-for-secrets)
- [GitHub secret scanning AI-generated custom patterns](https://github.blog/changelog/2024-07-16-secret-scanning-ai-generated-custom-patterns-general-availability)
- [GitHub Secret Scanning Partner Program](https://docs.github.com/en/code-security/secret-scanning/secret-scanning-partner-program)
- [GitHub secret scanning shows metrics for push protection at the organization level](https://github.blog/changelog/2023-07-31-secret-scanning-shows-metrics-for-push-protection-at-the-organization-level)
- [HashiCorp acquires BluBracket to add secrets scanning](https://hashicorp.com/blog/announcing-acquisition-of-blubracket)
- [Introducing Cloudflare Secrets Store Beta](https://blog.cloudflare.com/secrets-store-beta)
- [Introducing fine-grained personal access tokens](https://github.blog/changelog/2022-10-18-introducing-fine-grained-personal-access-tokens)
- [Introducing GitHub Secret Protection and GitHub Code Security](https://github.blog/changelog/2025-03-04-introducing-github-secret-protection-and-github-code-security)
- [Multi-secondary performance replication is now available on HCP Vault](https://hashicorp.com/blog/multi-secondary-performance-replication-is-now-available-on-hcp-vault)
- [OpenTofu 1.7.0 with State Encryption and Provider-Defined Functions](https://opentofu.org/blog/opentofu-1-7-0)
- [Pasha Sviderski on Docker's native Secrets Engine - secret references injected at runtime](https://x.com/psviderski/status/2064675044681503086)
- [Secret scanning detects generic passwords with AI, public beta - GitHub Changelog](https://github.blog/changelog/2024-07-16-secret-scanning-detects-generic-passwords-with-ai-public-beta)
- [Semantic Analysis for Secrets Detection - Semgrep Secrets](https://semgrep.dev/blog/2023/introducing-semgrep-secrets)
- [Vault PR 22484 - advanced TTL management for database static roles](https://github.com/hashicorp/vault/pull/22484)

## Guides

- [A better way to limit Claude Code access to secrets](https://patrickmccanna.net/a-better-way-to-limit-claude-code-and-other-coding-agents-access-to-secrets/)
- [Don't let AI read your .env files (Filip Hric / 1Password approach)](https://filiphric.com/dont-let-ai-read-your-env-files)
- [Access Azure Key Vault from a Local Kubernetes Cluster with Azure Arc Workload Identity](https://powers-hell.com/2026/08/26/access-azure-key-vault-from-a-local-kubernetes-cluster-with-azure-arc-workload-identity)
- [Anyone can Access Deleted and Private Repository Data on GitHub - Truffle Security](https://trufflesecurity.com/blog/anyone-can-access-deleted-and-private-repo-data-github)
- [API Security Best Practices - Leak Mitigation Checklist](https://github.com/GitGuardian/APISecurityBestPractices/blob/master/Leak%20Mitigation%20Checklist.md)
- [Automate Postman Secret Scanning with TruffleHog](https://andrelia.net/posts/automate-postman-secret-scanning-with-trufflehog)
- [Azure AD Client Secret Leak: The Keys to Cloud](https://resecurity.com/blog/article/azure-ad-client-secret-leak-the-keys-to-cloud)
- [Behind GitHub's new authentication token formats](https://github.blog/2021-04-05-behind-githubs-new-authentication-token-formats)
- [Charlie Marsh on uv pipeline breaking over Bearer Token redaction in GitHub Actions](https://x.com/charliermarsh/status/1978512448366706893)
- [Cracking the Vault: Zero-Day Flaws in Authentication, Identity, and Authorization in HashiCorp Vault](https://cyata.ai/blog/cracking-the-vault-how-we-found-zero-day-flaws-in-authentication-identity-and-authorization-in-hashicorp-vault)
- [Detecting and removing dangerous secrets on dev workstations before Shai-Hulud does](https://recyclebin.zip/posts/2026-05-25-secret-scanning-fleet-bagel)
- [Google API keys keep working after you delete them long enough to be exploited](https://aikido.dev/blog/google-api-keys-deletion)
- [Google API Keys Weren't Secrets, But Then Gemini Changed the Rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- [Hidden GitHub Commits and How to Reveal Them](https://neodyme.io/en/blog/github_secrets)
- [How I Found 3,800+ Leaked Secrets on GitHub Archive Using AI](https://aydinnyunus.github.io/2026/06/30/hunting-leaked-secrets-on-github-archive)
- [How I Scanned all of GitHub's Oops Commits for Leaked Secrets - Truffle Security](https://trufflesecurity.com/blog/guest-post-how-i-scanned-all-of-github-s-oops-commits-for-leaked-secrets)
- [How to Monitor GitHub for Secrets - Duo Labs](https://duo.com/labs/research/how-to-monitor-github-for-secrets)
- [jtgi on wallet drained after leaked private key in old public GitHub commit](https://x.com/jtgi/status/1864936442499399974)
- [Keeping Secrets Out of Logs](https://allan.reyes.sh/posts/keeping-secrets-out-of-logs)
- [Leaked-Credentials - finding leaked credentials with DevTools regex](https://github.com/h4x0r-dz/Leaked-Credentials)
- [Making TruffleHog Faster with Aho-Corasick](https://trufflesecurity.com/blog/making-trufflehog-faster-with-aho-corasick)
- [Martez Reed on authenticating to HashiCorp Vault from Proxmox with JWT auth](https://x.com/greenreedtech/status/1833231068641824883)
- [Native Secure Enclave backed SSH keys on macOS](https://gist.github.com/arianvp/5f59f1783e3eaf1a2d4cd8e952bb4acf)
- [Regex is almost all you need - how Gitleaks combines regex, entropy and allowlists to find secrets](https://lookingatcomputer.substack.com/p/regex-is-almost-all-you-need)
- [The Day We Unveiled the Secret Rotation Illusion](https://clutch.security/blog/the-day-we-unveiled-the-secret-rotation-illusion)
- [The end of GitHub PATs: You can't leak what you don't have](https://chainguard.dev/unchained/the-end-of-github-pats-you-cant-leak-what-you-dont-have)
- [The Postman Carries Lots of Secrets - leaked credentials in public Postman workspaces](https://trufflesecurity.com/blog/postman-carries-lots-of-secrets)
- [The State of Secrets Sprawl Report 2025](https://gitguardian.com/files/the-state-of-secrets-sprawl-report-2025)
- [The Trivy Attack Revealed a Blind Spot in Every Secrets Manager](https://vaultproof.dev/blog/trivy-supply-chain-attack)
- [Thousands of Exposed Secrets Found on Docker Hub](https://flare.io/learn/resources/docker-hub-secrets-exposed)
- [Top HashiCorp Vault Alternatives](https://infisical.com/blog/hashicorp-vault-alternatives)
- [Unauthorized access to any organization's Codespace secrets via a GitHub Security Advisory flaw](https://ophionsecurity.com/blog/access-organization-secrets-in-github)

---
*95 resources*
