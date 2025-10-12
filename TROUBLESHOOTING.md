# Troubleshooting Guide - Agricultural Data Management

## Issue: "Add New Item" not working in all 4 pages

### Step 1: Test Database Connection

First, run the database test script to verify everything is set up correctly:

```bash
python test_db_connection.py
```

This will check:
- Database connection
- Table existence
- Data in tables

### Step 2: Set Up Database (if needed)

If the database doesn't exist or tables are missing:

1. **Start MySQL server** (if not running)
2. **Run the SQL script**:
   ```sql
   -- Open MySQL command line or MySQL Workbench
   -- Run the contents of database_schema.sql
   source database_schema.sql;
   ```

   Or copy and paste the contents of `database_schema.sql` into your MySQL client.

### Step 3: Install Dependencies

Make sure all Python packages are installed:

```bash
pip install -r requirements.txt
```

### Step 4: Start the Application

```bash
python app.py
```

### Step 5: Test in Browser

1. Open `http://localhost:5000` in your browser
2. Open browser Developer Tools (F12)
3. Go to Console tab
4. Try to add a new item
5. Check console for error messages

### Common Issues and Solutions

#### Issue 1: "Failed to load data" error
**Cause**: Database connection failed
**Solution**: 
- Check if MySQL is running
- Verify database credentials in `app.py`
- Run `test_db_connection.py`

#### Issue 2: "Cannot POST to /api/farmers" error
**Cause**: Flask app not running or wrong URL
**Solution**:
- Make sure Flask app is running on port 5000
- Check if you're accessing the correct URL

#### Issue 3: Modal opens but form doesn't submit
**Cause**: JavaScript errors or form validation
**Solution**:
- Check browser console for JavaScript errors
- Verify all form fields are filled correctly
- Check if required fields are marked with *

#### Issue 4: Database connection error in Flask
**Cause**: Wrong database credentials or database doesn't exist
**Solution**:
- Update `DB_CONFIG` in `app.py` with correct credentials
- Create database using `database_schema.sql`

### Debugging Steps

1. **Check Flask Console**: Look for error messages when starting the app
2. **Check Browser Console**: Look for JavaScript errors
3. **Check Network Tab**: See if API calls are being made
4. **Test API Directly**: Try accessing `http://localhost:5000/api/farmers` directly

### Manual API Testing

You can test the API endpoints directly using curl:

```bash
# Test GET farmers
curl http://localhost:5000/api/farmers

# Test POST farmer
curl -X POST http://localhost:5000/api/farmers \
  -H "Content-Type: application/json" \
  -d '{"farmer_name": "Test Farmer", "village": "Test Village", "phone": "123-456-7890"}'
```

### Database Verification

Check if your database has the correct structure:

```sql
-- Connect to your database
USE dbms_proj;

-- Check tables
SHOW TABLES;

-- Check table structure
DESCRIBE Farmers;
DESCRIBE Crops;
DESCRIBE Markets;
DESCRIBE Transactions;

-- Check data
SELECT * FROM Farmers;
SELECT * FROM Crops;
SELECT * FROM Markets;
SELECT * FROM Transactions;
```

### Still Having Issues?

If you're still having problems:

1. **Check the Flask console output** for any error messages
2. **Check the browser console** (F12 → Console tab) for JavaScript errors
3. **Verify the database** has data by running the test script
4. **Try a simple test**: Add a farmer manually through the database, then see if it appears in the web interface

### Quick Fix Commands

```bash
# Install dependencies
pip install Flask mysql-connector-python flask-cors

# Test database
python test_db_connection.py

# Start app
python app.py
```

### Expected Behavior

When working correctly:
1. Home page loads with 4 navigation buttons
2. Each page shows a table (empty or with data)
3. "Add New" button opens a modal form
4. Form submission creates new records
5. Table updates automatically after adding
6. Edit/Delete buttons work for existing records

