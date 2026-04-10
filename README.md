# Restaurant Management & Ordering Application

## Project Overview

A comprehensive multi-venue restaurant management and ordering system with customer-facing menu browsing, cart management, real-time order tracking, and manager dashboard for operations, staff management, and menu configuration.

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **WebSocket**: For real-time order updates
- **Payment Gateway**: Razorpay
- **Authentication**: JWT (JSON Web Tokens)

### Frontend
- **Framework**: React 18
- **UI Library**: Material-UI (MUI)
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Real-time Communication**: WebSocket
- **Routing**: React Router v6

### DevOps
- **Containerization**: Docker & Docker Compose
- **Local Development**: MongoDB, FastAPI server, React dev server

## Project Structure

```
HotelManagment/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── models/          # Data models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── __init__.py
│   ├── config/
│   │   ├── settings.py      # Configuration settings
│   │   ├── database.py      # MongoDB connection
│   │   └── __init__.py
│   ├── tests/               # Unit and integration tests
│   ├── main.py              # FastAPI app entry point
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example         # Environment template
│   ├── Dockerfile           # Docker image for backend
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API and WebSocket services
│   │   ├── hooks/          # Custom React hooks
│   │   ├── contexts/       # React Context providers
│   │   ├── assets/         # Images, fonts, etc.
│   │   ├── __tests__/      # Component tests
│   │   ├── App.js          # Main App component
│   │   └── index.js        # React entry point
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── package.json        # Node dependencies
│   ├── .env.example        # Environment template
│   ├── Dockerfile          # Docker image for frontend
│   └── .gitignore
│
├── database/
│   └── init_db.py          # MongoDB initialization script
│
├── docker-compose.yml      # Docker Compose configuration
├── plan.md                 # Project planning document
└── detailed_plan.md        # Detailed implementation plan
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development without Docker)
- Python 3.11+ (for local backend development without Docker)
- MongoDB (local or Atlas)

### Using Docker Compose (Recommended)

1. **Clone the repository and navigate to project directory**
   ```bash
   cd HotelManagment
   ```

2. **Create environment files**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. **Update `.env` files with your credentials**
   - Razorpay API keys
   - Zomato/Swiggy API keys (optional)
   - Secret keys for JWT

4. **Start all services**
   ```bash
   docker-compose up --build
   ```

5. **Initialize MongoDB with sample data** (in another terminal)
   ```bash
   docker exec restaurant_backend python -m pip install motor
   python database/init_db.py
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MongoDB: localhost:27017 (admin/admin123)

### Local Development (Without Docker)

#### Backend Setup

1. **Create Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```

4. **Start MongoDB** (locally or use MongoDB Atlas)
   ```bash
   mongod
   ```

5. **Initialize database**
   ```bash
   python ../database/init_db.py
   ```

6. **Run FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend Setup

1. **Install Node dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```

3. **Start React dev server**
   ```bash
   npm start
   ```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register-manager` - Register a new manager
- `POST /api/auth/login-manager` - Login and get JWT token
- `POST /api/auth/refresh-token` - Refresh JWT token
- `POST /api/auth/logout` - Logout

### Menu Endpoints
- `GET /api/cuisines/{venue_id}` - Get all cuisines
- `GET /api/cuisines/{venue_id}/{cuisine_id}/items` - Get items by cuisine
- `GET /api/items/search` - Search items (params: q, venue_id)
- `POST /api/items` - Add new food item (Manager only)
- `PUT /api/items/{item_id}` - Edit food item (Manager only)
- `DELETE /api/items/{item_id}` - Delete food item (Manager only)

### Order Endpoints
- `POST /api/orders/create` - Create a new order
- `GET /api/orders/{tracking_id}` - Get order status by tracking ID
- `GET /api/orders/search` - Search orders (params: order_id, customer_phone)
- `PUT /api/orders/{order_id}/status` - Update order status (Manager only)
- `GET /api/orders/venue/{venue_id}` - Get all venue orders (Manager only)

### Payment Endpoints
- `POST /api/payments/create-order` - Create Razorpay order
- `POST /api/payments/verify` - Verify payment after transaction

### WebSocket
- `WS /ws/orders/{order_id}` - Real-time order status updates

## Cuisines & Menu Items

The application includes 50+ pre-loaded food items across:

- **North Indian**: Butter Chicken, Biryani, Tandoori Chicken, Naan, Paneer Tikka Masala
- **Marathi**: Vada Pav, Misal Pav, Puran Poli
- **Gujarati**: Dhokla, Undhiyu, Fafda & Jalebi
- **South Indian**: Masala Dosa, Idli Sambar, Uttapam, Chettinad Chicken
- **Chinese**: Kung Pao Chicken, Fried Rice, Chow Mein, Spring Rolls
- **Italian**: Margherita Pizza, Spaghetti Carbonara, Penne Arrabbiata, Pepperoni Pizza
- **Beverages**: Lassi, Chai Tea, Mango Smoothie, Orange Juice

## User Roles

### Customer
- No login required
- Browse menu by cuisine
- Search for items
- Add items to cart
- Checkout and make payment
- Receive tracking ID
- Track order status in real-time

### Hotel Manager
- Login with credentials
- View and manage orders
- Add/edit cuisines and food items
- Manage staff (kitchen, delivery, front-desk)
- Add and manage multiple venues (branches)
- Configure Zomato/Swiggy integration
- View order analytics

## Key Features

✅ **Multi-Venue Support** - Manage multiple restaurant branches  
✅ **Real-Time Order Tracking** - WebSocket-based live updates  
✅ **Cuisine Hierarchy** - Organized menu by cuisine type  
✅ **Payment Integration** - Razorpay (UPI, Cards, Wallets, Net Banking)  
✅ **Staff Management** - Add and manage different staff types  
✅ **Order Status Updates** - Kitchen, Delivery, Customer views  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **Zomato/Swiggy Ready** - API structure for integration  

## Next Steps (Phase 2 Onwards)

1. **Implement Authentication Routes** - Manager login/signup endpoints
2. **Develop Customer UI** - Menu, cart, checkout components
3. **Develop Manager Dashboard** - Order management, menu management
4. **Implement Payment Integration** - Razorpay integration
5. **Add Real-Time Features** - WebSocket for live order updates
6. **Zomato/Swiggy Integration** - Menu sync and order webhooks
7. **Testing & Deployment** - Unit tests, E2E tests, production deployment

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=restaurant_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
ZOMATO_API_KEY=your_zomato_key
SWIGGY_API_KEY=your_swiggy_key
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_RAZORPAY_KEY_ID=your_key_id
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod`
- Check connection string in `.env`
- Verify database exists or will auto-create

### Backend Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Frontend Compilation Errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

Private project - All rights reserved

## Support

For issues and questions, contact: manager@indiandelight.com
