# 💸 PesaLoop (SendPesa) — Financial Services Platform

## 📖 Overview

**PesaLoop** is a multi-service fintech platform providing secure, scalable financial services including:

- **Digital wallet management**
- **Payments and transfers**
- **Credit management**
- **Forex services**
- **Biometric-secure authentication**
- **Admin and operational dashboards**
- **Infrastructure management tools**
- **Mobile applications for users**

The system is modular, built on Django REST Framework for the backend, React Native (Expo) for mobile, and modern admin interfaces.

---

## 📦 Monorepo Structure

```
.
├── business/               # Django backend (APIs, services, integrations)
├── mobile/                 # React Native Expo mobile application
├── admindashboard/         # (To be renamed `website/` or `dashboard/`) Web admin dashboard (Next.js)
├── network-dashboard/      # Network monitoring and control dashboard (Python script-based)
├── infrastructure/         # Infrastructure-as-code, deployments, CI/CD scripts
├── LICENSE.md
├── TERMS.md
└── README.md               # This file
```

---

## 📱 Applications & Services

### `business/` — Backend APIs

**Tech:** Django, Django REST Framework, Celery, Redis

- Wallet, payments, forex, credit, media, reporting services
- Secure token-based and biometric authentication
- API documentation via **Swagger** and **Redoc**
- Celery workers for background tasks

➡️ [See `business/README.md`](./business/README.md)

---

### `mobile/` — Mobile App

**Tech:** React Native (Expo SDK 53+), Expo Router, TypeScript, Tailwind CSS

- User onboarding, authentication, wallet, transfers, KYC, payments
- Secure biometric storage and token management
- React Query for API state
- Push notifications support (with development builds)

➡️ [See `mobile/README.md`](./mobile/README.md)

---

### `admindashboard/` — Web Admin Dashboard (To be renamed)

**Tech:** Next.js, React, TypeScript

- Admin interfaces for transaction management, user oversight, reports
- Replaces the legacy `website/` folder
- Will be renamed to `website/` or `dashboard/` in upcoming iterations

➡️ [See `admindashboard/README.md`](./admindashboard/README.md)

---

### `network-dashboard/`

**Tech:** Python, CLI-based

- Provides real-time network monitoring and reporting
- Primarily for internal infrastructure oversight and server health

➡️ [See `network-dashboard/README.md`](./network-dashboard/README.md)

---

### `infrastructure/`

**Tech:** Docker, Nginx, CI/CD pipelines (future), EAS for Expo

- Manages deployments, dockerization, load balancing configurations, and infrastructure scripts
- Future home for Terraform / Ansible playbooks and cloud deployment config

➡️ [See `infrastructure/README.md`](./infrastructure/README.md)

---

## 📃 Licensing

This project is licensed under the **MIT License** — see the [LICENSE.md](./LICENSE.md) file for full terms.

---

## 📄 Terms & Conditions

Use of this software and platform constitutes agreement to our [TERMS.md](./TERMS.md). Review carefully before deploying or distributing the system.

---

## 📌 Roadmap

- ✅ Finalize mobile biometric auth
- ✅ Forex service integration
- ✅ Push notification support (SDK 53+)
- ✅ Admin dashboard migration (website → dashboard)
- [ ] Infrastructure dockerization and CI/CD
- [ ] Kubernetes support for scalable deployment
- [ ] Merchant and agency portals

---

## 📖 Documentation

Each service directory contains its own `README.md` with setup and usage instructions.

For API reference:

- Swagger: `/api/docs/swagger/`
- Redoc: `/api/docs/redoc/`

---

## ✅ Contributing

Contribution guidelines coming soon.
For now, internal team contributors can open feature branches and submit pull requests targeting the `develop` branch.

---

## 💬 Support

For questions, issues, or contribution requests, please contact **Musied Group DevOps** or the lead developer.

---

## ✨ Summary

PesaLoop is a secure, modular, fintech platform designed for modern financial services at scale — serving users, agents, and administrators through mobile, web, and API interfaces.

---
