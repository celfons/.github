# Rule: SAST-SQLI — SQL Injection

## Summary

SQL injection occurs when user-supplied input is concatenated directly into a SQL query
without parameterization, allowing an attacker to manipulate the query structure.

---

## Accepted Patterns

Always use parameterized queries or prepared statements.

**Node.js (pg)**
```js
// ACCEPTED
const result = await client.query('SELECT * FROM users WHERE id = $1', [userId]);
```

**Python (psycopg2)**
```python
# ACCEPTED
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**Java (JDBC)**
```java
// ACCEPTED
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
stmt.setInt(1, userId);
```

---

## Anti-Patterns

Never concatenate or interpolate user input into SQL strings.

**Node.js**
```js
// FORBIDDEN
const result = await client.query(`SELECT * FROM users WHERE id = ${userId}`);
```

**Python**
```python
# FORBIDDEN
cursor.execute("SELECT * FROM users WHERE id = " + user_id)
```

**Java**
```java
// FORBIDDEN
Statement stmt = conn.createStatement();
stmt.executeQuery("SELECT * FROM users WHERE id = " + userId);
```

---

## Remediation Steps

1. Identify the SQL query that contains user input
2. Replace string concatenation or interpolation with a parameterized placeholder
3. Pass the user input as a bound parameter, not as part of the query string
4. Do not change query logic, table names, or column names
5. Do not add input validation as the sole fix — parameterization is required

---

## Scope

Apply this rule only to the specific line(s) flagged by the scanner.
Do not audit or modify other queries in the same file unless they are flagged separately.
