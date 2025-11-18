from fastapi.testclient import TestClient
from app.main import app
import time
import json

client = TestClient(app)

def test_e2e_full_categoria_lifecycle():
  cat_nombre = f"E2E Categoria {int(time.time())}"
  response_get_initial = client.get("/categorias")
  initial_list = response_get_initial.json()
  initial_count = len(initial_list)
  print("\nE2E: lista inicial de categorias:")
  print(json.dumps(initial_list, indent=2))
  print(f"Numero de categorias: {initial_count}")

  # Crear una nueva categoria
  response_post = client.post(
    "/categorias",
    params={"nombre": cat_nombre}
  )
  assert response_post.status_code == 200
  categoria_creada = response_post.json()
  print("\nE2E: categoria creada:")
  print(json.dumps(categoria_creada, indent=2))
  print("--------------")

  # Verificar lista actual despues del post
  response_get_final = client.get("/categorias")
  list_final = response_get_final.json()
  print("\nE2E: lista final de categorias:")
  print(json.dumps(list_final, indent=2))
  final_count = len(list_final)
  print(f"Numero de categorias: {final_count}")
  assert final_count == initial_count + 1
  assert any(cat['nombre'] == cat_nombre for cat in list_final)
