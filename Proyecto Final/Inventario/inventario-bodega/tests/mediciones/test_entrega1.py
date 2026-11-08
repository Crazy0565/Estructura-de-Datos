from mediciones import entrega1


def test_crear_producto_es_determinista():
    a, b = entrega1.crear_producto(7), entrega1.crear_producto(7)
    assert (a.id, a.nombre, a.pasillo, a.estante) == (
        b.id,
        b.nombre,
        b.pasillo,
        b.estante,
    )


def test_probar_arreglo_devuelve_capacidad_suficiente():
    insercion, acceso, capacidad, producto = entrega1.probar_arreglo(100)
    assert capacidad >= 100
    assert producto.id == 50
    assert insercion >= 0 and acceso >= 0


def test_quicksort_coincide_con_sorted(capsys):
    assert entrega1.probar_contra_sorted() is True
    assert "Orden correcto:      SI" in capsys.readouterr().out
