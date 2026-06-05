"""
Runner that monkeypatches the `arxiv.Client` defaults to be more conservative
(before importing your retriever module). This avoids changing your project
code; it only alters runtime behavior for this run.

Usage (PowerShell):
& .venv\Scripts\python.exe run_arxiv_safe.py
"""

import importlib
import sys

# Monkeypatch arxiv.Client.__init__ before anything else imports arxiv.
try:
    import arxiv
except Exception:
    print("arxiv package not installed in venv. Please install with: pip install arxiv")
    sys.exit(1)

# Keep original initializer
_orig_client_init = arxiv.Client.__init__

def _patched_client_init(self, page_size: int = 100, delay_seconds: float = 3.0, num_retries: int = 3, *args, **kwargs):
    # Use safer defaults: smaller page_size, longer delay, more retries
    safe_page_size = min(page_size, 20)
    safe_delay_seconds = max(delay_seconds, 5.0)
    safe_num_retries = max(num_retries, 5)
    return _orig_client_init(self, page_size=safe_page_size, delay_seconds=safe_delay_seconds, num_retries=safe_num_retries, *args, **kwargs)

arxiv.Client.__init__ = _patched_client_init

print("Patched arxiv.Client defaults: page_size<=20, delay_seconds>=5.0, num_retries>=5")

# Now import and run your retriever module (which will instantiate and run the query)
# Import by module path to avoid executing as a script twice.
try:
    spec = importlib.util.spec_from_file_location("user_arxiv_retriever", r"retrievers\arixv.py")
    user_mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = user_mod
    spec.loader.exec_module(user_mod)
except Exception as e:
    print("Runner failed:", e)
    raise
