from unittest.mock import patch
from app.crud import create_producto_db
import json

MOCK_DB_DATA = {
  "categorias": [
    { "id": 10, "nombre": "Electrónica" }
  ],
  "productos": [
    { "id": 100, "nombre": "Laptop", "categoria_id": 10 }
  ]
}

def test_unit_create_producto_logic():
  nombre_producto = "producto unitario"
  categoria_id = 10
  with patch('app.crud._load_db', return_value=MOCK_DB_DATA.copy()) as mock_load_db, \
    patch('app.crud._save_db') as mock_save:
    resultado = create_producto_db(nombre_producto, categoria_id)
    assert resultado['nombre'] == nombre_producto
    assert resultado['categoria_id'] == categoria_id
    assert resultado['id'] == 101

    mock_save.assert_called_once()
    saved_data = mock_save.call_args[0][0]
    print("\n--- Datos guardados en la base de datos mock ---")
    print(json.dumps(saved_data, indent=2))
    print("--- Fin de los datos guardados ---\n")
    assert any(prod["nombre"] == nombre_producto for prod in saved_data["productos"])
