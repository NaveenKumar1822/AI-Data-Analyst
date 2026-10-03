# 📊 AI Data Analyst

### Natural Language → SQL → Analytics

An AI-powered natural-language analytics assistant that allows users to interact with a relational retail database using plain English.

Instead of manually writing SQL queries, users can ask questions such as:

> "Which product generated the highest revenue?"

The system uses an LLM to translate the natural-language question into SQL, executes the generated query against a SQLite database, and displays the resulting data through an interactive Streamlit application.

---

## 🚀 Overview

Business analysts and data professionals frequently need to query databases to answer questions about revenue, customers, products, regions, and business performance.

However, answering these questions traditionally requires knowledge of:

- SQL
- Database schemas
- Table relationships
- Joins
- Aggregations
- Filtering
- Date-based analysis

The **AI Data Analyst** project explores how Large Language Models can simplify this workflow by allowing users to interact with structured data using natural language.

The application combines:

- Large Language Models
- Natural Language Processing
- Text-to-SQL generation
- Relational databases
- Python
- LangChain
- Streamlit

The project is designed as a practical demonstration of how Generative AI can be integrated into a traditional data analytics workflow.

---

# 🎯 Problem Statement

A typical business user may want to ask questions such as:

- Which product generated the highest revenue?
- What is the total revenue by region?
- Which category generated the most revenue?
- What were the monthly revenues in 2025?
- Who are the top 10 customers by revenue?

A traditional workflow would require the user to understand the database structure and manually write SQL.

For example:

```sql
SELECT
    p.product_name,
    SUM(o.revenue) AS total_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 1;