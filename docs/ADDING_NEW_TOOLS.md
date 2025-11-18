# Adding a New MCP Tool – Step-by-Step Guide

This document explains **how to add a new MCP tool** in our FastMCP server, using:

* **Pydantic models** for input/output
* A clean separation into:

  * `models/` (schemas)
  * `services/` (business logic)
  * `tools/` (MCP-facing functions)
  * `server/routes.py` (tool registration)
* **Google-style docstrings** so AI agents understand the tool behavior clearly

We’ll cover **two patterns**:

1. ✅ **Pattern A – New Domain Tool (new files)**
   Example: `currency_tool` (completely new feature)
2. ✅ **Pattern B – Math Tool (reuse existing files)**
   Example: `multiply_tool` (leveraging `math_models.py` and `math_service.py`)

---

## 0. Mental Model of Our Architecture

Before adding anything, remember how our project is structured:

```bash
app/
  core/            # config, logging, exceptions
  server/          # MCP server + tool registration
  models/          # Pydantic models (input/output)
  services/        # Business logic, API calls
  tools/           # Tool functions exposed to MCP clients
tests/             # Unit tests per tool/service
run.py             # Entry point
```

**Golden rule:**

> Every new tool should have:
>
> * A Pydantic **input model**
> * A Pydantic **output model**
> * A **service function** that does the real work
> * A **tool function** that MCP exposes
> * A **route registration** entry
> * Tests

---

## 1. Pattern A – New Domain Tool (New Files)

### Scenario

We want to add a **new tool**: `currency_tool`, which converts an amount from one currency to another (e.g. INR → USD).

This will require **new files** in:

* `app/models/currency_models.py`
* `app/services/currency_service.py`
* `app/tools/currency_tool.py`
* `tests/test_currency_tool.py`
* And modifications in `app/server/routes.py`

---

### Step 1: Create Input/Output Models

**File:** `app/models/currency_models.py`

```python
from pydantic import BaseModel, Field
from typing import Optional


class CurrencyConvertInput(BaseModel):
    """Input model for currency conversion tool."""
    from_currency: str = Field(
        ...,
        description="Source currency code (ISO 4217).",
        example="INR"
    )
    to_currency: str = Field(
        ...,
        description="Target currency code (ISO 4217).",
        example="USD"
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Amount to convert.",
        example=1000.0
    )


class CurrencyConvertOutput(BaseModel):
    """Output model for currency conversion result."""
    from_currency: str = Field(..., description="Source currency code.")
    to_currency: str = Field(..., description="Target currency code.")
    original_amount: float = Field(..., description="Original amount.")
    converted_amount: float = Field(..., description="Converted amount.")
    rate: float = Field(..., description="Conversion rate used.")
```

> ✅ Now we have a clear contract for the tool.

---

### Step 2: Implement the Service Logic

**File:** `app/services/currency_service.py`

For now, let’s implement a **stub** (later you can connect to a real FX API):

```python
from app.models.currency_models import CurrencyConvertInput, CurrencyConvertOutput

# In real use, this would call an external API (e.g. Fixer, ExchangeRate API)
MOCK_RATES = {
    ("INR", "USD"): 0.012,
    ("USD", "INR"): 83.0,
}


def convert_currency(input: CurrencyConvertInput) -> CurrencyConvertOutput:
    """
    Convert currency using a mock rate table. Replace with real API calls
    in production.
    """
    key = (input.from_currency.upper(), input.to_currency.upper())
    rate = MOCK_RATES.get(key)

    if rate is None:
        # In production, you'd throw a richer exception type
        raise ValueError(f"No mock rate configured for {key}")

    converted = input.amount * rate

    return CurrencyConvertOutput(
        from_currency=input.from_currency.upper(),
        to_currency=input.to_currency.upper(),
        original_amount=input.amount,
        converted_amount=converted,
        rate=rate,
    )
```

---

### Step 3: Create the MCP Tool Function

**File:** `app/tools/currency_tool.py`

```python
from app.models.currency_models import CurrencyConvertInput, CurrencyConvertOutput
from app.services.currency_service import convert_currency


def currency_convert_tool(input: CurrencyConvertInput) -> CurrencyConvertOutput:
    """
    Convert an amount from one currency to another.

    This MCP tool allows AI Agents and MCP Clients to perform currency
    conversion using a backend service (mock or real). It uses Pydantic
    for strict input and output validation.

    Parameters
    ----------
    input : CurrencyConvertInput
        A Pydantic model containing:
        - from_currency (str): Source currency code, e.g. "INR".
        - to_currency (str): Target currency code, e.g. "USD".
        - amount (float): Amount to convert.

    Returns
    -------
    CurrencyConvertOutput
        A Pydantic model containing:
        - from_currency (str)
        - to_currency (str)
        - original_amount (float)
        - converted_amount (float)
        - rate (float)

    Examples
    --------
    >>> currency_convert_tool(
    ...     CurrencyConvertInput(from_currency="INR", to_currency="USD", amount=1000)
    ... )
    CurrencyConvertOutput(
        from_currency="INR",
        to_currency="USD",
        original_amount=1000.0,
        converted_amount=12.0,
        rate=0.012
    )

    Notes
    -----
    This tool is exposed to MCP clients and may be called by AI Agents
    whenever users ask currency-related questions.
    """
    return convert_currency(input)
```

---

### Step 4: Register the Tool in the MCP Server

**File:** `app/server/routes.py`

Add import + registration:

```python
from fastmcp import FastMCP

# Existing imports...
from app.tools.math_tools import add_tool  # (after we rename)
from app.tools.google_search import google_search_tool
from app.tools.bing_search import bing_search_tool
from app.tools.weather_tool import weather_tool
from app.tools.currency_tool import currency_convert_tool  # ✅ NEW


def register_tools(mcp: FastMCP):
    # Existing tools
    mcp.add_tool(add_tool)
    mcp.add_tool(google_search_tool)
    mcp.add_tool(bing_search_tool)
    mcp.add_tool(weather_tool)

    # New currency tool
    mcp.add_tool(currency_convert_tool)
```

> ✅ Now the MCP server exposes the new `currency_convert_tool` to clients.

---

### Step 5: Add Tests

**File:** `tests/test_currency_tool.py`

```python
from app.tools.currency_tool import currency_convert_tool
from app.models.currency_models import CurrencyConvertInput


def test_currency_conversion_inr_to_usd():
    input_data = CurrencyConvertInput(
        from_currency="INR",
        to_currency="USD",
        amount=1000.0
    )
    result = currency_convert_tool(input_data)
    assert result.from_currency == "INR"
    assert result.to_currency == "USD"
    assert result.original_amount == 1000.0
    # With mock rate 0.012
    assert result.converted_amount == 12.0
```

---

## 2. Pattern B – New Math Tool (Use Existing Files)

### Scenario

We already have:

* `app/models/math_models.py` (with `MathAddInput`, `MathAddOutput`)
* `app/services/math_service.py` (with `add_numbers`)
* `app/tools/math_tools.py` (with `add_tool`)

Now we want to add:

* `multiply_tool`
* `MathMultiplyInput`, `MathMultiplyOutput`
* `multiply_numbers`

We **reuse existing files** instead of creating new ones.

---

### Step 1: Extend the Math Models

**File:** `app/models/math_models.py`

Add below the existing `MathAddInput` / `MathAddOutput`:

```python
from pydantic import BaseModel, Field


class MathAddInput(BaseModel):
    """Input model for the add tool."""
    a: int = Field(..., description="First number to add.", example=2)
    b: int = Field(..., description="Second number to add.", example=3)


class MathAddOutput(BaseModel):
    """Output model for the add tool."""
    result: int = Field(..., description="The computed sum of a and b.")


class MathMultiplyInput(BaseModel):
    """Input model for the multiply tool."""
    a: int = Field(..., description="First number to multiply.", example=3)
    b: int = Field(..., description="Second number to multiply.", example=4)


class MathMultiplyOutput(BaseModel):
    """Output model for the multiply tool."""
    result: int = Field(..., description="The product of a and b.")
```

> ✅ No new file, just extending the existing `math_models.py`.

---

### Step 2: Extend the Math Service

**File:** `app/services/math_service.py`

Assuming we already have:

```python
from app.models.math_models import MathAddInput, MathAddOutput

def add_numbers(input: MathAddInput) -> MathAddOutput:
    return MathAddOutput(result=input.a + input.b)
```

Add multiplication:

```python
from app.models.math_models import (
    MathAddInput,
    MathAddOutput,
    MathMultiplyInput,
    MathMultiplyOutput,
)


def add_numbers(input: MathAddInput) -> MathAddOutput:
    return MathAddOutput(result=input.a + input.b)


def multiply_numbers(input: MathMultiplyInput) -> MathMultiplyOutput:
    """
    Multiply two numbers and return the result.
    """
    return MathMultiplyOutput(result=input.a * input.b)
```

---

### Step 3: Extend the Math Tool File

**File:** `app/tools/math_tools.py`

Assuming we have:

```python
from app.models.math_models import MathAddInput, MathAddOutput
from app.services.math_service import add_numbers


def add_tool(input: MathAddInput) -> MathAddOutput:
    """
    Add two integers and return the computed result.
    ...
    """
    return add_numbers(input)
```

Add the new tool:

```python
from app.models.math_models import (
    MathAddInput,
    MathAddOutput,
    MathMultiplyInput,
    MathMultiplyOutput,
)
from app.services.math_service import add_numbers, multiply_numbers


def add_tool(input: MathAddInput) -> MathAddOutput:
    """
    Add two integers and return the computed result.
    (docstring omitted here for brevity)
    """
    return add_numbers(input)


def multiply_tool(input: MathMultiplyInput) -> MathMultiplyOutput:
    """
    Multiply two integers and return the computed result.

    This MCP tool performs integer multiplication. It uses Pydantic
    models for input/output validation and is exposed as a tool to
    MCP clients and AI agents.

    Parameters
    ----------
    input : MathMultiplyInput
        A Pydantic model containing:
        - a (int): First integer.
        - b (int): Second integer.

    Returns
    -------
    MathMultiplyOutput
        A Pydantic model containing:
        - result (int): Product of `a` and `b`.

    Examples
    --------
    >>> multiply_tool(MathMultiplyInput(a=3, b=4))
    MathMultiplyOutput(result=12)
    """
    return multiply_numbers(input)
```

---

### Step 4: Register the New Math Tool

**File:** `app/server/routes.py`

Add it to the registry:

```python
from fastmcp import FastMCP

from app.tools.math_tools import add_tool, multiply_tool
from app.tools.google_search import google_search_tool
from app.tools.bing_search import bing_search_tool
from app.tools.weather_tool import weather_tool
from app.tools.currency_tool import currency_convert_tool


def register_tools(mcp: FastMCP):
    # Math tools
    mcp.add_tool(add_tool)
    mcp.add_tool(multiply_tool)  # ✅ new

    # External tools
    mcp.add_tool(google_search_tool)
    mcp.add_tool(bing_search_tool)
    mcp.add_tool(weather_tool)
    mcp.add_tool(currency_convert_tool)
```

---

### Step 5: Add Tests

**File:** `tests/test_math_tools.py`

Extend existing tests:

```python
from app.tools.math_tools import add_tool, multiply_tool
from app.models.math_models import MathAddInput, MathMultiplyInput


def test_add_tool():
    result = add_tool(MathAddInput(a=2, b=3))
    assert result.result == 5


def test_multiply_tool():
    result = multiply_tool(MathMultiplyInput(a=3, b=4))
    assert result.result == 12
```

---

## 3. Quick Checklist for Team Members

When adding a **new tool**, always:

1. **Decide the pattern**

   * New domain → new files in `models/`, `services/`, `tools/`
   * Existing domain → extend existing files

2. **Create/extend Pydantic models**

   * Input model (`*Input`)
   * Output model (`*Output`)

3. **Create/extend service**

   * Implement logic, call APIs, handle errors

4. **Create/extend tool**

   * Call service function
   * Add **Google-style docstring** (parameters, returns, examples, notes)

5. **Register tool in `app/server/routes.py`**

   * Import tool
   * `mcp.add_tool(your_tool)`

6. **Add tests in `tests/`**

   * At least one positive test
   * Add edge case tests when relevant