# Integrating with Starlette

markupy can be used with Starlette to generate HTML. Since FastAPI is built upon Starlette, markupy can also be used with FastAPI.

To return HTML contents, pass a markupy element to Starlette's `HTMLResponse`:

```python
--8<-- "examples/starlette/html_response.py"
```
