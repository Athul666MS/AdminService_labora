<<<<<<< HEAD
# Admin Service – Freelancing Platform

## Overview

The Admin Service is a supervisory microservice in the Freelancing Platform. It allows administrators to monitor, control, and manage platform activities without owning core business data.

This service follows microservice architecture principles:

- Admin Service does not store users, jobs, reviews, or notifications
- It communicates with other services to perform admin actions
- It maintains audit logs for accountability and security

## Responsibilities

The Admin Service is responsible for:

- **User Management** – Manage Clients and Freelancers
- **User Blocking/Unblocking** – Restrict or restore user access
- **User Verification** – Approve and verify users on the platform
- **Payment Dispute Monitoring** – Track and manage payment conflicts
- **Review Moderation** – Delete or flag inappropriate reviews
- **Notification Triggering** – Send notifications to users
- **Notification Monitoring** – Track notification status and delivery
- **Audit Logging** – Maintain complete audit trail of admin actions

## Architecture

```
Admin Dashboard
      ↓
 Admin Service
      ↓
 ┌──────────────┬──────────────┬──────────────┐
 │Client Service│Freelancer Svc│Notification  │
 │              │              │Service       │
 └──────────────┴──────────────┴──────────────┘
              ↓
        Review Service
```

**Design Principle:**
- Admin Service controls and monitors
- Other services own the actual data
- Admin Service is the coordination layer

## Authentication & Authorization

- Uses JWT Authentication for all endpoints
- Only users with `role = admin` can access Admin Service APIs
- JWT token is forwarded to other services for secure service-to-service communication
- All actions are logged with admin identity for audit trail

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** JWT (Stateless)
- **Database:** MySQL / PostgreSQL
- **Service Communication:** HTTP (REST)
- **Audit Logging:** Database-backed logs

## Project Structure

```
admin/
├── models.py           # Admin-owned database tables
├── serializers.py      # Request/response validation
├── views.py            # Admin API endpoints
├── permissions.py      # Admin-only access control
├── urls.py             # API routes
├── services.py         # Service-to-service communication
└── README.md
```

## Database Models

Admin Service owns the following database models:

### 1. UserVerification

Tracks which admin verified which user and when.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary Key |
| `user_id` | Integer | User being verified |
| `user_type` | String | `client` or `freelancer` |
| `admin_id` | Integer | Admin who verified |
| `verified_at` | DateTime | Verification timestamp |
| `status` | String | `approved` or `rejected` |

### 2. PaymentDispute

Tracks payment-related disputes for admin resolution.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary Key |
| `job_id` | Integer | Related job ID |
| `payment_id` | Integer | Related payment ID |
| `client_id` | Integer | Client who raised dispute |
| `freelancer_id` | Integer | Freelancer involved |
| `dispute_reason` | Text | Reason for dispute |
| `status` | String | `open`, `resolved`, `rejected` |
| `admin_resolution` | Text | Admin's decision |
| `created_at` | DateTime | Dispute creation time |
| `resolved_at` | DateTime | Resolution timestamp |

### 3. AdminActionLog

Audit log for every admin action for accountability and traceability.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary Key |
| `admin_id` | Integer | Admin who performed action |
| `action_type` | String | Type of action (block, verify, delete, etc.) |
| `target_service` | String | Service affected (user, review, payment) |
| `target_id` | Integer | ID of affected resource |
| `details` | JSON | Additional action details |
| `status` | String | `success` or `failure` |
| `timestamp` | DateTime | Action timestamp |
| `ip_address` | String | Admin's IP address |

## API Endpoints

### User Management

#### View All Users

Fetches users from Client Service and Freelancer Service and combines them.

```http
GET /api/admin/users/
Authorization: Bearer <JWT_TOKEN>
```

**Response:**

```json
{
  "clients": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "status": "active"
    }
  ],
  "freelancers": [
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "skills": ["Django", "React"],
      "status": "active"
    }
  ]
}
```

**Query Parameters:**
- `status` – Filter by user status (active, blocked, pending)
- `role` – Filter by role (client, freelancer)

#### Block / Unblock User

```http
PATCH /api/admin/users/{role}/{user_id}/block/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Path Parameters:**
- `role` – `client` or `freelancer`
- `user_id` – User ID to block/unblock

**Request Body:**

```json
{
  "action": "block",
  "reason": "Violation of platform guidelines"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "User blocked successfully",
  "user_id": 5,
  "blocked_at": "2026-01-19T10:30:00Z"
}
```

#### Verify User

```http
POST /api/admin/users/verify/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**

```json
{
  "user_id": 3,
  "user_type": "freelancer",
  "status": "approved",
  "notes": "Documents verified successfully"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "User verified",
  "verified_at": "2026-01-19T10:30:00Z"
}
```

### Payment Dispute Management

#### View All Payment Disputes

```http
GET /api/admin/payments/disputes/
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters:**
- `status` – Filter by status (open, resolved, rejected)
- `job_id` – Filter by job ID

**Response:**

```json
{
  "disputes": [
    {
      "id": 1,
      "job_id": 5,
      "payment_id": 10,
      "client_id": 2,
      "freelancer_id": 3,
      "dispute_reason": "Work not completed",
      "status": "open",
      "created_at": "2026-01-19T10:00:00Z"
    }
  ]
}
```

#### Create/Resolve Dispute

```http
POST /api/admin/payments/disputes/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body (Create):**

```json
{
  "job_id": 5,
  "payment_id": 10,
  "client_id": 2,
  "freelancer_id": 3,
  "dispute_reason": "Payment discrepancy"
}
```

**Request Body (Resolve):**

```json
{
  "dispute_id": 1,
  "status": "resolved",
  "admin_resolution": "Refund 50% to client",
  "action": "refund"
}
```

### Review Moderation

#### Delete Review

```http
DELETE /api/admin/reviews/{review_id}/delete/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**

```json
{
  "reason": "Inappropriate content"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Review deleted successfully",
  "review_id": 15,
  "deleted_at": "2026-01-19T10:30:00Z"
}
```

### Notification Management

#### Send Notification

```http
POST /api/admin/notifications/send/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**

```json
{
  "notification_type": "user",
  "user_id": 5,
  "title": "Account Verification",
  "message": "Your account has been verified successfully",
  "priority": "high"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Notification sent",
  "notification_id": 25
}
```

#### View All Notifications

```http
GET /api/admin/notifications/
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters:**
- `status` – Filter by status (sent, pending, failed)
- `user_id` – Filter by recipient user ID

**Response:**

```json
{
  "notifications": [
    {
      "id": 25,
      "user_id": 5,
      "title": "Account Verification",
      "message": "Your account has been verified",
      "status": "sent",
      "sent_at": "2026-01-19T10:30:00Z"
    }
  ]
}
```

### Audit Logging

#### View Admin Action Logs

```http
GET /api/admin/logs/
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters:**
- `admin_id` – Filter by specific admin
- `action_type` – Filter by action type (block, verify, delete, etc.)
- `date_from` – Filter from date (ISO 8601)
- `date_to` – Filter to date (ISO 8601)

**Response:**

```json
{
  "logs": [
    {
      "id": 1,
      "admin_id": 1,
      "action_type": "user_block",
      "target_service": "user",
      "target_id": 5,
      "details": {
        "reason": "Violation of platform guidelines"
      },
      "status": "success",
      "timestamp": "2026-01-19T10:30:00Z",
      "ip_address": "192.168.1.1"
    }
  ]
}
```

## Service-to-Service Communication

Admin Service communicates with other microservices using HTTP requests with JWT token forwarding.

### Example Communication Pattern

```python
import requests

def call_user_service(endpoint, method="GET", data=None, admin_token=None):
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    url = f"http://user-service:8001{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data, timeout=5)
        
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Service timeout"}
    except requests.exceptions.ConnectionError:
        return {"error": "Service unavailable"}
```

**Key Features:**
- JWT token forwarded via `Authorization` header
- Timeout handling (5 seconds)
- Error handling for service failures
- Secure service-to-service communication

## Error Handling

Admin Service gracefully handles various error scenarios:

| Status Code | Error | Cause | Solution |
|-------------|-------|-------|----------|
| 401 | Unauthorized | Invalid or missing JWT token | Provide valid JWT token |
| 403 | Forbidden | User is not admin | Only admins can access |
| 404 | Not Found | Resource doesn't exist | Check resource ID |
| 502 | Bad Gateway | Called service is down | Service unavailable, retry later |
| 503 | Service Unavailable | Admin Service is down | Service temporarily unavailable |
| 504 | Gateway Timeout | Service call took too long | Timeout exceeded, retry |

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/admin-service.git
cd admin-service
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Service URLs
USER_SERVICE_URL=http://user-service:8001
REVIEW_SERVICE_URL=http://review-service:8002
NOTIFICATION_SERVICE_URL=http://notification-service:8003
PAYMENT_SERVICE_URL=http://payment-service:8004

# Database
DATABASE_URL=postgresql://user:password@db:5432/admin_db
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start Server

```bash
python manage.py runserver
```

## Postman Examples

### Block User

**URL:** `PATCH http://localhost:8000/api/admin/users/freelancer/5/block/`

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Body:**
```json
{
  "action": "block",
  "reason": "Violation of platform guidelines"
}
```

### Verify User

**URL:** `POST http://localhost:8000/api/admin/users/verify/`

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Body:**
```json
{
  "user_id": 3,
  "user_type": "freelancer",
  "status": "approved",
  "notes": "Documents verified successfully"
}
```

## Key Design Principles

- **Separation of Concerns** – Admin Service doesn't store user/job data
- **No Data Duplication** – Data remains in source services
- **Secure Access** – Admin-only endpoints with JWT validation
- **Full Audit Trail** – Every action is logged with admin identity
- **Scalable Design** – Microservice-based, independent scaling
- **Graceful Degradation** – Handles service failures gracefully
- **Service Independence** – Can operate even if one service is down

## Testing

### Unit Tests

```bash
python manage.py test admin
```

### Test Admin Actions

Use Postman to test all admin APIs with valid JWT tokens.

## Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure all service URLs correctly
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS/SSL for all endpoints
- [ ] Set up proper logging and monitoring
- [ ] Configure database backups
- [ ] Set up rate limiting
- [ ] Enable CORS for admin dashboard

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues and questions:

- Open an issue on GitHub
- Contact the development team
- Check Django REST Framework documentation
=======
# Admin Service

Admin Service is the administrative API for Labora. It verifies admin JWTs, aggregates data from other microservices through internal endpoints, manages local admin records such as disputes and action logs, and proxies selected service-management operations.

## Responsibilities

- Provide dashboard statistics from Auth, Job, Application, Payment, and Review services.
- Aggregate client and freelancer lists from profile services.
- Block and unblock users by calling Auth Service.
- Verify users locally.
- Proxy job, application, payment, review, skill, and notification administration to the owning services.
- Manage payment disputes and admin action logs locally.

## Features

- Admin-only access through JWT role checks.
- Service-key authenticated calls to internal endpoints on downstream services.
- Local admin action logging for block/unblock, verification, notifications, disputes, and review deletion workflows.
- Paginated admin logs with filters.
- Local dispute resolution and rejection workflows.

## API Endpoints

Base path: `/api/`

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `admin/dashboard/` | Aggregate platform statistics. |
| `GET` | `admin/users/` | Return client and freelancer profile lists. |
| `PATCH` | `admin/users/<role>/<user_id>/block/` | Block a user through Auth Service. |
| `PATCH` | `admin/users/<role>/<user_id>/unblock/` | Unblock a user through Auth Service. |
| `POST` | `admin/users/verify/` | Create a local verified `UserVerification` record. |
| `GET` | `admin/jobs/` | Proxy internal job list. |
| `GET` | `admin/jobs/<job_id>/` | Proxy internal job detail. |
| `GET` | `admin/applications/` | Proxy internal application list. |
| `GET` | `admin/applications/<application_id>/` | Proxy internal application detail. |
| `GET` | `admin/payments/` | Proxy internal payment list. |
| `GET` | `admin/payments/stats/` | Proxy internal payment stats. |
| `GET` | `admin/payments/<payment_id>/` | Proxy internal payment detail. |
| `GET` | `admin/reviews/` | Proxy internal review list. |
| `GET` | `admin/reviews/<review_id>/` | Proxy internal review detail. |
| `DELETE` | `admin/reviews/<review_id>/delete/` | Delete a review through Review Service. |
| `GET`, `POST` | `admin/skills/` | List or create skills through Skill Service. |
| `GET`, `PUT`, `DELETE` | `admin/skills/<skill_id>/` | Manage one skill through Skill Service. |
| `POST` | `admin/notifications/send/` | Send one notification through Notification Service. |
| `POST` | `admin/notifications/broadcast/` | Broadcast notifications through Notification Service. |
| `GET` | `admin/notifications/` | Proxy internal notification history. |
| `GET`, `POST` | `admin/disputes/` | List or create local payment disputes. |
| `GET` | `admin/disputes/<dispute_id>/` | Return a local dispute. |
| `PATCH` | `admin/disputes/<dispute_id>/resolve/` | Mark a dispute resolved. |
| `PATCH` | `admin/disputes/<dispute_id>/reject/` | Mark a dispute rejected. |
| `GET` | `admin/logs/` | List admin action logs with optional filters. |
| `GET` | `admin/logs/<log_id>/` | Return one admin action log. |

## Authentication Requirements

All Admin Service endpoints require `Authorization: Bearer <access_token>` and the token role must pass `labora_admin.permissions.IsAdminUser`. Downstream service calls use `X-Service-Key: <SERVICE_API_KEY>`.

## Internal Service Endpoints

Admin Service primarily consumes internal endpoints exposed by the owning services:

- Auth: user stats, block, unblock.
- Client/Freelancer Profile: internal profile lists.
- Job: internal job list, detail, and stats.
- Application: internal application list, detail, and stats.
- Payment: internal payment list, detail, and stats.
- Review: internal review list, detail, stats, and delete.
- Skill: internal skill CRUD.
- Notification: internal create, broadcast, list, and detail.

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key. |
| `DEBUG` | Enables debug mode when set to `True`. |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | MySQL database configuration. |
| `JWT_PUBLIC_KEY_PATH` | Public key used to verify Auth Service JWTs. |
| `SERVICE_API_KEY` | Shared key used for downstream internal calls. |
| `AUTH_SERVICE_URL`, `CLIENT_PROFILE_SERVICE_URL`, `FREELANCER_PROFILE_SERVICE_URL`, `JOB_SERVICE_URL`, `APPLICATION_SERVICE_URL`, `PAYMENT_SERVICE_URL`, `REVIEW_SERVICE_URL`, `SKILL_SERVICE_URL`, `NOTIFICATION_SERVICE_URL` | Downstream service base URLs. |

## Setup

```bash
cd AdminService
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8011
```

## Service Architecture

- Django project: `adminservice`
- App: `labora_admin`
- Authentication: `labora_admin.authentication.CustomJWTAuthentication`
- Admin permission: `labora_admin.permissions.IsAdminUser`
- Domain views: `labora_admin/views/`
- URL groups: `labora_admin/api_urls/`
- Local data: admin profiles, user verifications, payment disputes, and action logs

## Database Models

- `AdminProfile`: local profile for admin users.
- `UserVerification`: local verification record for client/freelancer users.
- `PaymentDispute`: local dispute state for payment/application ids.
- `AdminActionLog`: local audit log of admin operations.

## Notification/Event Flow

Admin Service does not deliver WebSocket events itself. It calls Notification Service internal endpoints to send or broadcast notifications and records selected notification actions in `AdminActionLog`.
>>>>>>> a387250 (docs(admin): update administrative API documentation)
