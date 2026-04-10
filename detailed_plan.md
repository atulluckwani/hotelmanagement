# Hotel Management & Restaurant Ordering Application

## Plan Overview

**TL;DR**: Build a full-stack restaurant application with multiple venues (branches), supporting customers (no-login menu browsing + cart), Hotel Managers (with login for admin), and multiple staff types. Include real-time order tracking, Razorpay payments, and Zomato/Swiggy integration for delivery & platform listing across cuisines (Indian, Chinese, Italian) with WebSocket-based live updates.

---

## Requirements Summary

### Confirmed Decisions
- **Zomato/Swiggy**: Full integration (API + platform listing)
- **Venues**: Multi-location support (separate branches)
- **Staff Types**: Delivery, Kitchen, Front-desk
- **Database**: MongoDB
- **Scope**: Full application build
- **Payment**: Razorpay gateway (UPI, cards, net banking, wallets)
- **Auth**: Username/password for Hotel Manager, no login for customers
- **Order Tracking**: Real-time WebSocket updates
- **Tech Stack**: React (frontend), Python FastAPI (backend), MongoDB, WebSockets

### Cuisines & Menu
- **Indian**: North Indian, Marathi, Gujarati, South Indian
- **International**: Chinese, Italian
- **Beverages**: Tea, Lassi, Coffee, Wine, Soft drinks, etc.

---

## Implementation Phases

### Phase 1: Project Setup & Database Design

#### Step 1: Initialize Frontend (React.js)
- Create React project with TypeScript
- Set up routing (React Router v6)
- Install UI library (Material-UI or Ant Design)
- Configure Axios + WebSocket client
- Folder structure: `src/{components,pages,hooks,services,contexts,assets}`

#### Step 2: Initialize Backend (Python FastAPI)
- Set up FastAPI application
- Install: pymongo, pydantic, python-dotenv, websockets, razorpay, requests
- Folder structure: `backend/{app,config,models,routes,services,utils,schemas}`
- Configure CORS for frontend

#### Step 3: Design MongoDB Schema

**Collections:**

1. **Venues**
{
id: ObjectId,
name: String,
address: String,
phone: String,
email: String,
city: String,
cuisines: [ObjectId],
staff: [ObjectId],
operating_hours: Object,
created_at: DateTime
}
2. **Users**
{
id: ObjectId,
role: String (customer/manager/staff),
email: String,
phone: String,
password_hash: String,
venue_id: ObjectId (for staff/manager),
preferences: Object,
created_at: DateTime
}
3. **Cuisines**
{
id: ObjectId,
name: String,
description: String,
image_url: String,
venue_id: ObjectId,
items_count: Number
}
4.4. **FoodItems**
{
id: ObjectId,
name: String,
description: String,
price: Number,
cuisine_id: ObjectId,
venue_id: ObjectId,
image_url: String,
availability: Boolean,
dietary_info: String,
ratings: Number,
created_at: DateTime
}

5. **Orders**
{
order_id: String (unique),
customer_phone: String,
venue_id: ObjectId,
items: [
{
food_id: ObjectId,
qty: Number,
price: Number
}
],
total_amount: Number,
payment_status: String (pending/paid/failed),
order_status: String (pending/accepted/preparing/ready/out_for_delivery/delivered),
order_type: String (dine-in/delivery),
created_at: DateTime,
tracking_updates: [Object],
assigned_delivery_staff_id: ObjectId,
delivery_address: String
}
6. **Payments**
{
id: ObjectId,
order_id: String,
razorpay_id: String,
mode: String (upi/card/wallet/netbanking),
amount: Number,
status: String (pending/success/failed),
created_at: DateTime
}
7. **Staff**
{
id: ObjectId,
name: String,
phone: String,
email: String,
role: String (kitchen/delivery/front_desk),
venue_id: ObjectId,
salary: Number,
join_date: DateTime,
status: String (active/inactive)
}
8. **ZomatoSwiggyIntegration**
{
venue_id: ObjectId,
platform: String (zomato/swiggy),
api_key: String (encrypted),
menu_sync_status: String,
last_sync: DateTime,
restaurant_id: String (platform's ID)
}


---

### Phase 2: Backend API Development

#### Step 4: Authentication Routes (`backend/app/routes/auth.py`)
- `POST /api/auth/register-manager` — Hotel Manager signup
- `POST /api/auth/login-manager` — Login, returns JWT token
- `POST /api/auth/refresh-token` — Refresh JWT
- `POST /api/auth/logout` — Logout

#### Step 5: Cuisine & Food Item Routes (`backend/app/routes/menu.py`)
- `GET /api/cuisines/{venue_id}` — List cuisines for venue
- `GET /api/cuisines/{venue_id}/{cuisine_id}/items` — Items by cuisine
- `GET /api/items/search?q={query}&venue_id={id}` — Search items
- `POST /api/cuisines` — Add cuisine (Manager only)
- `PUT /api/cuisines/{cuisine_id}` — Edit cuisine (Manager only)
- `POST /api/items` — Add food item (Manager only)
- `PUT /api/items/{item_id}` — Edit item (Manager only)
- `DELETE /api/items/{item_id}` — Delete item (Manager only)

#### Step 6: Order Management Routes (`backend/app/routes/orders.py`)
- `POST /api/orders/create` — Create order, returns tracking_id
- `GET /api/orders/{tracking_id}` — Order status by tracking ID
- `GET /api/orders/search?order_id={id}&customer_phone={phone}` — Manager search
- `PUT /api/orders/{order_id}/status` — Update order status
- `GET /api/orders/venue/{venue_id}` — All orders for venue (Manager only)
- `WS /ws/orders/{order_id}` — WebSocket for real-time updates

#### Step 7: Payment Routes (`backend/app/routes/payments.py`)
- `POST /api/payments/create-order` — Razorpay order creation
- `POST /api/payments/verify` — Webhook verification
- `GET /api/payments/{order_id}` — Payment details

#### Step 8: Venue & Staff Routes
- `backend/app/routes/venues.py`
  - `POST /api/venues` — Add venue (Manager only)
  - `GET /api/venues/{manager_id}` — Get managed venues
  - `PUT /api/venues/{venue_id}` — Edit venue
  
- `backend/app/routes/staff.py`
  - `POST /api/staff` — Add staff (Manager only)
  - `GET /api/staff/{venue_id}` — Get venue staff
  - `PUT /api/staff/{staff_id}` — Edit staff
  - `DELETE /api/staff/{staff_id}` — Remove staff

#### Step 9: Zomato/Swiggy Integration Routes (`backend/app/routes/integrations.py`)
- `POST /api/integrations/sync-menu` — Push menu to platforms (Manager only)
- `PUT /api/integrations/api-keys` — Store API credentials (Manager only)
- `POST /api/integrations/zomato/webhook` — Receive Zomato orders
- `POST /api/integrations/swiggy/webhook` — Receive Swiggy orders

---

### Phase 3: Frontend Development

#### Step 10: Customer-Facing Components

**Components** (`frontend/src/components`):
- `CuisineHierarchy.js` — Display cuisines as tabs/categories
- `FoodItemCard.js` — Item display with price, image, add-to-cart
- `SearchBar.js` — Search across items
- `Cart.js` — Shopping cart with quantity controls
- `Checkout.js` — Delivery/dine-in selection
- `PaymentModal.js` — Razorpay integration
- `OrderTracking.js` — Real-time status updates

**Pages** (`frontend/src/pages`):
- `Menu.js` — Main menu with cuisine hierarchy
- `OrderConfirmation.js` — Show tracking ID after order
- `OrderStatus.js` — Track by ID or phone

#### Step 11: Hotel Manager Dashboard (`frontend/src/pages/ManagerDashboard`)

- `LoginPanel.js` — Manager authentication
- `MenuManagement.js` — Add/edit cuisines & items
- `OrderManagement.js` — View & update order status
- `StaffManagement.js` — Add/edit staff
- `VenueManagement.js` — Add/edit branches
- `IntegrationSettings.js` — Zomato/Swiggy API configuration
- `OrderDashboard.js` — Real-time kitchen order board
- `AnalyticsWidget.js` — Basic stats (orders, revenue)

#### Step 12: WebSocket Setup (`frontend/src/services/websocket.js`)
- Initialize WebSocket client for real-time order updates
- Auto-reconnect on disconnect
- Emit updates to UI without page reload

---

### Phase 4: Integrations & Payments

#### Step 13: Razorpay Payment Integration (`backend/app/services/payment_service.py`)
- Create Razorpay order on checkout
- Verify payment via webhook with signature validation
- Update order payment status
- Support: UPI, Credit/Debit Cards, Net Banking, Wallets

#### Step 14: Zomato Integration (`backend/app/services/zomato_service.py`)
- Authenticate via API key
- Upload restaurant menu to Zomato
- Listen to order webhooks from Zomato
- Update order status back to Zomato
- Sync delivery partner availability

#### Step 15: Swiggy Integration (`backend/app/services/swiggy_service.py`)
- Similar to Zomato implementation
- Authenticate, upload menu, listen to orders, update status

---

### Phase 5: Real-Time Features

#### Step 16: Implement WebSocket Server (`backend/app/websocket.py`)
- Connection manager to track active sessions
- Broadcast order status changes
- Allow kitchen staff to update status in real-time
- Notify delivery staff when orders are ready

#### Step 17: Kitchen Order Board
- Display incoming orders by queue time
- Staff mark items as "preparing", "ready"
- WebSocket broadcast to customer & delivery staff

---

### Phase 6: Core Services

#### Step 18: Backend Services (`backend/app/services/`)

- `order_service.py` — Create order, validate items, calculate totals
- `menu_service.py` — Manage cuisines and items
- `venue_service.py` — Multi-venue management
- `staff_service.py` — Staff operations by role
- `auth_service.py` — JWT generation/verification
- `notification_service.py` — Email/SMS notifications (optional)

#### Step 19: Database Optimization (`backend/config/database.py`)
- Index orders: `order_id`, `customer_phone`, `venue_id`, `created_at`
- Index items: `cuisine_id`, `venue_id`
- Compound indexes for search queries

---

### Phase 7: Testing & QA

#### Step 20: Backend Unit Tests (`backend/tests/`)
- Authentication (JWT generation, validation)
- Order creation (item validation, pricing)
- Payment verification
- Role-based access control
- Zomato/Swiggy webhook responses

#### Step 21: Frontend Integration Tests (`frontend/src/__tests__/`)
- Menu loading & cuisine hierarchy
- Add-to-cart functionality
- Checkout & payment flow
- Order tracking with WebSocket
- Manager login & dashboard operations

#### Step 22: End-to-End Testing
- Full customer flow: Browse → Cart → Checkout → Payment → Track
- Manager flow: Login → Manage → View orders → Update status
- Zomato/Swiggy webhooks → Order creation
- Real-time WebSocket updates across clients

#### Step 23: Load Testing
- 100+ concurrent customers browsing
- 50+ live orders with real-time updates
- WebSocket stability under load
- Target: <2s response time

---

### Phase 8: Deployment

#### Step 24: Local Development (docker-compose.yml)
- MongoDB container
- FastAPI backend container
- React frontend development server
- Environment variables (.env)

#### Step 25: Production Deployment
- Backend: AWS ECS or Google Cloud Run
- Frontend: AWS S3 + CloudFront or Firebase Hosting
- Database: MongoDB Atlas
- CI/CD: GitHub Actions

---

## Critical Files to Create

| File | Purpose |
|------|---------|
| `frontend/src/pages/Menu.js` | Customer menu with cuisine hierarchy |
| `frontend/src/pages/ManagerDashboard/index.js` | Manager dashboard |
| `frontend/src/components/OrderTracking.js` | Real-time WebSocket order status |
| `backend/app/routes/auth.py` | Manager authentication |
| `backend/app/routes/orders.py` | Order CRUD & WebSocket |
| `backend/app/routes/menu.py` | Food items & cuisines |
| `backend/app/routes/payments.py` | Razorpay integration |
| `backend/app/routes/integrations.py` | Zomato/Swiggy webhooks |
| `backend/app/services/payment_service.py` | Razorpay logic |
| `backend/app/services/zomato_service.py` | Zomato API client |
| `backend/app/services/swiggy_service.py` | Swiggy API client |
| `backend/app/websocket.py` | WebSocket manager |
| `backend/config/database.py` | MongoDB & indexes |
| `docker-compose.yml` | Local dev environment |

---

## Order Status Flow
pending → accepted → preparing → ready → out_for_delivery → delivered


Each status change triggers WebSocket broadcast to customer & staff.

---

## Key Features Checklist

### Customer Features
- [x] Browse menu by cuisine hierarchy
- [x] Search food items
- [x] Add to cart, adjust quantities
- [x] Checkout with dine-in/delivery options
- [x] Razorpay payment (UPI, cards, wallet, net banking)
- [x] Receive tracking ID (no login required)
- [x] Real-time order status via WebSocket
- [x] Track order by ID or phone number

### Manager Features
- [x] Login with credentials
- [x] Add/edit/delete cuisines
- [x] Add/edit/delete food items
- [x] Add/edit/delete staff (kitchen, delivery, front-desk)
- [x] Add/edit venues (branches)
- [x] View all orders for venue
- [x] Update order status
- [x] Configure Zomato/Swiggy API keys
- [x] Sync menu to platforms
- [x] Real-time kitchen order board
- [x] View analytics (orders, revenue)

### System Features
- [x] Multi-venue support
- [x] Real-time WebSocket updates
- [x] Zomato integration (menu sync, order webhooks)
- [x] Swiggy integration (menu sync, order webhooks)
- [x] Razorpay payment processing
- [x] Role-based access control
- [x] Order database persistence

---

## Development Notes

- Start with Phase 1 (setup) and Phase 2 (APIs) in parallel
- Cuisines: Start with 5-8 items per cuisine (40-50 total), expand based on sales
- Payment: Configure Razorpay dashboard first, get API keys
- Integrations: Zomato/Swiggy developer accounts needed for API access
- Testing: Use Razorpay sandbox mode before production
- WebSocket: Test with multiple browser tabs to verify real-time delivery

---

## Timeline Estimate

- **Phase 1 (Setup)**: 2-3 days
- **Phase 2 (Backend APIs)**: 5-7 days
- **Phase 3 (Frontend)**: 5-7 days
- **Phase 4 (Integrations)**: 3-4 days
- **Phase 5-6 (Real-time & Services)**: 3-4 days
- **Phase 7 (Testing)**: 3-4 days
- **Phase 8 (Deployment)**: 2-3 days

**Total: 4-5 weeks** for complete implementation

---

## Next Steps

1. Proceed with Phase 1: Create project structure
2. Set up MongoDB locally or Atlas
3. Create API skeleton with FastAPI
4. Initialize React frontend structure
5. Begin Phase 2 API implementation with Phase 3 frontend components in parallel
