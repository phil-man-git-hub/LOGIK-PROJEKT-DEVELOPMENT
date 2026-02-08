# Issue-Driven Development (IDD) Documentation Hub

> **Your comprehensive guide to the IDD system for MAN-IAC**

This documentation hub provides a detailed overview, setup instructions, usage guides, and architectural insights into the Issue-Driven Development (IDD) system. IDD aims to transform your repository into a fully integrated, AI-assisted development workflow.

---

## 🚀 Getting Started & Quick Overview

If you're new to IDD or need a quick refresher, start here:

*   **[quick_start.md](quick_start.md)**: Get IDD up and running in your repository in just 5 minutes.
*   **[idd-workflow-roadmap_issue_driven_development.md](idd-workflow-roadmap_issue_driven_development.md)**: Understand the overall implementation plan, phases, and current status of IDD in MAN-IAC.
*   **[idd-workflow-architecture.md](idd-workflow-architecture.md)**: A high-level overview of the IDD system's components, design principles, and overall structure.

---

## 📖 Core Documentation & Deep Dives

For a deeper understanding of each major component of the IDD system, explore these guides:

### 🏗️ System Architecture & Design
*   **[architecture/system-design.md](architecture/system-design.md)**: Detailed technical documentation covering the system architecture, core components, data flows, and design decisions.
*   **[guides/guide-best-practices.md](guides/guide-best-practices.md)**: Guidelines and recommendations for effective issue management, commit practices, PR workflows, and label strategies within IDD.

### ⚙️ Automation Workflows (GitHub Actions)
*   **[guides/guide-workflows.md](guides/guide-workflows.md)**: An overview of all active GitHub Actions workflows, their triggers, and what they automate.
*   **[guides/guide-sync.md](guides/guide-sync.md)**: Dedicated guide for the Issue ↔ TO-DO.md synchronization system, explaining its architecture, usage, and configuration.
*   **[templates/pr-template-guide.md](templates/pr-template-guide.md)**: Comprehensive guide to the Pull Request template, its purpose, structure, and best practices for authors and reviewers.
*   **[templates/issue-templates-guide.md](templates/issue-templates-guide.md)**: Guide to the standardized GitHub Issue Templates, explaining when to use each, their key sections, and best practices for writing good issues.
*   **[idd-workflow-example_workflows.md](idd-workflow-example_workflows.md)**: Real-world usage patterns and advanced workflows for leveraging the AI Context System.

### 🧠 AI Memory & Context System
*   **[idd-workflow-quick_start_ai_context.md](idd-workflow-quick_start_ai_context.md)**: A 5-minute guide to getting started with the AI Memory & Context system.
*   **[guides/guide-session-capture.md](guides/guide-session-capture.md)**: Detailed guide on how the system automatically captures development session activity and generates AI context files.
*   **[guides/guide-memory-search.md](guides/guide-memory-search.md)**: Guide to searching and querying captured development sessions and AI context memory.
*   **[guides/guide-context-retrieval.md](guides/guide-context-retrieval.md)**: Explains how the system intelligently assembles relevant context from multiple sources for AI assistants.
*   **[guides/guide-ai-diagnostics.md](guides/guide-ai-diagnostics.md)**: Leveraging RAG, MCP, and Live Diagnostics for AI-assisted development and debugging.
*   **[week_2_completion_summary.md](status-updates/week_2_completion_summary.md)**: A summary of the deliverables and achievements from Phase 2 (AI Memory & Context).

---

## 🛠️ Setup, Customization & Maintenance

These documents provide practical guidance for setting up, tailoring, and maintaining your IDD system:

*   **[guides/guide-setup.md](guides/guide-setup.md)**: Complete installation and configuration guide for Issue-Driven Development.
*   **[guides/guide-customization.md](guides/guide-customization.md)**: A comprehensive guide to customizing IDD for your team's specific needs via `idd-config.yml`.
*   **[guides/guide-platform-notes.md](guides/guide-platform-notes.md)**: Platform-specific instructions and considerations for macOS, Linux, and Windows/WSL.
*   **[guides/guide-troubleshooting.md](guides/guide-troubleshooting.md)**: Solutions to common issues encountered when setting up and using IDD.
*   **[guides/guide-metrics-tracking.md](guides/guide-metrics-tracking.md)**: Framework for measuring and tracking IDD success, including KPIs and ROI calculation.
*   **[guides/guide-migration.md](guides/guide-migration.md)**: Guide for migrating to IDD from other issue tracking systems or workflows.

---

## 📦 Template & Publication

Documents related to the reusability and sharing of the IDD system:

*   **[guides/guide-template-extraction.md](guides/guide-template-extraction.md)**: Documents how to extract the IDD system into a reusable template.
*   **[guides/guide-template-file-inventory.md](guides/guide-template-file-inventory.md)**: A complete inventory of all files that should be extracted for the reusable IDD template.
*   **[idd-workflow-template_readme.md](idd-workflow-template_readme.md)**: The README for the extracted IDD template repository.
*   **[guides/guide-publication.md](guides/guide-publication.md)**: Guide for publishing and releasing your Issue-Driven Development system.
*   **[guides/guide-sharing.md](guides/guide-sharing.md)**: Strategies and templates for sharing your IDD system with the community.
*   **[week_4_completion_summary.md](status-updates/week_4_completion_summary.md)**: A summary of the deliverables and achievements from Phase 4 (Reusable Template).

---

## 💡 Key Principles

*   **Issues First** - All work starts with an issue
*   **Automate Everything** - Reduce manual overhead
*   **Preserve Context** - Never lose important decisions
*   **Stay Lean** - Avoid bloat and complexity
*   **Document As You Go** - Capture insights immediately
*   **Make It Reusable** - Think template-first

---

## 🤝 Contributing

This is an evolving system. As we implement:
- Document what works (insights/)
- Record decisions (architecture/decision-records/)
- Share patterns (templates/)
- Improve continuously

---

*Last Updated: November 10, 2025*