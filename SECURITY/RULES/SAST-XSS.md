# Rule: SAST-XSS — Cross-Site Scripting

## Summary

Cross-site scripting (XSS) occurs when user-supplied input is rendered in a browser context
without escaping, allowing an attacker to inject and execute arbitrary JavaScript.

---

## Accepted Patterns

Always escape or encode user input before rendering it in HTML, attributes, or JavaScript.

**React (JSX)**
```jsx
// ACCEPTED — JSX auto-escapes text content
const element = <div>{userInput}</div>;
```

**JavaScript (DOM)**
```js
// ACCEPTED
element.textContent = userInput;
```

**Python (Jinja2)**
```python
# ACCEPTED — autoescaping enabled
{{ user_input }}  {# safe when autoescape=True #}
```

---

## Anti-Patterns

Never inject user input into HTML without explicit escaping.

**JavaScript (DOM)**
```js
// FORBIDDEN
element.innerHTML = userInput;
```

**Python (Jinja2)**
```python
# FORBIDDEN
{{ user_input | safe }}
```

**JavaScript (document.write)**
```js
// FORBIDDEN
document.write(userInput);
```

---

## Remediation Steps

1. Identify the output point where user input is rendered
2. Replace unsafe rendering methods with safe equivalents:
   - `innerHTML` → `textContent`
   - `| safe` filter → remove the filter and rely on autoescaping
   - `document.write` → use DOM methods with `textContent`
3. Do not sanitize with a custom regex — use the framework's built-in escaping
4. If HTML output is genuinely required, use a well-maintained sanitization library
   (e.g., DOMPurify for JavaScript) and document why raw HTML is needed

---

## Scope

Apply this rule only to the specific output point flagged by the scanner.
Do not audit or modify other rendering locations unless flagged separately.
