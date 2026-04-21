# Rule: SAST-RCE — Remote Code Execution

## Summary

Remote code execution (RCE) occurs when user-supplied input is passed to a system shell,
process spawner, or dynamic evaluator, allowing an attacker to execute arbitrary commands
or code on the server.

---

## Accepted Patterns

Avoid shell invocation with user input entirely. When process execution is required,
use argument arrays (not shell strings) and never include user input in command names.

**Node.js**
```js
// ACCEPTED — array form, no shell
const { execFile } = require('child_process');
execFile('convert', ['-resize', userWidth + 'x', inputPath, outputPath], callback);
```

**Python**
```python
# ACCEPTED — list form, shell=False
import subprocess
subprocess.run(['convert', '-resize', user_width + 'x', input_path, output_path])
```

---

## Anti-Patterns

Never pass user input to shell-string execution functions.

**Node.js**
```js
// FORBIDDEN
const { exec } = require('child_process');
exec(`convert -resize ${userWidth}x ${inputPath} ${outputPath}`, callback);
```

**Python**
```python
# FORBIDDEN
import os
os.system('convert -resize ' + user_width + 'x ' + input_path)
```

**JavaScript (eval)**
```js
// FORBIDDEN
eval(userCode);
```

**Python**
```python
# FORBIDDEN
eval(user_expression)
```

---

## Remediation Steps

1. Identify the function receiving user input that executes a command or evaluates code
2. If the function accepts a shell string, replace it with the array/list form:
   - `exec(string)` → `execFile(cmd, [args])` (Node.js)
   - `os.system(string)` → `subprocess.run([cmd, args], shell=False)` (Python)
3. Ensure the command name itself is a hardcoded constant, never derived from user input
4. If `eval` or equivalent is used, remove it entirely and implement the logic explicitly
5. Do not add input validation as the sole fix — shell-safe invocation is required

---

## Scope

Apply this rule only to the specific invocation flagged by the scanner.
Do not audit or modify other command executions unless flagged separately.
