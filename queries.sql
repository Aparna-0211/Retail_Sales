-- =========================
-- Retail Sales SQL Analysis
-- =========================

-- View full table
SELECT * FROM sales;

-- -------------------------
-- Total Sales
-- -------------------------
SELECT SUM(Quantity * UnitPrice) AS TotalSales
FROM sales;

-- -------------------------
-- Total Number of Orders
-- -------------------------
SELECT COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM sales;

-- -------------------------
-- Sales by Country
-- -------------------------
SELECT Country, SUM(Quantity * UnitPrice) AS TotalSales
FROM sales
GROUP BY Country
ORDER BY TotalSales DESC;

-- -------------------------
-- Top 10 Selling Products
-- -------------------------
SELECT Description, SUM(Quantity * UnitPrice) AS TotalSales
FROM sales
GROUP BY Description
ORDER BY TotalSales DESC
LIMIT 10;

-- -------------------------
-- Monthly Sales Trend
-- -------------------------
SELECT 
    strftime('%m', InvoiceDate) AS Month,
    SUM(Quantity * UnitPrice) AS TotalSales
FROM sales
GROUP BY Month
ORDER BY Month;

-- -------------------------
-- Average Order Value
-- -------------------------
SELECT 
    SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo) AS AvgOrderValue
FROM sales;

-- -------------------------
-- Top Customers (if CustomerID exists)
-- -------------------------
SELECT CustomerID, SUM(Quantity * UnitPrice) AS TotalSpent
FROM sales
GROUP BY CustomerID
ORDER BY TotalSpent DESC
LIMIT 10;