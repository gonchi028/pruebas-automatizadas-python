from unittest.mock import patch
from app.crud import create_categoria_db
import json

MOCK_DB_DATA = {
  "categorias": [
    { "id": 10, "nombre": "Electrónica" }
  ],
  "productos": []
}

def test_unit_create_categoria_logic():
  nombre_categoria = "categoria unitaria"
  with patch('app.crud._load_db', return_value=MOCK_DB_DATA.copy()) as mock_load_db, \
    patch('app.crud._save_db') as mock_save:
    resultado = create_categoria_db(nombre_categoria)
    assert resultado['nombre'] == nombre_categoria
    assert resultado['id'] == 11

    mock_save.assert_called_once()
    saved_data = mock_save.call_args[0][0]
    print("\n--- Datos guardados en la base de datos mock ---")
    print(json.dumps(saved_data, indent=2))
    print("--- Fin de los datos guardados ---\n")
    assert any(cat["nombre"] == nombre_categoria for cat in saved_data["categorias"])
