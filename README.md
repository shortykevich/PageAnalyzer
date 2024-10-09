# Page Analyzer
### Hexlet tests and linter status:
[![Actions Status](https://github.com/shortykevich/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/shortykevich/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/58a7c4b4502e5bba770d/maintainability)](https://codeclimate.com/github/shortykevich/python-project-83/maintainability)

## Description
A simple web application for checking several HTML tags important for SEO

## Installation
```bash
# Clone repo
git clone git@github.com:shortykevich/PageAnalyzer.git && cd PageAnalyzer
# Install dependencies:
make install
# Create .env file and define SECRET_KEY and DATABASE_URL. Example:
echo "SECRET_KEY=your-very-secret-key" >> .env
# To create sqlite file in project directory for testing purposes:
echo "DATABASE_URL=sqlite:///./test.db"
# Or if you have postgres URL:
echo "DATABASE_URL=postgresql://username:password@host:port/database_name" >> .env
```
Initialize the db with:
```bash
make build
```
and start with:
```bash
make start
```
To start Flask Development server:
```bash
make dev
```
### Demo
Checkout [demo!](https://page-analyzer-test-deploy.onrender.com) It may take up to 2 minutes for project to start.
