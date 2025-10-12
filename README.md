# Agricultural Data Management System

A full-stack web application for managing agricultural data including farmers, crops, markets, and transactions. Built with Python Flask backend and vanilla JavaScript frontend.

## Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete for all data entities
- **Modern UI**: Clean, responsive design with intuitive navigation
- **Real-time Updates**: Dynamic table updates without page refresh
- **Data Validation**: Client and server-side validation
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Python 3.x, Flask, MySQL Connector
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: MySQL
- **Styling**: Custom CSS with modern design patterns

## Database Schema

The application uses four main tables:

1. **Farmers**: Store farmer information (ID, name, village, phone)
2. **Crops**: Manage crop data (ID, name, season)
3. **Markets**: Track market locations (ID, name, location)
4. **Transactions**: Record sales transactions with foreign key relationships

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- MySQL Server
- pip (Python package installer)

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd agricultural_project

# Or simply download and extract the files
```

### 2. Set Up the Database

1. Start your MySQL server
2. Open MySQL command line or MySQL Workbench
3. Run the SQL script to create the database and tables:

```sql
-- Run the contents of database_schema.sql
source database_schema.sql;
```

Or copy and paste the contents of `database_schema.sql` into your MySQL client.

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database Connection

Edit the `DB_CONFIG` in `app.py` to match your MySQL setup:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',      # Change this
    'password': 'your_password',  # Change this
    'database': 'agriculture_db'
}
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Home Page
- Navigate to the main page to see four management options
- Click on any button to access the respective data management page

### Managing Data

#### Farmers Management
- View all farmers in a table format
- Add new farmers with name, village, and phone information
- Edit existing farmer details
- Delete farmers (with confirmation)

#### Crops Management
- Manage crop information including name and season
- Add, edit, or delete crop records

#### Markets Management
- Track market locations and names
- Full CRUD operations for market data

#### Transactions Management
- Record sales transactions
- Link farmers, crops, and markets
- Track quantity and pricing
- Automatic total calculation

### Features

- **Add New Records**: Click "Add New" button to open a form
- **Edit Records**: Click "Edit" button in any table row
- **Delete Records**: Click "Delete" button with confirmation dialog
- **Real-time Updates**: Tables update automatically after changes
- **Data Validation**: Required fields are validated before submission
- **Responsive Design**: Works on all screen sizes

## API Endpoints

The application provides RESTful API endpoints:

### Farmers API
- `GET /api/farmers` - Get all farmers
- `POST /api/farmers` - Create new farmer
- `PUT /api/farmers/<id>` - Update farmer
- `DELETE /api/farmers/<id>` - Delete farmer

### Crops API
- `GET /api/crops` - Get all crops
- `POST /api/crops` - Create new crop
- `PUT /api/crops/<id>` - Update crop
- `DELETE /api/crops/<id>` - Delete crop

### Markets API
- `GET /api/markets` - Get all markets
- `POST /api/markets` - Create new market
- `PUT /api/markets/<id>` - Update market
- `DELETE /api/markets/<id>` - Delete market

### Transactions API
- `GET /api/transactions` - Get all transactions (with joined data)
- `POST /api/transactions` - Create new transaction
- `PUT /api/transactions/<id>` - Update transaction
- `DELETE /api/transactions/<id>` - Delete transaction

## File Structure

```
agricultural_project/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── database_schema.sql    # Database setup script
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── farmers.html      # Farmers management page
│   ├── crops.html        # Crops management page
│   ├── markets.html      # Markets management page
│   └── transactions.html # Transactions management page
└── static/               # Static assets
    ├── style.css         # CSS styles
    └── script.js         # JavaScript functionality
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL server is running
   - Check database credentials in `app.py`
   - Verify database `agriculture_db` exists

2. **Module Not Found Error**
   - Run `pip install -r requirements.txt`
   - Ensure you're using the correct Python version

3. **Port Already in Use**
   - Change the port in `app.py` (last line)
   - Or stop the process using port 5000

4. **CORS Issues**
   - The application includes CORS headers
   - If issues persist, check browser console for errors

### Database Issues

If you encounter foreign key constraint errors:
- Ensure you have sample data in Farmers, Crops, and Markets tables
- Check that referenced IDs exist before creating transactions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please check the troubleshooting section or create an issue in the repository.

