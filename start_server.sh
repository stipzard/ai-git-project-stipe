#!/bin/bash

# Automatski postavlja ključ za ovu sesiju
export GEMINI_API_KEY="AIzaSyCaJCQZdE0e0JsQkNbvlghiWWWF3gceqP8"

echo "AI ključ je postavljen. Pokrećem Flask server..."

# Pokreće Python server
py server.py

# Napomena: Ovu datoteku NEMOJTE dodati u Git jer sadrži ključ!