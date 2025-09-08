from mcp.server.fastmcp import FastMCP
import requests
import os
from typing import Optional, Literal
from pathlib import Path

# Create an MCP server with BODMAS calculation capabilities
mcp = FastMCP("BODMAS Calculator Server")

# Add a prompt for BODMAS calculations
@mcp.prompt()
def bodmas_calculation_prompt(expression: str) -> str:
    """
    A prompt to help users structure their BODMAS calculation query for the LLM.
    
    Args:
        expression: The mathematical expression to evaluate
        
    Returns:
        A structured prompt that guides the LLM to use the available tools
    """
    return f"""You are a BODMAS calculation assistant with access to mathematical operation tools.

**Expression to evaluate:** {expression}

**Your task:**
1. First, check the bodmas_chart.jpg resource to understand the order of operations
2. Break down the expression according to BODMAS rules:
   - B: Brackets (Parentheses) first
   - O: Orders (Exponents/Powers) 
   - D: Division and M: Multiplication (left to right)
   - A: Addition and S: Subtraction (left to right)

3. Use the available tools to calculate step by step:
   - add(a, b) - for addition
   - subtract(a, b) - for subtraction  
   - multiply(a, b) - for multiplication
   - divide(a, b) - for division
   - power(base, exponent) - for exponents

4. Show each step clearly:
   - Identify which operation to perform first according to BODMAS
   - Call the appropriate tool with the correct arguments
   - Use the result in the next step
   - Continue until you reach the final answer

Please evaluate: {expression}

Remember to always follow BODMAS order and use the tools for each calculation step."""

# Resource for BODMAS image
@mcp.resource(
    uri="file://resources/bodmas_chart.jpg",
    name="bodmas_chart.jpg", 
    title="BODMAS Order of Operations Chart",
    mime_type="image/jpeg"
)
def bodmas_chart_image() -> bytes:
    """
    Visual chart showing BODMAS order of operations.
    Returns the image as bytes.
    """
    try:
        image_path = Path("resources/bodmas.jpg")
        with open(image_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        # Return empty bytes if file not found
        print("Warning: bodmas_chart.jpg not found")
        return b""
    except Exception as e:
        print(f"Error loading image: {e}")
        return b""

# Additional text resource for BODMAS guide
@mcp.resource(
    uri="file://resources/bodmas_guide.md",
    name="bodmas_guide.md",
    title="BODMAS Quick Reference Guide",
    mime_type="text/markdown"
)
def bodmas_guide() -> str:
    """
    Quick reference guide to BODMAS order of operations.
    """
    return """# BODMAS Quick Reference

## Order of Operations:
1. **B**rackets (Parentheses) - ( ), [ ], { }
2. **O**rders (Powers/Exponents) - ^, ², ³, √
3. **D**ivision ÷ / and **M**ultiplication × * (left to right)
4. **A**ddition + and **S**ubtraction - (left to right)

## Remember:
- Always work from left to right within the same priority level
- Complete innermost brackets first
- See bodmas_chart.jpg for visual reference
"""

@mcp.tool()
def add(a: float, b: float) -> float:
    """
    Add two numbers together (BODMAS: Addition operation).
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    result = a + b
    return result

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    Subtract the second number from the first number (BODMAS: Subtraction operation).
    
    Args:
        a: First number (minuend)
        b: Second number (subtrahend)
    
    Returns:
        The difference of a minus b
    """
    result = a - b
    return result

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers together (BODMAS: Multiplication operation).
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The product of a and b
    """
    result = a * b
    return result

@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    Divide the first number by the second number (BODMAS: Division operation).
    
    Args:
        a: First number (dividend)
        b: Second number (divisor)
    
    Returns:
        The quotient of a divided by b
    
    Raises:
        ValueError: If attempting to divide by zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    
    result = a / b
    return result

@mcp.tool()
def power(base: float, exponent: float) -> float:
    """
    Calculate base raised to the power of exponent (BODMAS: Orders/Exponents operation).
    
    Args:
        base: The base number
        exponent: The power to raise the base to
    
    Returns:
        The result of base^exponent
    """
    result = base ** exponent
    return result

# Create ASGI app for cloud deployment
app = mcp.serve().asgi()

# For local testing and cloud deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )