---
name: code-testing-extensions
description: >-
  Provides file paths to language-specific extension files for the code-testing
  pipeline. Call this skill to discover available extension guidance files
  (e.g., dotnet.md for .NET, cpp.md for C++). Do not use directly — invoked
  by code-testing agents and skills that need language-specific references.
user-invocable: false
license: MIT
---

# Code Testing Extensions

This skill provides access to language-specific guidance files used by the code-testing pipeline. Call this skill to get the file paths, then read the relevant file for your target language.

## Available Extension Files

| File | Language | Contents |
|------|----------|----------|
| [extensions/dotnet.md](code-testing-extensions/extensions/dotnet.md) | .NET (C#/F#/VB) | Build commands, test commands, project reference validation, common CS error codes, MSTest template |
| [extensions/python.md](code-testing-extensions/extensions/python.md) | Python | Framework-adaptive test commands (pytest, custom runners), project layout detection, mocking guidelines, common errors |
| [extensions/typescript.md](code-testing-extensions/extensions/typescript.md) | TypeScript/JavaScript | Build/test commands (Jest/Vitest/Mocha), framework detection, mocking, TS-specific considerations |
| [extensions/powershell.md](code-testing-extensions/extensions/powershell.md) | PowerShell | Test commands (Pester v5), module import patterns, discovery/run pitfalls, mocking, common errors |
| [extensions/cpp.md](code-testing-extensions/extensions/cpp.md) | C++ | Testing internals with friend declarations |
| [extensions/go.md](code-testing-extensions/extensions/go.md) | Go | `go test` commands, table-driven tests, integration vs unit layout, mocking via interfaces, common errors |
| [extensions/java.md](code-testing-extensions/extensions/java.md) | Java | Maven/Gradle commands, JUnit 4/5 and TestNG detection, Mockito, Spring Boot slices, common errors |
| [extensions/rust.md](code-testing-extensions/extensions/rust.md) | Rust | `cargo test` commands, unit vs integration vs doc tests, features, async test harnesses, common errors |
| [extensions/ruby.md](code-testing-extensions/extensions/ruby.md) | Ruby | RSpec and Minitest commands, Bundler usage, Rails specifics, mocking patterns, common errors |
| [extensions/swift.md](code-testing-extensions/extensions/swift.md) | Swift | SPM and Xcode test commands, XCTest vs Swift Testing, `@testable import`, async/throws tests, common errors |
| [extensions/kotlin.md](code-testing-extensions/extensions/kotlin.md) | Kotlin | Gradle commands, JUnit/Kotest detection, MockK, coroutines test, KMP and Android specifics, common errors |
| [extensions/dotnet-examples.md](code-testing-extensions/extensions/dotnet-examples.md) | .NET (C#/F#/VB) | Concrete pipeline examples: sample research output, plan, generated tests, fix cycles, final report |
| [extensions/python-examples.md](code-testing-extensions/extensions/python-examples.md) | Python | Concrete pipeline examples (pytest): research, plan, generated test file, fix cycles, final report |
| [extensions/typescript-examples.md](code-testing-extensions/extensions/typescript-examples.md) | TypeScript/JavaScript | Concrete pipeline examples (Vitest, applicable to Jest): research, plan, generated test file, fix cycles, final report |
| [extensions/go-examples.md](code-testing-extensions/extensions/go-examples.md) | Go | Concrete pipeline examples (standard `testing`): research, plan, table-driven test file, fix cycles, final report |
| [extensions/java-examples.md](code-testing-extensions/extensions/java-examples.md) | Java | Concrete pipeline examples (JUnit 5 + Mockito on Maven): research, plan, generated test file, fix cycles, final report |

## Usage

Read the appropriate extension file for the target language before writing test code. When an `<language>-examples.md` file exists for the target language, read it alongside the base extension to see a concrete end-to-end pipeline walkthrough (research output, plan, generated tests, fix cycles, final report).
