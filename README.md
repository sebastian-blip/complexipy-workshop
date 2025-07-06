# complexipy Workshop Materials

**PyCon Colombia 2025 - A Deep Dive into Code Readability**

This repository contains hands-on exercises and examples for the complexipy workshop, designed to help developers understand and improve code complexity through practical refactoring exercises.

## 🎯 Workshop Overview

This workshop explores the transition from traditional code metrics to modern **Cognitive Complexity** analysis. You'll learn to use `complexipy`, a Rust-based tool, to analyze and improve Python code quality through practical examples and refactoring exercises.

## 📚 Repository Structure

The workshop includes two main modules, each demonstrating different complexity scenarios:

### 1. Password Validator (`password_validator/`)
**Complexity Level:** Beginner to Intermediate

A password validation module that demonstrates:
- Complex conditional logic
- Configuration management
- Pattern detection
- Input validation and error handling

**Files:**
- `src/password_validator.py` - Original implementation with complexity issues
- `tests/test_password_validator.py` - Comprehensive test suite

### 2. Text Analyzer (`text_analyzer/`)
**Complexity Level:** Intermediate to Advanced

A text analysis module that demonstrates:
- Statistical analysis
- Multiple analysis dimensions (words, characters, readability)
- Optional feature configuration
- Complex data processing

**Files:**
- `src/text_analyzer.py` - Original implementation with complexity issues
- `tests/test_text_analyzer.py` - Comprehensive test suite using pytest

## 🧠 What to Expect Based on Your Python Experience

### 🟢 **Beginner Python Developers**
If you're new to Python or have limited experience:

**You'll learn:**
- Basic Python concepts through working examples
- How to read and understand existing code
- The importance of code organization and structure
- Basic testing concepts and how to run tests

**Focus on:**
- Understanding the `password_validator` module first
- Reading through the test files to understand expected behavior
- Comparing original vs. refactored code to see improvements
- Running the provided tests to see how code validation works

### 🟡 **Intermediate Python Developers**
If you have some Python experience:

**You'll learn:**
- Advanced refactoring techniques
- How to identify and reduce code complexity
- Different approaches to problem-solving
- Testing strategies and best practices

**Focus on:**
- Analyzing both modules for complexity patterns
- Understanding the refactoring decisions made
- Experimenting with the `complexipy` tool
- Writing additional tests for edge cases

### 🔴 **Advanced Python Developers**
If you're experienced with Python:

**You'll learn:**
- Cognitive complexity vs. cyclomatic complexity
- Advanced refactoring patterns (Strategy, Factory, etc.)
- Integration of complexity analysis in CI/CD pipelines
- Performance implications of code structure

**Focus on:**
- Deep diving into the refactored implementations
- Understanding the design patterns used

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** (specified in `pyproject.toml`)
- **pip** or **uv** (package manager)
- **Git** (for cloning and version control)

## 🧪 Running Tests

Both modules include comprehensive test suites. Here's how to run them:

### Option 1: Run All Tests
```bash
pytest
```

### Option 2: Run Individual Module Tests

**Password Validator Tests:**
```bash
pytest password_validator/tests/
```

**Text Analyzer Tests:**
```bash
# Using pytest (preferred for this module)
pytest text_analyzer/tests/
```

### Understanding Test Output

- ✅ **Green dots or "PASSED"** - Tests are passing
- ❌ **Red "FAILED"** - Tests are failing (check error messages)
- ⚠️ **Yellow "SKIPPED"** - Tests are skipped (usually conditional)

### Common Test Issues for Beginners

1. **Import errors:** Ensure you're running tests from the workshop directory
2. **Missing dependencies:** Run `pip install pytest` if using pytest directly

## 🔧 Workshop Activities

### Activity 1: Complexity Analysis
Run the complexipy tool on the original implementations:

```bash
# Install complexipy first
pip install complexipy

# Analyze password validator
complexipy password_validator/src/password_validator.py

# Analyze text analyzer
complexipy text_analyzer/src/text_analyzer.py
```

### Activity 3: Hands-on Refactoring
Try refactoring parts of the original code yourself:

1. Identify high-complexity functions
2. Apply refactoring techniques (extract method, guard clauses, etc.)
3. Re-run tests to ensure functionality is preserved
4. Measure complexity improvements

## 📖 Key Learning Concepts

### Refactoring Techniques Demonstrated

1. **Extract Method** - Breaking large functions into smaller, focused functions
2. **Guard Clauses** - Early returns to reduce nesting
3. **Configuration Objects** - Using dataclasses for cleaner configuration
4. **Strategy Pattern** - Separating different analysis strategies
5. **Single Responsibility Principle** - Each class/function has one job

### Testing Strategies

1. **Unit Testing** - Testing individual functions and methods
2. **Edge Case Testing** - Testing boundary conditions and error cases
3. **Integration Testing** - Testing how components work together
4. **Parameterized Testing** - Testing multiple inputs efficiently

---

**Happy coding! 🐍✨**
