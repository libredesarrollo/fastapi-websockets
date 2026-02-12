# FastAPI Clean Architecture Refactoring - Walkthrough

## Overview

Successfully refactored the FastAPI application following Clean Architecture principles with clear separation of concerns across four distinct layers.

## New Architecture Structure

```
src/
├── entities/                    # Layer 1: Enterprise Business Rules
├── use_cases/                   # Layer 2: Application Business Rules
├── interface_adapters/          # Layer 3: Interface Adapters
└── frameworks_drivers/          # Layer 4: Frameworks & Drivers
```

---

## Layer 1: Entities (Domain Models)

Pure Python dataclasses with **zero framework dependencies**.

### Created Files

- [user.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/entities/user.py) - User entity
- [alert.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/entities/alert.py) - Alert entity
- [room.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/entities/room.py) - Room entity
- [token.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/entities/token.py) - Token entity

**Key Benefit**: Domain models are completely independent and can be used in any context.

---

## Layer 2: Use Cases (Business Logic)

Application-specific business rules that orchestrate the flow of data to and from entities.

### Created Files

**Authentication**
- [login.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/use_cases/auth/login.py) - `LoginUseCase`
- [register.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/use_cases/auth/register.py) - `RegisterUseCase`
- [logout.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/use_cases/auth/logout.py) - `LogoutUseCase`

**Data Retrieval**
- [get_alerts.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/use_cases/alerts/get_alerts.py) - `GetAlertsUseCase`
- [get_rooms.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/use_cases/rooms/get_rooms.py) - `GetRoomsUseCase`

**Key Benefit**: Business logic is isolated from HTTP layer and database implementation. Use cases accept repository interfaces via dependency injection.

---

## Layer 3: Interface Adapters

Converts data between the format most convenient for use cases/entities and the format most convenient for external agencies.

### Repository Interfaces

- [repository_interfaces.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/repositories/repository_interfaces.py) - Abstract base classes defining contracts

### Repository Implementations

- [user_repository.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/repositories/user_repository.py) - `SQLUserRepository`
- [alert_repository.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/repositories/alert_repository.py) - `SQLAlertRepository`
- [room_repository.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/repositories/room_repository.py) - `SQLRoomRepository`
- [token_repository.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/repositories/token_repository.py) - `SQLTokenRepository`

### Controllers (HTTP Endpoints)

- [auth_controller.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/controllers/auth_controller.py) - `/api/login`, `/api/register`, `/api/logout`
- [alerts_controller.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/controllers/alerts_controller.py) - `/api/alerts`
- [rooms_controller.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/controllers/rooms_controller.py) - `/api/rooms`

### Presenters

- [schemas.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/interface_adapters/presenters/schemas.py) - Pydantic models for request/response

**Key Benefit**: Repository pattern allows easy swapping of data sources. Controllers are thin and delegate to use cases.

---

## Layer 4: Frameworks & Drivers

External frameworks and tools like database drivers and web frameworks.

### Database Configuration

- [connection.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/frameworks_drivers/db/connection.py) - SQLAlchemy engine and session setup
- [orm_models.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/frameworks_drivers/db/orm_models.py) - SQLAlchemy ORM models

### HTTP Framework

- [app.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/frameworks_drivers/http/app.py) - FastAPI application with router registration and WebSocket endpoint
- [dependencies.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/src/frameworks_drivers/http/dependencies.py) - Dependency injection (repositories, authentication)

---

## Entry Point

- [main.py](file:///Users/andrescruz/Desktop/proyects/fastapi/websockets/main.py) - Application entry point

Run with:
```bash
uvicorn main:app --reload
```

---

## Dependency Direction (Clean Architecture Rule)

```
┌────────────────────────────────┐
│  Frameworks & Drivers          │ ──┐
│  (FastAPI, SQLAlchemy)         │   │
└────────────────────────────────┘   │
                                     ▼
┌────────────────────────────────┐
│  Interface Adapters            │ ──┐
│  (Controllers, Repositories)   │   │
└────────────────────────────────┘   │
                                     ▼
┌────────────────────────────────┐
│  Use Cases                     │ ──┐
│  (Business Logic)              │   │
└────────────────────────────────┘   │
                                     ▼
┌────────────────────────────────┐
│  Entities                      │
│  (Domain Models)               │
└────────────────────────────────┘
```

**All dependencies point INWARD** - outer layers depend on inner layers, never the reverse.

---

## API Endpoints

All endpoints are accessible under the `/api` prefix:

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/login` | Authenticate user and get token | No |
| POST | `/api/register` | Create new user account | No |
| POST | `/api/logout` | Invalidate user token | No |
| GET | `/api/alerts` | Get alerts (optionally filter by room) | Yes |
| GET | `/api/rooms` | Get all available rooms | No |

### WebSocket

- `WS /ws` - Real-time chat communication

---

## Verification Results

✅ **Server Started Successfully**

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### What Was Tested

1. **Application startup** - No import errors, all modules load correctly
2. **Database initialization** - Tables created successfully
3. **Dependency injection** - All repositories and services wired correctly
4. **Router registration** - All endpoints registered under `/api` prefix

---

## Migration from Old Structure

### Files Refactored

| Old File | New Location | Notes |
|----------|--------------|-------|
| `models.py` | `src/entities/` + `src/frameworks_drivers/db/orm_models.py` | Split into domain entities and ORM models |
| `schemas.py` | `src/interface_adapters/presenters/schemas.py` | Moved to presenters layer |
| `database.py` | `src/frameworks_drivers/db/connection.py` | Moved to frameworks layer |
| `rest_api.py` | `src/use_cases/` + `src/interface_adapters/controllers/` | Split into use cases and controllers |
| `api.py` | `src/frameworks_drivers/http/app.py` + `main.py` | Split into app initialization and entry point |

### Files to Keep (Optional)

The old files can remain for reference or be deleted:
- `api.py`
- `rest_api.py`
- `models.py`
- `database.py`
- `schemas.py`

The new architecture is completely self-contained in the `src/` directory and `main.py`.

---

## Benefits Achieved

### ✅ Separation of Concerns
- Each layer has a single, well-defined responsibility
- Business logic is isolated from infrastructure

### ✅ Testability
- Use cases can be tested without HTTP layer or database
- Easy to mock repository interfaces

### ✅ Maintainability
- Changes to database don't affect business logic
- Changes to HTTP framework don't affect domain models

### ✅ Flexibility
- Easy to swap SQLAlchemy for another ORM
- Easy to swap FastAPI for another web framework
- Easy to add new use cases without modifying existing code

### ✅ Independence
- Entities have zero external dependencies
- Use cases only depend on repository interfaces
- Framework-specific code is isolated to outer layers
