---
applyTo: "**/*.py"
---
# Python Deployment Safety

## Production Crashes & Concurrency Bugs
- **Shared Mutable State**: Flag mutable default arguments (e.g., `def fn(items=[])`), which persist across requests in web servers and leak user data or state.
- **Resource & Connection Exhaustion**: Flag database connections, files, or network sessions not opened within a `with` context manager.
- **Silent Failures**: Flag bare `except:` or `except Exception: pass` blocks that swallow critical production errors.
- **Asyncio Pitfalls**: Flag unclosed tasks, missing exception handling on `asyncio.create_task` (fire-and-forget without error tracking), and missing `await` on coroutines.
