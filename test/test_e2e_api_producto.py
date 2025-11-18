from fastapi.testclient import TestClient
from app.main import app
import time
import json

client = TestClient(app)

def test_e2e_full_producto_lifecycle():
  # Crear una categoría primero
  cat_nombre = f"E2E Categoria {int(time.time())}"
  response_cat = client.post(
    "/categorias",
    params={"nombre": cat_nombre}
  )
  assert response_cat.status_code == 200
  categoria_creada = response_cat.json()
  categoria_id = categoria_creada['id']
  print("\nE2E: categoria creada:")
  print(json.dumps(categoria_creada, indent=2))

  # GET inicial de productos
  response_get_initial = client.get("/productos")
  initial_list = response_get_initial.json()
  initial_count = len(initial_list)
  print("\nE2E: lista inicial de productos:")
  print(json.dumps(initial_list, indent=2))
  print(f"Numero de productos: {initial_count}")

  # CREATE: Crear un nuevo producto
  prod_nombre = f"E2E Producto {int(time.time())}"
  response_post = client.post(
    "/productos",
    params={"nombre": prod_nombre, "categoria_id": categoria_id}
  )
  assert response_post.status_code == 200
  producto_creado = response_post.json()
  producto_id = producto_creado['id']
  print("\nE2E: producto creado:")
  print(json.dumps(producto_creado, indent=2))
  print("--------------")

  # Verificar que fue agregado a la lista
  response_get_after_create = client.get("/productos")
  list_after_create = response_get_after_create.json()
  print("\nE2E: lista de productos después de crear:")
  print(json.dumps(list_after_create, indent=2))
  assert len(list_after_create) == initial_count + 1
  assert any(prod['nombre'] == prod_nombre for prod in list_after_create)

  # UPDATE: Actualizar el producto
  prod_nombre_actualizado = f"E2E Producto Actualizado {int(time.time())}"
  response_put = client.put(
    f"/productos/{producto_id}",
    params={"nombre": prod_nombre_actualizado, "categoria_id": categoria_id}
  )
  assert response_put.status_code == 200
  producto_actualizado = response_put.json()
  print("\nE2E: producto actualizado:")
  print(json.dumps(producto_actualizado, indent=2))
  assert producto_actualizado['nombre'] == prod_nombre_actualizado

  # DELETE: Eliminar el producto
  response_delete = client.delete(f"/productos/{producto_id}")
  assert response_delete.status_code == 200
  print("\nE2E: producto eliminado")

  # Verificar que fue eliminado de la lista
  response_get_after_delete = client.get("/productos")
  list_after_delete = response_get_after_delete.json()
  print("\nE2E: lista de productos después de eliminar:")
  print(json.dumps(list_after_delete, indent=2))
  assert len(list_after_delete) == initial_count
  assert not any(prod['id'] == producto_id for prod in list_after_delete)
